#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will return the status of the alarm system

# Import required libraries
import sys,os

# Read the armed txt file
with open("txt_files/armed.txt", "r") as fo1:
    alarm_status = fo1.readline()
fo1.close()	

# Interpret the txt file
if alarm_status != "0":
    print "ACTIVATED"
else:
    print "NOT ACTIVATED"
