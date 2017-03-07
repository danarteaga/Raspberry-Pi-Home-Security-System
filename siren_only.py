#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will sound the siren manually


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
import sys,os
import time,subprocess

# Remove file created when siren manually deactivated
os.system("rm /home/pi/Desktop/txt_files/myfile.txt")

# Import push notification library
if use_pushbullet == True:
	from pushbullet import Pushbullet
	for access_token in token_list:
		pushbullet_list.append(Pushbullet(access_token))

# Path to executable to manually send RF code
send_script = "/home/pi/433Utils/RPi_utils/codesend"

# Arm the system 
os.system("sudo echo -n 1 > /home/pi/Desktop/txt_files/armed.txt")

# Send text/email/pushbullet notification that siren manually armed		
if send_text == True:
	for my_number in text_list:
		to_send1 = 'echo "Siren manually activated" | mail -s "Alert" %s' %(my_number)
		os.system(to_send1)			

if send_email == True:		
	for my_email in email_list:
		to_send1 = 'echo "Siren manually activated" | mail -s "Alert" %s' %(my_email)
		os.system(to_send1)

if use_pushbullet == True:
	for itir,pushme1 in enumerate(pushbullet_list):		
		pushme1.push_note("Alert","Siren manually activated")	
		new_push = pushme1.get_pushes()
		
		# Save the identity of the push to delete after 2 days
		identity1 = new_push[0].get("iden")
		to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
		os.system(to_identity)			

# Turn on speaker siren at a volume of 100
p5 = subprocess.Popen("sudo -u pi mpg321 -g 100 sound_files/alarm.mp3", shell=True, stdout=subprocess.PIPE)

# Turn on the siren(s)
to_run1 = "sudo " + send_script + " %s" %(siren_on)
os.system(to_run1)
	
# Only turn on siren for six 30 second cycles (separated by 15 second pauses)
time_counter = 1

# Track time
begin_time = time.time()
siren_begin_time = time.time()
time_expired = False

# Begin loop
siren_status = True
while siren_status == True and os.path.isfile('/home/pi/Desktop/txt_files/myfile.txt') == False:

	# Only turn on siren for six 30 second cycles (separated by 15 second pauses)
	if time_counter >= 4:
		time_expired = True
		break		

	# Delay by 1/2 second before rechecking
	time.sleep(0.5)
	
	# Check to see if file, which is created when siren deactivated, exists
	if os.path.isfile('/home/pi/Desktop/txt_files/myfile.txt') == True:
		break		
	
	# Siren played through speakers stops after 8 seconds
	if (time.time()-siren_begin_time) >= 10:
	
		# Turn on speaker siren
		p5 = subprocess.Popen("sudo -u pi mpg321 -g 100 sound_files/alarm.mp3", shell=True, stdout=subprocess.PIPE)

		# Reset siren begin time	
		siren_begin_time = time.time()
		
	# Check to see if file, which is created when siren deactivated, exists
	if os.path.isfile('/home/pi/Desktop/txt_files/myfile.txt') == True:
		break			
							
	# Siren will automatically turn off after 30 seconds, pause for 15 seconds, 
	# then turn on for another 30 seconds to complete a cycle
	if (time.time()-begin_time) > 90:
	
		# Add another iteration of no intervention
		time_counter += 1
		
		# Turn on siren
		to_run1 = "sudo " + send_script + " %s" %(siren_on)
		os.system(to_run1)
		
# Kill the speaker siren 
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
	if 'mpg321' in line:
		pid = int(line.split(None, 1)[0])
		to_kill = "sudo kill %s" %(pid)
		os.system(to_kill)			

# Turn off siren(s)
to_siren = "sudo " + send_script + " %s" %(siren_off)
os.system(to_siren)
os.system(to_siren)						
os.system(to_siren)						
os.system(to_siren)	
os.system(to_siren)
os.system(to_siren)
os.system(to_siren)	

# Send text notifications about event closure
if time_expired == False:

	# Send text/email/pushbullet warning if sensor that is tripped				
	if send_text == True:
		for my_number in text_list:
			to_send1 = 'echo "Siren manually turned off" | mail -s "Alert" %s' %(my_number)
			os.system(to_send1)			

	if send_email == True:		
		for my_email in email_list:
			to_send1 = 'echo "Siren manually turned off" | mail -s "Alert" %s' %(my_email)
			os.system(to_send1)

	if use_pushbullet == True:	
		for itir,pushme1 in enumerate(pushbullet_list):
			pushme1.push_note("Alert","Siren manually turned off")		
			new_push = pushme1.get_pushes()
			
			# Save the identity of the push to delete after 2 days
			identity1 = new_push[0].get("iden")
			to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
			os.system(to_identity)			

else:

	# Send text/email/pushbullet warning if sensor that is tripped				
	if send_text == True:
		for my_number in text_list:
			to_send1 = 'echo "Siren turned off after 5 minutes" | mail -s "Alert" %s' %(my_number)
			os.system(to_send1)			

	if send_email == True:	
		for my_email in email_list:
			to_send1 = 'echo "Siren turned off after 5 minutes" | mail -s "Alert" %s' %(my_email)
			os.system(to_send1)

	if use_pushbullet == True:	
		for itir,pushme1 in enumerate(pushbullet_list):
			pushme1.push_note("Alert","Siren turned off after 5 minutes")	
			new_push = pushme1.get_pushes()
			
			# Save the identity of the push to delete after 2 days
			identity1 = new_push[0].get("iden")
			to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
			os.system(to_identity)			
			
	
# Remove file created when siren manually deactivated
os.system("echo 'Test' > /home/pi/Desktop/txt_files/myfile.txt")
