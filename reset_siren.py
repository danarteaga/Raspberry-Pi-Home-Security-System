#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will reset the siren

# Load data from the input_variable.txt file:
with open('input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
email_list = []
text_list = []
token_list = []	
pushbullet_list = []	
for new_lines in content:
	try:
		if new_lines[0] != '#':	
			if 'use_pushbullet' in new_lines:
				use_pushbullet = new_lines.split(" ")[1:][0]
			if 'access_token' in new_lines:
				token_list.append(new_lines.split(" ")[1:][0])
			if 'send_text' in new_lines:
				send_text = new_lines.split(" ")[1:][0]		
			if 'my_number' in new_lines:
				text_list.append(new_lines.split(" ")[1:][0])	
			if 'send_email' in new_lines:
				send_email = new_lines.split(" ")[1:][0]
			if 'email_basic' in new_lines:
				send_email_basic = new_lines.split(" ")[1:][0]
			if 'my_email' in new_lines:
				email_list.append(new_lines.split(" ")[1:][0])			
			if 'siren_on' in new_lines:
				siren_on = new_lines.split(" ")[1:][0]
			if 'siren_off' in new_lines:
				siren_off = new_lines.split(" ")[1:][0]
			if 'domain_name' in new_lines:
				domain_name = new_lines.split(" ")[1:][0]
			if 'video_port' in new_lines:
				video_port = new_lines.split(" ")[1:][0]
	except:
		pass				

# Import required libraries
import sys,os

# Path to executable to manually send RF code
send_script = "/home/pi/433Utils/RPi_utils/codesend"		

# Turn off siren(s)
to_siren = "sudo " + send_script + " %s" %(siren_off)
os.system(to_siren)
os.system(to_siren)						
os.system(to_siren)						
os.system(to_siren)	
os.system(to_siren)
os.system(to_siren)
os.system(to_siren)	
