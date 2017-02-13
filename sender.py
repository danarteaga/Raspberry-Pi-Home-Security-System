#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will send notifications as a subprocess

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
	

if use_pushbullet == 'True' or use_pushbullet == 'true' or use_pushbullet == 'TRUE':
	use_pushbullet = True	
else:
	use_pushbullet = False	
if send_text == 'True' or send_text == 'true' or send_text == 'TRUE':
	send_text = True
else:
	send_text = False		
if send_email == 'True' or send_email == 'true' or send_email == 'TRUE':
	send_email = True	
else:
	send_email = False	
if send_email_basic == 'True' or send_email_basic == 'true' or send_email_basic == 'TRUE':
	send_email_basic = True	
else:
	send_email_basic = False			
	
my_camera = "%s:%s" %(domain_name,video_port)	

# Import required libraries
import os,sys,time

# Import push notification library
if use_pushbullet == True:
	from pushbullet import Pushbullet
	for access_token in token_list:
		pushbullet_list.append(Pushbullet(access_token))

# Import arguments
door_to_show = sys.argv[1]

# Remove all '_' from the name
door_to_show.replace('_',' ')

# Send update
if use_pushbullet == True:
	for itir,pushme1 in enumerate(pushbullet_list):
		pushme1.push_link(door_to_show,my_camera)
		new_push = pushme1.get_pushes()
		
		# Save the identity of the push to delete after 2 days
		identity1 = new_push[0].get("iden")
		to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
		os.system(to_identity)			
		
if send_email_basic == True:
	for my_email in email_list:		
		to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %(my_camera,door_to_show,my_email)
		os.system(to_send1)		
		
if send_text == True:
	for my_number in text_list:
		to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %(my_camera,door_to_show,my_number)
		os.system(to_send1)			
