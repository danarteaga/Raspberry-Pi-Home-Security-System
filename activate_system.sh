#!/bin/bash

# Created by Dan Arteaga

# This script will arm the alarm system 
# The user has ~60 seconds to leave the house while the music plays

# Change to Desktop directory
cd /home/pi/Desktop

# I don't remember what keep_armed does...:/
echo -n 1 > txt_files/keep_armed.txt

# Motion_sound, when 0, will not allow any sound to play from speakers except
# for sound played directly from this script (e.g. no door opening sound)
echo -n 0 > txt_files/motion_sound.txt

# Randomly play of the 3 60-second song files available
rand1=$(( ( RANDOM % 3 )  + 1 ))
if [ "$rand1" -eq 1 ]
  then
     sudo mpg321 -g 100 sound_files/Interstellar.mp3
elif [ "$rand1" -eq 2 ]
  then
     sudo mpg321 -g 10 sound_files/Time.mp3
elif [ "$rand1" -eq 3 ]
  then
     sudo mpg321 -g 100 sound_files/MadMax.mp3	 
fi

# Don't activate immediately to allow user to leave room when song ends
sleep 5

# This is when the system is finally armed
echo -n 1 > txt_files/armed.txt

# Turn on Motion software (from pause state) via RPI_IP:webcontrol_port
/usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/start" 
# Motion software will then run on_file1.sh when detects motion

# Speakers will pronounce that system is activated (i.e. armed)
# where -g 80 is the volume levl
sudo mpg321 -g 80 /home/pi/Desktop/sound_files/activate.mp3 >/dev/null 2>&1 

# Allow other sound to come from speakers again
echo -n 1 > txt_files/motion_sound.txt
