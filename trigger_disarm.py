#!/usr/local/bin/python

# Created by Dan Arteaga

# This script is run when the unlock button on the keychain is pressed

# Import required libraries
import os

# Disarm the system
os.system('sudo bash /home/pi/Desktop/deactivate_system.sh')
	