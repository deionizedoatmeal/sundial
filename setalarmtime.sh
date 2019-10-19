#!/bin/bash

echo "Type the hour you would like the alarm to go off at (24hr), followed by [ENTER]:"
read hour
echo "Type the minute you would like the alarm to go off at, followed by [ENTER]:"
read min

#check hour is an int
re='^[0-9]+$'
if ! [[ $hour =~ $re ]] ; then
   echo "error4: not a valid time" >&2; exit 1
#check hour is not to large
elif (($hour > 23)) ; then
  echo "error5: not a valid time" >&2; exit 1
#or to small
elif (($hour < 0)) ; then
  echo "error6: not a valid time" >&2; exit 1
#check min is an int
elif ! [[ $min =~ $re ]] ; then
   echo "error7: not a valid time" >&2; exit 1
#check min is not to large
elif (($min > 59)) ; then
  echo "error8: not a valid time" >&2; exit 1
#or to small
elif (($min < 0)) ; then
  echo "error9: not a valid time" >&2; exit 1
else
  rm alarmtimehour; touch alarmtimehour;
  rm alarmtimemin; touch alarmtimemin;
  echo "$hour" >> alarmtimehour;  echo "$min" >> alarmtimemin;
  echo "Alarm is set to $hour:$min"; exit 1
fi
