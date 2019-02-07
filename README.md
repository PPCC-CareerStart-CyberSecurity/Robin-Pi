# Robin-Pi (Needs Better Name)
Tools and Software for Gadget Mode Raspberry Pi Zero W devices

A PPCC Career Start Cyber Security project

Default Hardware:
 * Raspberry Pi Zero W
 * Zero Stem for Pi Zero
 * Adafruit 128x64 OLED Bonnet for Raspberry Pi
  
# SETUP:

Enabling SSH over USB
   
  Mount the micro sd card containing your operating system, using an adapter if necessary
  
  Open the Boot partition    
  
  Create a new, empty file named ssh in the top level directory of Boot
    
Enabling Ethernet Gadget mode
  
   Open config.txt, and add the following on a new line:
  
    dtoverlay=dwc2
  
   Open cmdline.txt, and add the following at the end of the first line:
   
    modules-load=dwc2,g_ether
    
# CONNECTING:

By USB Stem:
  Plug your raspberry pi gadget directly into a powered USB port
  
  By Micro USB Cable:
    Plug your Micro USB cable into the micro USB port closest to the middle of the board. If you have your USB Stem installed, it'll be at the end of the red arm labelled D+ D-.

DO NOT USE BOTH CONNECTION METHODS AT THE SAME TIME!

To WiFi:

  Type the following command to open the Raspberry Pi Configuration Utility:
 
    sudo raspi-config
    
  Highlight the second line for Network Options, and press enter
  
  If prompted for your country, scroll allllllll the way down to United States, then press enter
  
  If you're on the PPCC campus, your SSID will be:
  
    PPCC GUEST
    
  ... and there won't be a password. You'll have to supply the correct SSID/Passkey for other networks you try to connect to, however
  Back at the raspi-config menu, press right twice, then press enter when FINISH is highlighted
  
  Reboot if requested, or test your WiFi connection by typing:
  
    ping google.com
    
  Linux will ping forever, so kill it with ctrl-c

To OLED Bonnet:

    sudo raspi-config
  
  Highlight 5 Interfacing Options and press enter

  Highlight A5 I2C and press enter

  Highlight Yes and press enter

  Reboot with:
 
    sudo reboot

# INSTALLING REQUIRED DEPENDENCIES
 (Adapted from https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/usage)
  
# RPi.GPIO

  From the bash shell:

    sudo apt-get update

    sudo apt-get install build-essential python-dev python-pip

    sudo pip install RPi.GPIO

# Python Imaging Library

    sudo apt-get install python-imaging python-smbus i2c-tools

# Adafruit SSD1306 python library code

    sudo apt-get install git
  
    git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
  
    cd Adafruit_Python_SSD1306
  
    sudo python setup.py install
  
# TESTING YOUR SCREEN AND BUTTONS:
  
  cd to the Adafruit_Python_SSD1306 folder, then run:
  
    sudo python examples/buttons.py
  
  Try the other scripts in the examples directory, then read through the code to see how they work
    
# STARTING SCRIPTS ON BOOT:

  Add commands on new lines in /etc/rc.local to run those commands when the RPi0W boots, such as the stats demo:
  
    sudo nano /etc/rc.local
  
  Add this line before the line containing "exit 0"
 
    sudo python /home/pi/Adafruit_Python_SSD1306/examples/stats.py  &
 
  Then ctrl-o enter ctrl-x to save and quit
  
# TRANSFERING FILES FROM YOUR PI

  Install proftp:
    
    sudo apt install proftpd
    sudo service proftpd reload
    
  Connect to proftpd server from host computer (in-browser):
  
    ftp://(your USB IP address)
    
# SETTING UP A WIFI ACCESS POINT ON YOUR PI
  (Adapted from: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)

  Update apt-get, if you haven't recently:
  
    sudo apt-get update
    
  Install dnsmasq (dhcp service) and hostapd (access point software):
  
    sudo apt-get install dnsmasq hostapd
  
  Shut off dnsmasq and hostapad until after they've been configured:
  
    sudo systemctl stop dnsmasq
    sudo systemctl stop hostapd
    
  # Configure dnsmasq
  Backup the original dnsmasq.conf file, and create a simpler version:
  
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  
    sudo nano /etc/dnsmasq.conf
    
  Add the following to your new dnsmasq.conf file:
  
    interface=wlan0      # If your wireless interface is something else, use that instead
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h

  # Configure hostapd
  Create a new /etc/hostapd/hostapd.conf file, and populate it with your network settings.
  Change the settings below to fit your requirements:
  
    interface=wlan0
    driver=nl80211
    ssid=HackMyPi
    hw_mode=g
    channel=7
    wmm_enabled=0
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=ChangeThisPassword
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP
    
  Edit /etc/default/hostapd to update the location of hostapd.conf:
  
    sudo nano /etc/default/hostapd
    
  Uncomment the line that starts with #DAEMON_CONF, and change it to this:
  
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    
  Start both services now:
  
    sudo systemctl start hostapd
    sudo systemctl start dnsmasq
    
  You should now be able to connect to your Pi Thing by switching to the Wireless network you specified (HackMyPi in this example), and sshing the usual way. If you still want to connect to the internet with your Pi Thing, you have a few more steps to complete, though.
  
  #Setting up IP forwarding
  
    sudo nano /etc/sysctl.conf
    
  Find #net.ipv4.ip_forward=1 and delete the #, then save and exit.
  
  Tell the firewall (iptables) to allow outbound traffic on eth0:
  
    sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
    
  Add this line to /etc/rc.local, just above exit 0, to set the rule on boot:
  
    iptables-restore < /etc/iptables.ipv4.nat
    
  Reboot:
  
    sudo reboot
  
# CLEAR SCREEN ON LOGIN
If you've added a script to /etc/rc.local, and you subsequently start another script that attempts to use the display, both programs will interfere if you don't kill the first script first. If your rc.local script has done its job and you don't need it anymore, just add these two lines to the end of your ~/.profile file:

    sudo kill $(ps -ax | grep '[p]ython /home/pi/' | grep -v sudo | awk '{print $1}') 2> /dev/null
    sudo python ~/bin/clear.py
    
