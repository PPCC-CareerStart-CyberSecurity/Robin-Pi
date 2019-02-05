import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time
import subprocess

# Inputs for AdaFruit SSD1306 128x64 Bonnet:
U_pin = 17
D_pin = 22
C_pin = 4
L_pin = 27
R_pin = 23

A_pin = 5
B_pin = 6

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library, clear display.
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Define some constants.
x = 0
y = 0

# Load default font.
font = ImageFont.load_default()

except KeyboardInterrupt:
    GPIO.cleanup()
