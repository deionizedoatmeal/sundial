#!/bin/bash

echo "Type what color setting you would like (0-5), followed by [ENTER]:"
read color

#check setting is an int
re='^[0-9]+$'
if ! [[ $color =~ $re ]] ; then
   echo "error1: not a valid setting" >&2; exit 1
#check setting is not to large
elif (($color > 5)) ; then
  echo "error2: not a valid setting" >&2; exit 1
#or to small
elif (($color < 1)) ; then
  echo "error3: not a valid setting" >&2; exit 1
else
  rm colorsetting; touch colorsetting;
  echo "$color" >> colorsetting;
  echo "Alarm colorsetting is set to $color"; exit 1
fi
