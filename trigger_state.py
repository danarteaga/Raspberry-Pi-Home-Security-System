#!/usr/local/bin/python

# Created by Dan Arteaga

# This script is run when a sensor is activated. Depending on the senosr, it may wait for 
# 10 seconds prior to allowing that sensor to play a sound again upon activation

# Import required libraries
import time
import os

# Check to see if file created after sensor is activated, exists
if os.path.isfile('/home/pi/Desktop/txt_files/state.txt') == False:

	os.system("echo -n 1 > /home/pi/Desktop/txt_files/trigger.txt")
	time.sleep(0.5) #Keep
	os.system("echo -n 1 > /home/pi/Desktop/txt_files/state.txt")
	time.sleep(10)
	os.remove('/home/pi/Desktop/txt_files/state.txt')
	