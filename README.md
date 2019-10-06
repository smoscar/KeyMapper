# KeyMapper
Maps different controller input events to keyboard key presses and vice versa. It can be used to simulate non-existing buttons and even simulate analog+digital triggers like the ones available in the Gamecube controller.

## Features
  - Maps controller button events to key press events.
  - Maps analog stick/triggers to single key press events.
  - Maps single analog stick/triggers to multiple key press events.
  - Maps multiple controller events to single key press events.
  - Includes Retropie menu integration.
![Dreamcast controller example](https://ezway-imagestore.s3.amazonaws.com/files/2019/10/16731640991570305049.png)
  
## Installation
```
sudo pip install evdev
cd
git clone https://github.com/smoscar/KeyMapper.git
sudo reboot now
```

## Configuration
Run the script in configuration mode:
```
sudo python Main.py --config
```
Go through the instructions to configure your controller events.

## Retropie config
This optional config will run the script for you without manually SSH-ing into the Pi.
```
cp ~/KeyMapper/retropie/emulate-keys.sh /home/pi/RetroPie/retropiemenu/
cp ~/KeyMapper/retropie/emulatekeys.png /home/pi/RetroPie/retropiemenu/icons/
```
Add the following entry to the gamelist XML
```
vi /opt/retropie/configs/all/emulationstation/gamelists/retropie/gamelist.xml
```
```
        <game>
                <path>./emulate-keys.sh</path>
                <name>Key Mapper</name>
                <desc>Maps the controller events to keyboard key press events.</desc>
                <image>/home/pi/RetroPie/retropiemenu/icons/emulatekeys.png</image>
                <playcount>1</playcount>
                <lastplayed>20190704T182042</lastplayed>
        </game>
```
After rebooting you should see the option in Settings.
