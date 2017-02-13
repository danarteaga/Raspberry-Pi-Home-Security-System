#!/bin/bash

# Created by Dan Arteaga

# This script will disarm the system

# Change to the Desktop directory
cd /home/pi/Desktop

# When this file is created, the alarm.py script will know to disarm the system
echo 'Test' > /home/pi/Desktop/txt_files/myfile.txt

# Pause the Motion software
/usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/pause" 

# Disarm the system
sudo echo -n 0 > txt_files/armed.txt

# Read the motion_sound.txt file
input="/home/pi/Desktop/txt_files/motion_sound.txt"
while IFS='' read -r var 
do
 echo "$var" >/dev/null 2>&1
done < "$input"

if [ "$var" -eq "1" ]
 then
    # If motion_sound.txt is 0, play this sound right away (at volume of 80)
    sudo mpg321 -g 80 /home/pi/Desktop/sound_files/deactivate.mp3 >/dev/null 2>&1
else
    # If motion_sound.txt is 1, play this sound right after 3 seconds
    sleep 3
    sudo mpg321 -g 80 /home/pi/Desktop/sound_files/deactivate.mp3 >/dev/null 2>&1  
fi

# Motion_sound, when 0, will not allow any sound to play from speakers
echo -n 1 > txt_files/motion_sound.txt
