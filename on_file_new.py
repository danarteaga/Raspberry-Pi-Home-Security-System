#!/usr/local/bin/python

# Created by Dan Arteaga

# This script determines whether or not new motion is detected by the camera
# Of note, this is only relevant when the system is armed

# Import required libraries
import os,glob,datetime,time
import sys,subprocess,random

# Load data from the input_variable.txt file:
with open('input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
	
for new_lines in content:	
	try:
		if new_lines[0] != '#':	
			if 'python_interpreter' in new_lines:
				python_interpreter = new_lines.split(" ")[1:][0]	
	except:
		pass

# Remove file - which is created when new motion detected by camera - if it exists
os.system('sudo rm /home/pi/Desktop/txt_files/motion_files.txt >/dev/null 2>&1')

xbo = False
while xbo == False:

	# If no new motion detected by camera, keep looping through
	if os.path.exists('/home/pi/Desktop/txt_files/motion_files.txt') == False:
		time.sleep(0.5)
		
	else:	
	
		# Move to Camera directory
		os.chdir('/home/pi/Desktop/Camera')
		
		# Create name of new random directory
		new_fold = random.sample(range(10000000), 1)
		new_fold = new_fold[0]
		
		# Create new random directory
		to_move1 = 'mkdir /home/pi/Desktop/Camera_%s' %(new_fold) 		
		os.system(to_move1)
		
		# Move the files to this new temporary directory
		to_move2 = 'mv *jpg* /home/pi/Desktop/Camera_%s' %(new_fold) 
		os.system(to_move2)
		
		# Run the on_file_new1.py script, then keep looping through
		to_out = '%s /home/pi/Desktop/on_file_new1.py %s' %(python_interpreter,new_fold) 
		subprocess.Popen(to_out, shell=True, stdout=subprocess.PIPE)
		
		# Remove file, which is created when new motion detected by camera 
		os.system('sudo rm /home/pi/Desktop/txt_files/motion_files.txt')
