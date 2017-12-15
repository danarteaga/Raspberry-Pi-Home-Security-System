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
	

my_camera = "%s:%s" %(domain_name,video_port)	

# Import required libraries
import os,sys,time,random,string,fileinput,subprocess,glob

# Generate a random password
random_pass = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))

# Send email to each recipient
email_body = 'Dear family and friends,\n\nWe will be going out of town today, and wanted to invite you'
email_body += ' to monitor our home remotely. To do so, we will provide you with exclusive access to our 24/7 live camera'
email_body += ' feed (see below for details). In addition, you will receive new motion images via email. The vast'
email_body += ' majority of these images will be false positives (e.g. a change in lighting). However, if you do'
email_body += ' see someone in the house that you do NOT recognize (either on the 24/7 live camera feed or in the image'
email_body += ' sent to your email), please consider contacting local authorities as below:\n\n'
email_body += 'Charlottesville Police:\n(434) 970-3280.\n\n24/7 Live Camera Feed:\n'
email_body += 'Website = %s\nUsername = guest\nTemporary password = %s' %(my_camera,random_pass)
email_body += '\n\nYou will receive another text and email notification upon our return. Please contact me if you have any further questions.'
email_body += '\n\nBest,\nDan'

for my_email in email_list:		
	to_send1 = 'sudo echo "%s" | mail -s "Invitation to monitor home while on vacation" %s' %(email_body,my_email)
	os.system(to_send1)		
	

for my_number in text_list:
	to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %('Going out of town! Check your email for details.','',my_number)
	os.system(to_send1)			
	
	
# Update the motion-mmalcam.conf file
for i, line in enumerate(fileinput.input('motion-mmalcam.conf', inplace=1)):
	if 'stream_authentication' in line and line[0] != '#':
		temp_credentials = line.split(" ")[1:][0]
		new_credentials = 'guest:%s' %(random_pass)
		sys.stdout.write(line.replace(temp_credentials,new_credentials))
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