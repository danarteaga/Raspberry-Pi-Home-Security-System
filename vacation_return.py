#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will send notifications as a subprocess

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
				emergency_contact = new_lines.split(" ")[1:][0]	
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
os.system("echo -n 0 > txt_files/vacation.txt")

# Import required libraries
import os,sys,time,random,string,fileinput,subprocess,glob


# Send email to each recipient
email_body = 'Dear family and friends,\n\n%s are now back from %s vacation. Thank you for your vigilance!' %(pronoun[0],pronoun[1])
email_body += '\n\nBest,\n%s' %(final_user_id)

for my_email in email_list:		
	to_send1 = 'sudo echo "%s" | mail -s "Back from our vacation" %s' %(email_body,my_email)
	os.system(to_send1)		
	
for my_email in email_list_vacation:		
	to_send1 = 'sudo echo "%s" | mail -s "Back from our vacation" %s' %(email_body,my_email)
	os.system(to_send1)			
		
for my_number in text_list:
	to_send1 = 'sudo echo "%s" | mail -s "%s" %s' %('We are back from our vacation!','',my_number)
	os.system(to_send1)	

for my_number in text_list_vacation:
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
	
# Make sure that motion detection is off
os.system('/usr/bin/wget -q -O /dev/null "192.168.1.80:8086/0/detection/pause"')

# Restart the system
os.system('sudo reboot.py')
