# Pisteroids by Neil Austin, based on decades-old mismemories of Asteroids!
# Feel free to do whatever you want with this code; I'm not going to pretend
# it's in any way optimized or brilliant. That said; enjoy!

import RPi.GPIO as GPIO
import time

# AdaFruit-specific libraries
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from math import *

import subprocess

# Input pins for AdaFruit 128x64 Bonnet:
U_pin = 17
D_pin = 22
L_pin = 27
R_pin = 23
C_pin = 4

A_pin = 5
B_pin = 6

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

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

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

# Load default font.
font = ImageFont.load_default()

# Initialize Playing Field
hi_score = 0
nu_score = 0

# Start ship in middle screen, facing up
ex = width/2
ey = height/2
er = 0		# Rotation 0: pointing up

nose = 6
wing = 4

# Use for scoreboard
font = ImageFont.load_default()

def rot_point(angle,point,origin):
	dx = point[0] - origin[0]
	dy = point[1] - origin[1]
	nx = (dx*cos(radians(angle))) - (dy*sin(radians(angle)))
	ny = (dx*sin(radians(angle))) + (dy*cos(radians(angle)))
	nx += origin[0]
	ny += origin[1]
	return nx,ny

ship = (ex,ey)
ship_velocity = (0,0)
ship_acceleration = (0,0)
ship_dv = 0
r = 0
r_dv = 0

try:
    while 1:

	# Blank the screen before drawing the next frame
	draw.rectangle((0,0,width,height), outline =0, fill=0)

	# Redraw the ship
	# Note; the ship rotates around its stern/engine

	if ship[0]>width+nose:
		ship = -nose,ship[1]
	elif ship[0]<-nose:
		ship = width+nose,ship[1]
	if ship[1]>height+nose:
		ship = ship[0],-nose
	elif ship[1]<-nose:
		ship = ship[0],height+nose

	ship = (ship[0]+ship_velocity[0]),(ship[1]+ship_velocity[1])

	bow   = rot_point(r,(ship[0],  ship[1]-nose),ship)
	strbd = rot_point(r,(ship[0]+wing,ship[1]+wing),ship)
	port  = rot_point(r,(ship[0]-wing,ship[1]+wing),ship)
	stern = ship
	draw.line((bow,strbd),  fill=255)
	draw.line((strbd,stern),fill=255)
	draw.line((stern,port), fill=255)
	draw.line((port,bow),   fill=255)

	# Draw the Scores
#	draw.text(((width/2), 10), str(hi_score), font=font, fill=255)

	# Update Ship Velocities

	# A and B buttons both pressed (to kill Velocity)
	# THIS IS A TOTAL HACK -- remove after fixing speed limit
	if not GPIO.input(A_pin) and not GPIO.input(B_pin):
		ship_velocity = (0,0)
		ship_acceleration = (0,0)

	# Joystick pressed right (rotate right)
	if not GPIO.input(R_pin) and r_dv < 30:
		r_dv += 5
	# Joystick pressed left (rotate left)
	elif not GPIO.input(L_pin) and r_dv >-30:
		r_dv -= 5
	# Joystick pressed center (kill rotation)
	elif not GPIO.input(C_pin):
		r_dv = 0
	# Joystick pressed up (accelerate forward)
	# Stop accelerating at 3, but don't lock out acceleration in other directions! FIX THIS
	if (not GPIO.input(U_pin)) and ship_dv<4:
		ship_dv += 1
		ship_acceleration = rot_point(r,(0,ship_dv),(0,0))
		ship_velocity = (ship_velocity[0]-ship_acceleration[0],ship_velocity[1]-ship_acceleration[1])
	elif (not GPIO.input(D_pin)) and ship_dv>-4:
		ship_dv -= 1
		ship_acceleration = rot_point(r,(0,ship_dv),(0,0))
		ship_velocity = (ship_velocity[0]-ship_acceleration[0],ship_velocity[1]-ship_acceleration[1])
	else:
		ship_dv = 0
		ship_acceleration = (0,0)

	# Update Angle
	r += r_dv

	# Joystick pressed up
#       if GPIO.input(U_pin): # button is released
#		if (lp_dv < 0):
#			lp_dv = lp_dv +1
#       else: # button is pressed:
#		if (lp_dv > -3):
#			lp_dv = lp_dv -1

	# Joystick pressed down
#        if GPIO.input(D_pin): # button is released
#		if (lp_dv > 0):
#			lp_dv = lp_dv -1
#        else: # button is pressed:
#		if (lp_dv < 3):
#			lp_dv = lp_dv +1

	# Right Bottom Button pressed:
#        if GPIO.input(A_pin): # button is released
#		if (rp_dv > 0):
#			rp_dv = rp_dv -1
 #       else: # button is pressed:
#		if (rp_dv < 3):
#			rp_dv = rp_dv +1

	# Right Top Button pressed:
 #       if GPIO.input(B_pin): # button is released
#		if (rp_dv < 0):
#			rp_dv = rp_dv +1
 #       else: # button is pressed:
#		if (rp_dv > -3):
#			rp_dv = rp_dv -1

	disp.image(image)
        disp.display()
#        time.sleep(.005)

except KeyboardInterrupt:
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	disp.image(image)
	disp.display()
	GPIO.cleanup()
