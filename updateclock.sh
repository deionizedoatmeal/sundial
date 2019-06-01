#!/bin/bash
cd
# remove old version
sudo rm -r ~/sundial

# clone in the new version
git clone https://github.com/deionizedoatmeal/sundial.git

# move scripts to bin
sudo cp ~/sundial/updateclock.sh /bin/updateclock

# start the clock
sudo python ~/sundial/sundial.py

