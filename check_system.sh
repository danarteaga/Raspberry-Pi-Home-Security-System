#!/bin/bash

# Created by Dan Arteaga

# This script will determine whether or not to turn on motion detection

# Change to the Desktop directory
cd /home/pi/Desktop

# Read the armed.txt file
input="/home/pi/Desktop/txt_files/armed.txt"
while IFS='' read -r var 
do
 echo "$var" >/dev/null 2>&1
done < "$input"

if [ "$var" -eq "0" ]
  then
    # If armed.txt is 0 (disarmed), pause Motion software
    /usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/pause"
else
  # If armed.txt is 1 (armed), start Motion software
  /usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/start"
fi

sudo python /home/pi/Desktop/alarm.py >/dev/null 2>&1
