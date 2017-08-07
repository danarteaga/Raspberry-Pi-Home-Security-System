#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will update all relevant files and reboot the system


# Import required libraries
import os,glob,datetime,time
import sys,subprocess,random

# Load data from the input_variable.txt file:
with open('input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
# Obtain the python interpreter
for new_lines in content:	
	try:
		if new_lines[0] != '#':	
			if 'python_interpreter' in new_lines:
				python_interpreter = new_lines.split(" ")[1:][0]	
	except:
		pass

# Obtain Camera folders that have not been processed
mylist = glob.glob("Camera_*")

# Run through each folder and rerun script 
for myfolder in mylist:

	#curtime = time.time() - os.stat(myfolder).st_mtime 
	#if (curtime/3600) < 1:
	#	pass
	#else:	
	to_out = '%s /home/pi/Desktop/on_file_new2.py %s' %(python_interpreter,myfolder[7:]) 
	subprocess.Popen(to_out, shell=True, stdout=subprocess.PIPE)

		
# Run through each folder one more time
for myfolder in mylist:		
		
	# If the folder still exists, then delete it
	os.rmdir(myfolder)
		