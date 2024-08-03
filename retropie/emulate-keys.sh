#!/bin/bash

# Run these for Controller Screen mode
#if grep -Fxq "display_rotate=0" /boot/config.txt
#then
#       sudo sed -i 's/display_rotate=0/display_rotate=2/g' /boot/config.txt
#else
#       sudo sed -i 's/display_rotate=2/display_rotate=0/g' /boot/config.txt
#fi
#sudo reboot now

# Run this for Trigger mode
#sudo nohup python3 /home/pi/KeyMapper/Main.py >> /home/pi/KeyMap/output.log &

# Run this for Mapper mode
sudo python3 /home/pi/KeyMapper/Main.py --config
