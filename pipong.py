# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Additional code by Neil Austin. Do whatever you want with it, just don't
# complain to me when something I've added doesn't work, or explodes your pet
# emu or whatever. It's probably James DeVito's fault, anyway.

# Waveshare-specific libraries
#from luma.core.interface.serial import i2c, spi
#from luma.core.render import canvas
#from luma.core import lib
#from luma.oled.device import sh1106

import RPi.GPIO as GPIO

import time

# AdaFruit-specific libraries
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Input pins for AdaFruit 128x64 Bonnet:
L_pin = 27
R_pin = 23
C_pin = 4
U_pin = 17
D_pin = 22

A_pin = 5
B_pin = 6

# Input pins for Waveshare 128x64 Bonnet:
#L_pin = 5
#R_pin = 26
#C_pin = 13
#U_pin = 6
#D_pin = 19
#
#A_pin = 21
#B_pin = 20
#C_pin = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


# Adafruit-specific pin configuration:
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Waveshare-specific pin configuration:
#RST = 25
#DC = 24
#CS = 8

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Define some constants.
padding = -2
top = padding
bottom = height-padding
x = 0

# Load default font.
font = ImageFont.load_default()

# Initialize Playing Field
hi_score = 0
bounces = 0
# Start ball in middle court
ex = 63
ey = 31
# Initial velocity down and right 4x
dx = 4
dy = 4
# Size of ball = 5px radius
ra = 5
di = 2*ra
# Center Left Paddle Motionless
lp_width = 4
lp_height = 25
lp_t = (height - lp_height) / 2
lp_b = lp_t + lp_height -1
lp_l = 0
lp_r = lp_l + lp_width
lp_dv = 0
lp_score = 0
# Center Right Paddle Motionless
rp_width = 4
rp_height = 25
rp_t = (height - rp_height) / 2
rp_b = rp_t + rp_height -1
rp_l = width - rp_width -1
rp_r = width -1
rp_dv = 0
rp_score = 0


# Use for scoreboard
font = ImageFont.load_default()

try:
    while 1:

	# Blank the screen before drawing the next frame
	draw.rectangle((0,0,width,height), outline =0, fill=0)

	# Draw the playing field
	draw.line((0, 0,127, 0), fill=255)		# Top Wall
	draw.line((0,63,127,63), fill=255)		# Bottom Wall
	draw.line((width/2,0,width/2,63), fill=255)	# Center Court

	# Draw the ball
	draw.ellipse((ex,ey,ex+di,ey+di), outline=255, fill=255)
	if (( ex > rp_l-di) and ((ey+ra >= rp_t) and (ey+ra <= rp_b))):
		dx = dx * -1
		if rp_dv > 0:
			dy = dy +1
			bounces = bounces +1
		elif rp_dv < 0:
			dy = dy -1
			bounces = bounces +1
	elif ((ex < lp_r) and ((ey+ra >= lp_t) and (ey+ra <= lp_b))):
		dx = dx * -1
		if lp_dv > 0:
			dy = dy +1
			bounces = bounces +1
		elif lp_dv < 0:
			dy = dy -1
			bounces = bounces +1
	if (ey > height - di) or ((ey < 0) and (dy < 0)):
		dy = dy * -1
	ex = ex + dx
	ey = ey + dy

	# Reset Ball and Update Score if Ball Leaves Court
	if ex < 0-di:
		ex = 63
		ey = 31
		dx = dx * -1
		dy = dy * -1
		rp_score = rp_score +1
		bounces = 0
		time.sleep(.5)
	elif ex > width+di:
		ex = 63
		ey = 31
		dx = dx * -1
		dy = dy * -1
		lp_score = lp_score +1
		bounces = 0
		time.sleep(.5)
	if bounces > hi_score:
		hi_score = bounces

	# Draw the Scores
	draw.text((((width/4)*1), ra), str(lp_score), font=font, fill=255)
	draw.text((((width/4)*3), ra), str(rp_score), font=font, fill=255)
	draw.text(((width/2), di), str(hi_score), font=font, fill=255)

	# Draw the left paddle
	draw.rectangle((lp_l,lp_t,lp_r,lp_b), outline=255, fill=1)
	if (lp_b >= height) and (lp_dv > 0):
		lp_dv = lp_dv * -1
	elif (lp_t <=0) and (lp_dv < 0):
		lp_dv = lp_dv * -1
	lp_t = lp_t + lp_dv
	lp_b = lp_t + lp_height -1

	# Draw the right paddle
	draw.rectangle((rp_l,rp_t,rp_r,rp_b), outline=255, fill=1)
	if (rp_b >= height) and (rp_dv > 0):
		rp_dv = rp_dv * -1
	elif (rp_t <= 0) and (rp_dv < 0):
		rp_dv = rp_dv * -1
	rp_t = rp_t + rp_dv
	rp_b = rp_t + rp_height -1

	# Update Paddle Velocities

	# Left Joystick pressed up
        if GPIO.input(U_pin): # button is released
		if (lp_dv < 0):
			lp_dv = lp_dv +1
        else: # button is pressed:
		if (lp_dv > -3):
			lp_dv = lp_dv -1

	# Left Joystick pressed down
        if GPIO.input(D_pin): # button is released
		if (lp_dv > 0):
			lp_dv = lp_dv -1
        else: # button is pressed:
		if (lp_dv < 3):
			lp_dv = lp_dv +1

	# Right Bottom Button pressed:
        if GPIO.input(A_pin): # button is released
		if (rp_dv > 0):
			rp_dv = rp_dv -1
        else: # button is pressed:
		if (rp_dv < 3):
			rp_dv = rp_dv +1

	# Right Top Button pressed:
        if GPIO.input(B_pin): # button is released
		if (rp_dv < 0):
			rp_dv = rp_dv +1
        else: # button is pressed:
		if (rp_dv > -3):
			rp_dv = rp_dv -1

	disp.image(image)
        disp.display()
#        time.sleep(.005)


except KeyboardInterrupt:
    GPIO.cleanup()
