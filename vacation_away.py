#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will send notifications as a subprocess

import os

# Load data from the input_variable.txt file:
with open('input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
email_list = []
text_list = []
email_list_vacation = []
text_list_vacation = []
token_list = []	
pushbullet_list = []	
user_id_list = []
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
			if 'vacation_number' in new_lines:
				text_list_vacation.append(new_lines.split(" ")[1:][0])					
			if 'send_email' in new_lines:
				send_email = new_lines.split(" ")[1:][0]
			if 'email_basic' in new_lines:
				send_email_basic = new_lines.split(" ")[1:][0]
			if 'my_email' in new_lines:
				email_list.append(new_lines.split(" ")[1:][0])		
			if 'vacation_email' in new_lines:
				email_list_vacation.append(new_lines.split(" ")[1:][0])					
			if 'siren_on' in new_lines:
				siren_on = new_lines.split(" ")[1:][0]
			if 'siren_off' in new_lines:
				siren_off = new_lines.split(" ")[1:][0]
			if 'domain_name' in new_lines:
				domain_name = new_lines.split(" ")[1:][0]
			if 'video_port' in new_lines:
				video_port = new_lines.split(" ")[1:][0]	
			if 'user_id' in new_lines:
				user_id_list.append(new_lines.split(" ")[1:][0])	
			if 'emergency_contact' in new_lines:
				emergency_contact = new_lines.split(" ")[1:]					
	except:
		pass
	
pronoun = ['I','my','I','me']	
if len(user_id_list) > 1:
	pronoun = ['We','our','we','us']
	
if len(user_id_list) == 1:	
	final_user_id = user_id_list[0]
elif len(user_id_list) == 2:
	final_user_id = " and ".join(user_id_list)
else:
	final_user_id = '{}, and {}'.format(', '.join(listed[:-1]), listed[-1])	

my_camera = "%s:%s" %(domain_name,video_port)	

# Store vacation settings
os.system("echo -n 1 > txt_files/vacation.txt")

# Import required libraries
import os,sys,time,random,string,fileinput,subprocess,glob

# Generate a random password
random_pass = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))

# Send email to each recipient
email_body = 'Dear family and friends,\n\n'
email_body += '%s will be going out of town today, and wanted to invite you' %(pronoun[0])
email_body += ' to monitor %s home remotely. To do so, %s will provide you with exclusive access to %s 24/7 live camera' %(pronoun[1],pronoun[2],pronoun[1])
email_body += ' feed (see below for details). In addition, you will receive new motion images via email. The vast'
email_body += ' majority of these images will be false positives (e.g. a change in lighting). However, if you do'
email_body += ' see someone in the house that you do NOT recognize (either on the 24/7 live camera feed or in the image'
email_body += ' sent to your email), please consider contacting the contact listed below:\n\n'
email_body += '%s' %(" ".join(emergency_contact))
email_body += '\n\n24/7 Live Camera Feed:\n'
email_body += 'Website = %s\nUsername = guest\nTemporary password = %s' %(my_camera,random_pass)
email_body += '\n\nYou will receive another text and email notification upon %s return.' %(pronoun[1])
email_body += ' Please contact %s if you have any further questions.' %(pronoun[3])
email_body += '\n\nBest,\n%s' %(final_user_id)

for my_email in email_list:		
	to_send1 = 'sudo echo "%s" | mail -s "Invitation to monitor home while on vacation" %s' %(email_body,my_email)
	os.system(to_send1)	

for my_email in email_list_vacation:		
	to_send1 = 'sudo echo "%s" | mail -s "Invitation to monitor home while on vacation" %s' %(email_body,my_email)
	os.system(to_send1)			

for my_number in text_list:
	to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %('Going out of town! Check your email for details.','',my_number)
	os.system(to_send1)		

for my_number in text_list_vacation:
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

time.sleep(5)			
p0 = subprocess.Popen(["sudo","/home/pi/Desktop/motion","-n","-c","/home/pi/Desktop/motion-mmalcam.conf",">/dev/null","2>&1"],preexec_fn=os.setsid)

# Make sure that motion detection is on
os.system('/usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/start"')
