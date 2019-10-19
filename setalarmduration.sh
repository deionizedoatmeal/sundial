#!/bin/bash

echo "Type how long before the alarm you would like the sunrise to start (0-90 min), followed by [ENTER]:"
read duration

#check duration is an int
re='^[0-9]+$'
if ! [[ $duration =~ $re ]] ; then
   echo "error1: not a valid duration" >&2; exit 1
#check duration is not to large
elif (($duration > 90)) ; then
  echo "error2: not a valid duration" >&2; exit 1
#or to small
elif (($duration < 1)) ; then
  echo "error3: not a valid duration" >&2; exit 1
else
  rm alarmduration; touch alarmduration;
  echo "$duration" >> alarmduration;
  echo "Alarm duration is set to $duration min"; exit 1
fi
