#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will update all relevant files and reboot the system

import glob,os,time

mylist = glob.glob("Camera_*")
print mylist

for myfolder in mylist:
	curtime = time.time() - os.stat(myfolder).st_mtime 
	if (curtime/3600) > 24:
		os.rmdir(myfolder)
		