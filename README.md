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
  
   * Mount the micro sd card containing your operating system, using an adapter if necessary
   * Open the Boot partition    
   * Create a new, empty file named ssh in the top level directory of Boot
    
Enabling Ethernet Gadget mode

  On Windows:
  
   * Open config.txt, and add the following on a new line:
      dtoverlay=dwc2
   * Open cmdline.txt, and add the following at the end of the first line:
      modules-load=dwc2,g_ether
    
# CONNECTING:

By USB Stem:
  Plug your raspberry pi gadget directly into a powered USB port
  
By Micro USB Cable:
  Plug your Micro USB cable into the micro USB port closest to the middle of the board. If you have your USB Stem installed, it'll be at the end of the red arm labelled D+ D-.

# DO NOT USE BOTH CONNECTION METHODS AT THE SAME TIME!
