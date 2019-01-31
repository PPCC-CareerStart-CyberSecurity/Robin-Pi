#!/usr/bin/env python
# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

#from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Load default font
font = ImageFont.load_default()

#GPIO define
RST_PIN        = 24
CS_PIN         = 8
DC_PIN         = 23
KEY_UP_PIN     = 17
KEY_DOWN_PIN   = 22
KEY_LEFT_PIN   = 27
KEY_RIGHT_PIN  = 23
KEY_PRESS_PIN  = 4
KEY1_PIN       = 5
KEY2_PIN       = 20
KEY3_PIN       = 6

SPI_PORT = 0
SPI_DEVICE = 0

#Initialize Display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

# Create blank image
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

#SPI or IIC
#USER_I2C = 0
#if  USER_I2C == 1:
#	GPIO.setup(RST_PIN,GPIO.OUT)
#	GPIO.output(RST_PIN,GPIO.HIGH)
#
#	serial = i2c(port=1, address=0x3c)
#else:
#	serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = DC_PIN, gpio_RST = RST_PIN)
#device = sh1106(serial, rotate=2) #sh1106

#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
#width = 128
#height = 64
#image = Image.new('1', (width, height))

# Get drawing object to draw on image.
#draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

# Intialize Playing Field
hi_score = 0
bounces = 0
# Start ball in middle of screen
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
rp_l = width - rp_width - 1
rp_r = width - 1
rp_dv = 0
rp_score = 0

# Use for scoreboard
font = ImageFont.load_default()

try:
	while 1:
		with canvas(device) as draw:

			# Blank the screen before drawing the next frame
			draw.rectangle((0,0,width,height), outline =0, fill=0)

			# Draw the playing field
			draw.line((0, 0,127, 0), fill=255) 		# Top Wall
			draw.line((0,63,127,63), fill=255) 		# Bottom Wall
			draw.line((width/2,0,width/2,63), fill=255) 	# Center Court

			# Draw the ball
			draw.ellipse((ex,ey,ex+di,ey+di), outline=255, fill=255)
			if ((ex > rp_l-di) and ((ey+ra >= rp_t) and (ey+ra <= rp_b))):
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
				rp_score = rp_score +1
				bounces = 0
			elif ex > width+di:
				ex = 63
				ey = 31
				dx = dx * -1
				lp_score = lp_score +1
				bounces = 0
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
			elif (lp_t <= 0) and (lp_dv < 0):
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
			if GPIO.input(KEY_UP_PIN): # button is released
				if (lp_dv < 0):
					lp_dv = lp_dv +1
			else: # button is pressed:
				if (lp_dv > -3):
					lp_dv = lp_dv -1

			# Left Joystick pressed down
			if GPIO.input(KEY_DOWN_PIN): # button is released
				if (lp_dv > 0):
					lp_dv = lp_dv -1
			else: # button is pressed:
				if (lp_dv < 3):
					lp_dv = lp_dv +1

#			if GPIO.input(KEY_PRESS_PIN): # button is released
#			else: # button is pressed:

			# Right Top Button pressed
			if GPIO.input(KEY1_PIN): # button is released
				if (rp_dv < 0):
					rp_dv = rp_dv +1
			else: # button is pressed:
				if (rp_dv > -3):
					rp_dv = rp_dv -1

#			if GPIO.input(KEY2_PIN): # button is released
#			else: # button is pressed:

			# Right Botton Button pressed
			if GPIO.input(KEY3_PIN): # button is released
				if (rp_dv > 0):
					rp_dv = rp_dv -1
			else: # button is pressed:
				if (rp_dv < 3):
					rp_dv = rp_dv +1

except:
	print("except")
GPIO.cleanup()
