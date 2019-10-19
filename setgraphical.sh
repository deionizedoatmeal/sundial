#!/bin/bash

echo "Graphical window open? (decresses preformance). 1=open, 0=closed, followed by [ENTER]:"
read graphical

#check setting is an int
re='^[0-9]+$'
if ! [[ $graphical =~ $re ]] ; then
   echo "error1: not a valid setting" >&2; exit 1
#check setting is not to large
elif (($graphical > 1)) ; then
  echo "error2: not a valid setting" >&2; exit 1
#or to small
elif (($graphical < 0)) ; then
  echo "error3: not a valid setting" >&2; exit 1
else
  rm graphicalsetting; touch graphicalsetting;
  echo "$graphical" >> graphicalsetting;
  echo "Graphical window is set to $graphical"; exit 1
fi
