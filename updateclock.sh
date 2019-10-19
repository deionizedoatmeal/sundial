#!/bin/bash
cd

sudo pkill python
echo KILLED

# remove old version
sudo rm -r ../sundial
echo REMOVED

# clone in the new version
git clone https://github.com/deionizedoatmeal/sundial.git
echo CLONED

# move scripts to bin
sudo cp sundial/updateclock.sh /bin/updateclock
echo MOVED

# start the clock
