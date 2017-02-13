#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will restart insync-portable on startup and periodically according to 
# the cronjob schedule

# Import required libraries
import sys,os
import subprocess
import time 
aa = False

# Kill existing insync-portable instances
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
	if 'insync-portable' in line:
		#pid = int(line.split(None, 1)[0])
		#to_kill = "sudo kill %s" %(pid)
		#os.system(to_kill)
		aa = True
		pass

# If no insync-portable process exists, start it up		
if aa == False:		
	os.chdir('/home/pi/Desktop/insync-portable')
	os.system('sudo ./insync-portable start')
