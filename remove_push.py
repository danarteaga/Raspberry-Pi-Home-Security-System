#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will periodically delete push notifications after 2 days
# The periodicity is determined by the cronjob command

# Import library
import os

# Change to the Desktop directory
os.chdir('/home/pi/Desktop')

# Load data from the input_variable.txt file:
with open('/home/pi/Desktop/input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
token_list = []	
pushbullet_list = []	
for new_lines in content:
	try:
		if new_lines[0] != '#':	
			if 'use_pushbullet' in new_lines:
				use_pushbullet = new_lines.split(" ")[1:][0]
			if 'access_token' in new_lines:
				token_list.append(new_lines.split(" ")[1:][0])
	except:
		pass
		
if use_pushbullet == 'True' or use_pushbullet == 'true' or use_pushbullet == 'TRUE':
	use_pushbullet = True	
	

if use_pushbullet == True:

	# Import required libraries
	import sys
	import time
	import numpy as N

	# Import push notification library
	from pushbullet import Pushbullet
	for access_token in token_list:
		pushbullet_list.append(Pushbullet(access_token))

	for itir,pushme1 in enumerate(pushbullet_list):
	
		# Save the identity of the push to delete after 2 days
		bad_indices = []
		bad_identities = []

		to_load = '/home/pi/Desktop/txt_files/push_list%s.txt' %(itir)
		numpytxt = N.loadtxt(to_load,dtype='str')
		
		# First make sure all pushes are in the .txt file, else add them first
		new_push = pushme1.get_pushes()
		for xtt in range(len(new_push)):
			new_iden = new_push[xtt].get("iden")
			if new_iden not in numpytxt[:,0]:
				to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(new_iden, time.time(),itir)
				os.system(to_identity)
				
		# Reload the .txt file		
		to_load = '/home/pi/Desktop/txt_files/push_list%s.txt' %(itir)
		numpytxt = N.loadtxt(to_load,dtype='str')
		
		# If only one line exists, then have to go a different route
		multiple = True
		try:
			print numpytxt.shape[1]
		
			for index,line in enumerate(numpytxt):
				new_time = time.time() - N.float(line[1])
				# Check to see if 2 days have passed; time is in seconds:
				if new_time > 172800:
					bad_indices.append(index)	
					bad_identities.append(line[0])
		except:
			multiple = False
			new_time = time.time() - N.float(numpytxt[1])
			# Check to see if 2 days have passed; time is in seconds:
			if new_time > 172800:
				bad_indices.append(0)	
				bad_identities.append(numpytxt[0])			
				
		# Delete pushes over 2 days old
		for ident in bad_identities:
			try:
				pushme1.delete_push(ident)	
			except:
				pass

		# Save the new text file
		if multiple == True:
			new_numpytxt = N.delete(numpytxt,bad_indices,axis=0)
		else:
			new_numpytxt = N.delete(numpytxt,[0,1],axis=0)		

		# Save new txt file
		N.savetxt(to_load, new_numpytxt, delimiter=" ", fmt="%s")
