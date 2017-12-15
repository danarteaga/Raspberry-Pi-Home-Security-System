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
			if 'video_credentials' in new_lines:
				video_credentials = new_lines.split(" ")[1:][0]	
				
	except:
		pass
	

my_camera = "%s:%s" %(domain_name,video_port)	

# Import required libraries
import os,sys,time,random,string,fileinput,subprocess,glob


# Send email to each recipient
email_body = 'Dear family and friends,\n\nWe are now back from our vacation. Thank you for your vigilance!'
email_body += '\n\nBest,\nDan'

for my_email in email_list:		
	to_send1 = 'sudo echo "%s" | mail -s "Back from our vacation" %s' %(email_body,my_email)
	os.system(to_send1)		
	
	
for my_number in text_list:
	to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %('We are back from our vacation!','',my_number)
	os.system(to_send1)			
	
	
# Update the motion-mmalcam.conf file
for i, line in enumerate(fileinput.input('motion-mmalcam.conf', inplace=1)):
	if 'stream_authentication' in line and line[0] != '#':
		temp_credentials = line.split(" ")[1:][0]
		sys.stdout.write(line.replace(temp_credentials,video_credentials))
		sys.stdout.write('\n')	
	else:
		sys.stdout.write(line.replace('\r', ''))		
	
# Restart the motion daemon
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
	if 'motion' in line:
		pid = int(line.split(None, 1)[0])
		to_kill = "sudo kill %s" %(pid)
		os.system(to_kill)	
p0 = subprocess.Popen(["sudo","/home/pi/Desktop/motion","-n","-c","/home/pi/Desktop/motion-mmalcam.conf"],preexec_fn=os.setsid)			
