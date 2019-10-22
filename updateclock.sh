#!/bin/bash
cd

sudo pkill python
echo CLOCK KILLED

# presistant alarm settings
cp sundial/colorsetting colorsetting
cp sundial/armduration alarmduration
cp sundial/armtimemin alarmtimemin
cp sundial/armtimehour alarmtimehour
cp sundial/graphicalsetting graphicalsetting
echo SETTINGS SAVED

# remove old version
sudo rm -r sundial
echo OLD VERSION REMOVED

# clone in the new version
git clone https://github.com/deionizedoatmeal/sundial.git
echo REPO CLONED

# dependencies
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel datetime time subprocess webcolors spidev
echo DEPENDENCIES INSTALLED

# move scripts to bin
for f in sundial/*.sh; do
  base_name='echo $f \ cut -d "." -f 1'

sudo cp sundial/$f /bin/$base_name
echo SCRIPTS DROPPED IN BIN

# set alarm
cp colorsetting sundial/colorsetting
cp alarmduration sundial/alarmduration
cp alarmtimemin sundial/alarmtimemin
cp alarmtimehour sundial/alarmtimehour
cp graphicalsetting sundial/graphicalsetting

rm colorsetting
rm alarmduration
rm alarmtimemin
rm alarmtimehour
rm graphicalsetting
echo ALARM SET

# start the clock
./sundial/sundial.py
echo CLOCK RUNNING
