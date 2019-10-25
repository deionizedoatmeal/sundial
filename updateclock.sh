#!/bin/bash
cd

sudo pkill python
echo CLOCK KILLED

# presistant alarm settings
cp sundial/colorsetting colorsetting
cp sundial/alarmduration alarmduration
cp sundial/alarmtimemin alarmtimemin
cp sundial/alarmtimehour alarmtimehour
cp sundial/graphicalsetting graphicalsetting
echo SETTINGS SAVED

# remove old version
sudo rm -r sundial
echo OLD VERSION REMOVED

# clone in the new version
git clone https://github.com/deionizedoatmeal/sundial.git
echo REPO CLONED

# move scripts to bin
sudo cp sundial/setcolor.sh /bin/setcolor
sudo cp sundial/setalarmduration.sh /bin/setalarmduration
sud0 cp sundial/setgraphical.sh /bin/setgraphical
sudo cp sundial/setalarmtime.sh /bin/setalarmtime
sudo cp sundial/updateclock.sh /bin/updateclock
sudo cp sundial/installdependencies.sh /bin/installdependencies
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
sudo ./sundial/sundial.py
echo CLOCK RUNNING
