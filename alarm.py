#!/usr/local/bin/python

# Created by Dan Arteaga

# This is the main alarm script

# Import required libraries
import sys,os,glob,subprocess
import signal,random,time


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
			if 'python_interpreter' in new_lines:
				python_interpreter = new_lines.split(" ")[1:][0]		
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
		
rf_list = []	
to_stop = True
for yt in range(1,100):
	new_look = 'rf_code_%s' %(yt)
	for new_lines in content:
		if new_look in new_lines:
			# Only select the name of the sensor
			rf_list.append(new_lines.split(" ")[1:][0].split(":")[1])
			to_stop = False
	if to_stop == True:
		break

# Import push notification library
if use_pushbullet == True:
	from pushbullet import Pushbullet
	try:
		for access_token in token_list:
			pushbullet_list.append(Pushbullet(access_token))
	except:
		use_pushbullet = 'RETEST'		

# To kill a process manually -> type 'top' to obtain pid then 'sudo kill pid'
# Kill all the current RF Sniffer instances!
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
	if 'RFSniffer' in line:
		pid = int(line.split(None, 1)[0])
		to_kill = "sudo kill %s" %(pid)
		os.system(to_kill)		
	
# Path to executables
send_script = "/home/pi/433Utils/RPi_utils/codesend"
rf_sniffer_script = "/home/pi/433Utils/RPi_utils/RFSniffer"

# Turn on RF Sniffer
p0 = subprocess.Popen(["sudo",rf_sniffer_script],preexec_fn=os.setsid)	
		
# Change to Desktop directory
os.chdir('/home/pi/Desktop')

# Motion_sound, when 0, will not allow any sound to play from speakers
os.system("echo -n 1 > txt_files/motion_sound.txt")
		
# These files are created when a magnetic, motion, or glass break sensor is activated	
os.chdir('/home/pi/Desktop/txt_files')
trigger_list = glob.glob("*trigger.txt*")
for file4 in trigger_list:
	to_del = "sudo rm /home/pi/Desktop/txt_files/%s" %(file4)
	os.system(to_del)
os.chdir('/home/pi/Desktop')		

# Continuously loop to determine if a magnetic, motion, or glass break sensor is activated	
looper = True
while looper == True:

	# Give the computer a small break
	time.sleep(0.2)

	# If there is a keybaord interrupt event, the following will not be performed
	try:
						
		# When a magnetic, motion, or glass break sensor is activated, the .txt files without 'state' are first created.
		# When a magnetic or motion sensor in particular is activated, the .txt files with 'state' are also created 
		#   temporarily for 10 seconds to prevent reactivation within this time period.
		# See RFSniffer.cpp in the /home/pi/433Utils/RPi_utils/ directory for more details
		os.chdir('/home/pi/Desktop/txt_files')	
		trigger_list = glob.glob("*trigger.txt*")
		see_file = False
		
		# If no .txt file created upon sensor activation exists, then this will not loop
		for file4 in trigger_list:
			see_state = False
			to_show = "/home/pi/Desktop/txt_files/%s" %(file4)
			to_show1 = "/home/pi/Desktop/txt_files/%s" %(file4)			
			os.system(to_show)
			
			if ('door' in to_show) or ('Door' in to_show) or ('DOOR' in to_show) or ('window' in to_show) or ('Window' in to_show) \
					or ('WINDOW' in to_show) or ('motion' in to_show) or ('Motion' in to_show) or ('MOTION' in to_show) or \
					('monoxide' in to_show) or ('MONOXIDE' in to_show) or ('Monoxide' in to_show):
				to_show1 = to_show1[:-4]
				to_show1 += '_state.txt'
				if os.path.isfile(to_show1) == True:
					see_state = True
			if see_state == False:	
				see_file = True	
		os.chdir('/home/pi/Desktop')		
		
		# If conditions are met indicating that a sensor is activated, see_file = True
		if see_file == True:	
		
			# Remove 'rf_code_X_' from the name
			underscore_counter = 0
			string_counter = 0			
			for character in trigger_list[0]:
				if character == '_':
					underscore_counter += 1
				string_counter += 1
				if underscore_counter == 3:
					break
			door = trigger_list[0][string_counter:]
			
			# Remove '_trigger.txt' from the name
			door = door[:-12]
			
			# Check to see what magnetic, motion, or glass break sensor was activated
			if ('door' in to_show) or ('Door' in to_show) or ('DOOR' in to_show):	
				volume = '40'
				sensor_type = 'door'
				
			elif ('window' in to_show) or ('Window' in to_show) or ('WINDOW' in to_show):	
				volume = '40'	
				sensor_type = 'window'				
				
			elif ('motion' in to_show) or ('Motion' in to_show) or ('MOTION' in to_show):	
				volume = '80'	
				sensor_type = 'motion'
				
			elif ('glass' in to_show) or ('Glass' in to_show) or ('GLASS' in to_show):	
				volume = '70'
				sensor_type = 'glass'

			elif ('monoxide' in to_show) or ('Monoxide' in to_show) or ('MONOXIDE' in to_show):	
				sensor_type = 'carbon_monoxide'			
			
			else:
				sensor_type = 'unknown'
				
			# Open armed.txt and check to see if system is armed
			if sensor_type == 'carbon_monoxide':
				armed_status == '-1'
				to_cmd = 'sudo %s /home/pi/Desktop/carbon_monoxide.py' %(python_interpreter)
				os.system(to_cmd)
			else:	
				with open("txt_files/armed.txt", "r") as fo:
					armed_status = fo.readline()
				fo.close()				
			
			# If system is disarmed, simply play sound if magnetic, motion, or glass break sensor is activated
			if (armed_status == "0"):
			
				# Open motion_sound.txt and check to see if sound can come from speakers
				with open("txt_files/motion_sound.txt", "r") as fo1:
					opened_file = fo1.readline()
				fo1.close()

				# If sound can come through speakers, perform following
				if opened_file != "0":					
				
					# Will check to see specifically if door or window is activated
					if sensor_type == 'door' or sensor_type == 'window':

						# If magnetic sensor is activated, play one of the 2 sounds available
						aba = random.randint(1,2)
						if aba == 1:
							abcd = "sound_files/back_to_the_future.mp3"
							myvol = int(volume)
						else:
							abcd = "sound_files/secret.mp3"
							myvol = int(volume) + 110 # This sound is more quiet so add volume				
						to_play = 'sudo -u pi mpg321 -g %s %s' %(myvol,abcd)	
						os.system(to_play)
						
					# Will check to see specifically if motion sensor is activated	
					if sensor_type != 'door' and sensor_type != 'window' and sensor_type == 'motion':

						# Play sound file for motion sensor event	
						myvol = int(volume)
						to_play = 'sudo -u pi mpg321 -g %s sound_files/pinkpanther.mp3' %(myvol)
						os.system(to_play)
					
					# Will check to see specifically if glas break sensor is activated	
					if sensor_type != 'door' and sensor_type != 'window' and sensor_type != 'motion' and sensor_type == 'glass':
		
						# Play one of the 4 sounds available
						aba = random.randint(1,4)
						abcd = "sound_files/Bird%s.mp3" %(aba)
						myvol = int(volume)
						to_play = 'sudo -u pi mpg321 -g %s %s' %(myvol,abcd)	
						os.system(to_play)
						
				# Reset triggered files	
				os.chdir('/home/pi/Desktop/txt_files')
				trigger_list = glob.glob("*trigger.txt*")
				for file4 in trigger_list:
					to_del = "sudo rm /home/pi/Desktop/txt_files/%s" %(file4)
					os.system(to_del)
				os.chdir('/home/pi/Desktop')	
				
			# If system is armed, however, prepare to sound siren
			if (armed_status == "1"):  	
			
				# Turn off all sound coming through speaker temporarily except for sound created below
				os.system("echo -n 0 > txt_files/motion_sound.txt")
									
				# Send text/email/pushbullet warning of sensor that is tripped				
				me_send = "sudo %s /home/pi/Desktop/sender.py %s" %(python_interpreter,door)
				
				# Use subprocess as this takes a few seconds to carry out
				p51 = subprocess.Popen(me_send, shell=True, stdout=subprocess.PIPE)			

				# Give the initial 30 second warning
				start_time1 = time.time()		
				out1 = 'sudo -u pi mpg321 -g %s sound_files/30_sec.mp3' %(volume)
				os.system(out1)
				twenty_sec = False
				ten_sec = False
				five_sec = False
				time.sleep(1)
				
				break_loop = False
				turn_on_siren = False
				while break_loop == False:
				
					# Open armed.txt and check to see if system still armed
					with open("txt_files/armed.txt", "r") as fo2:
						armed_status = fo2.readline()
					fo2.close()
				   
					# If the system is still armed, keep counting down
					if armed_status == "1":

						# Time is up!
						if (30 - (time.time() - start_time1) < 0) and (five_sec == True):
							turn_on_siren = True
							break_loop = True
							
						# 20 seconds left	
						elif twenty_sec == False and ((30 - (time.time() - start_time1)) <= 20):
							out1 = 'sudo -u pi mpg321 -g %s sound_files/20_sec.mp3' %(volume)
							os.system(out1)	
							twenty_sec = True
							
						# 10 seconds left	
						elif ten_sec == False and ((30 - (time.time() - start_time1)) <= 10) and twenty_sec == True:
							out1 = 'sudo -u pi mpg321 -g %s sound_files/10_sec.mp3' %(volume)
							os.system(out1)	
							ten_sec = True	
							
						# 5 seconds left	
						elif five_sec == False and ((30 - (time.time() - start_time1)) <= 5) and ten_sec == True:
							out1 = 'sudo -u pi mpg321 -g %s sound_files/5_sec.mp3' %(volume)
							os.system(out1)	
							five_sec = True	
							
						else:
							out1 = 'sudo -u pi mpg321 -g %s sound_files/Please_deactivate.mp3' %(volume)
							os.system(out1)							

						time.sleep(1)
						
					else:										
					
						break_loop = True						
				
				# Turn on siren if system still armed after 30 seconds!
				if armed_status == "1" and turn_on_siren == True:		
				
					if use_pushbullet == 'RETEST':
						try:
							for access_token in token_list:
								pushbullet_list.append(Pushbullet(access_token))
							use_pushbullet = True
						except:
							pass

					# When myfile.txt is created again when deactivate_system.sh is started, then siren will stop
					os.system("rm /home/pi/Desktop/txt_files/myfile.txt")					
								
					# Turn on siren played through the speakers, where -g 100 is the volume
					p5 = subprocess.Popen("sudo -u pi mpg321 -g 100 sound_files/alarm.mp3", shell=True, stdout=subprocess.PIPE)		

					# Turn on siren(s)
					to_siren = "sudo " + send_script + " %s" %(siren_on)
					os.system(to_siren)		

					# Send text/email/pushbullet warning of sensor that is tripped				
					if send_text == True:
						for my_number in text_list:
							to_send1 = 'echo "Siren activated" | mail -s "Alert" %s' %(my_number)
							os.system(to_send1)			

					if send_email_basic == True:
						for my_email in email_list:
							to_send1 = 'echo "Siren activated" | mail -s "Alert" %s' %(my_email)
							os.system(to_send1)

					if use_pushbullet == True:	
						try:
							for itir,pushme1 in enumerate(pushbullet_list):
								pushme1.push_note("Alert","Siren activated")	
								new_push = pushme1.get_pushes()
								
								# Save the identity of the push to delete after 2 days
								identity1 = new_push[0].get("iden")
								to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
								os.system(to_identity)	
						except:
							pass
						
					# Only turn on siren for six 30 second cycles (separated by 15 second pauses)
					time_counter = 1
					time_expired = False
					
					# Track time	
					begin_time = time.time()	
					siren_begin_time = time.time()
					
					# Begin loop
					siren_status = True				
					while siren_status == True:
					
						# Only turn on siren for six 30 second cycles (separated by 15 second pauses)
						if time_counter >= 4:
							time_expired = True
							break					

						# Check to see if file, which is created when siren deactivated, exists
						if os.path.isfile('/home/pi/Desktop/txt_files/myfile.txt') == True:
							break	

						# Check for changes in alarm status
						time.sleep(0.5)
						
						# Siren being played through speakers stops after 8 seconds
						if (time.time()-siren_begin_time) >= 10:
						
							# Turn on speaker siren again
							p5 = subprocess.Popen("sudo -u pi mpg321 -g 100 sound_files/alarm.mp3", shell=True, stdout=subprocess.PIPE)

							# Reset siren begin time	
							siren_begin_time = time.time()
						
						"""
						# Siren will automatically turn off after 30 seconds, pause for 15 seconds, 
						# then turn on for another 30 seconds to complete a cycle
						if (time.time()-begin_time) > 90:
						
							# Add another iteration of no intervention
							time_counter += 1
							
							# Turn on siren again
							to_siren = "sudo " + send_script + " %s" %(siren_on)
							os.system(to_siren)
						"""	
						
					# Kill the speaker siren sound
					p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
					out, err = p.communicate()
					for line in out.splitlines():
						if 'mpg321' in line:
							pid = int(line.split(None, 1)[0])
							to_kill = "sudo kill %s" %(pid)
							os.system(to_kill)							
						
					# Turn siren off if siren deactivated with deactivate_system.sh
					if time_expired == False:
						
						# Disarm the system
						os.system("sudo echo -n 0 > /home/pi/Desktop/txt_files/armed.txt")	
						
						# Turn off the sirens
						to_siren = "sudo " + send_script + " %s" %(siren_off)
						os.system(to_siren)
						os.system(to_siren)						
						os.system(to_siren)						
						os.system(to_siren)	
						os.system(to_siren)
						os.system(to_siren)
						os.system(to_siren)

					else:
						# Turn off the sirens
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

						if send_email_basic == True:
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

						if send_email_basic == True:
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
				
				# Reset triggered files	
				os.chdir('/home/pi/Desktop/txt_files')
				trigger_list = glob.glob("*trigger.txt*")
				for file4 in trigger_list:
					to_del = "sudo rm /home/pi/Desktop/txt_files/%s" %(file4)
					os.system(to_del)
				os.chdir('/home/pi/Desktop')						
				
				# Allow other sound to come from speakers again
				os.system("echo -n 1 > txt_files/motion_sound.txt")	
				
				# Remove file created when siren manually deactivated
				os.system("rm /home/pi/Desktop/txt_files/myfile.txt")					
					
				# Allow other sound to come from speakers again
				os.system("echo -n 1 > txt_files/motion_sound.txt")	
					
					
	except KeyboardInterrupt:
	
		# Reset triggered files	
		os.chdir('/home/pi/Desktop/txt_files')
		trigger_list = glob.glob("*trigger.txt*")
		for file4 in trigger_list:
			to_del = "sudo rm /home/pi/Desktop/txt_files/%s" %(file4)
			os.system(to_del)
		os.chdir('/home/pi/Desktop')	
		
		# Remove file created when siren manually deactivated
		os.system("rm /home/pi/Desktop/txt_files/myfile.txt")			
	
		# Kill RF Sniffer
		os.system("sudo kill %s" %(p0.pid, ))			
		break
