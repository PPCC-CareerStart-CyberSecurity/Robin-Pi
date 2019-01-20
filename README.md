# Robin-Pi (Needs Better Name)
Tools and Software for Gadget Mode Raspberry Pi Zero W devices

A PPCC Career Start Cyber Security project

Default Hardware:
  * Raspberry Pi Zero W
  * Zero Stem for Pi Zero
  * Adafruit 128x64 OLED Bonnet for Raspberry Pi
  
# SETUP:

Enabling SSH over USB

  On Windows:
  
    * Mount the micro sd card containing your operating system, using an adapter if necessary.
    * Open the Boot partition.    
    * Create a new, empty file named ssh in the top level directory of Boot.
    
Enabling Ethernet Gadget mode

  On Windows:
  
    * Open config.txt, and add the following on a new line:
      dtoverlay=dwc2
    
