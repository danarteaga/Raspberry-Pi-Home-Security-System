#!/usr/local/bin/python

# Created by Dan Arteaga

# This script will update all relevant files and shut the system down
		

# Import required libraries
import sys,os,glob,re,fileinput
		
# Read the input_variable.txt file:
with open('input_variables.txt') as f:
	content = f.readlines()
content = [x.strip() for x in content]
		
# Read variables from the input_variable.txt file:		
for new_lines in content:
	try:
		if new_lines[0] != '#':
			if 'ip_address' in new_lines:
				ip_address = new_lines.split(" ")[1:][0]
			if 'domain_name' in new_lines:
				domain_name = new_lines.split(" ")[1:][0]		
			if 'python_interpreter' in new_lines:
				python_interpreter = new_lines.split(" ")[1:][0]		
			if 'video_port' in new_lines:
				video_port = new_lines.split(" ")[1:][0]	
			if 'control_port' in new_lines:
				control_port = new_lines.split(" ")[1:][0]	
			if 'rotate_camera' in new_lines:
				rotate_camera = new_lines.split(" ")[1:][0]	
			if 'video_credentials' in new_lines:
				video_credentials = new_lines.split(" ")[1:][0]		
			if 'insync_email' in new_lines:
				insync_email = new_lines.split(" ")[1:][0]	
			if 'python_interpreter' in new_lines:
				python_interpreter = new_lines.split(" ")[1:][0]			
	except:
		pass	
		
# Update the activate_system.sh file
only_once = False
for i, line in enumerate(fileinput.input('activate_system.sh', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		to_out = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/start"' %(ip_address,control_port)
		sys.stdout.write(to_out)
		sys.stdout.write('\n')	
		only_once = True
	else:
		sys.stdout.write(line.replace('\r', ''))	

# Update the deactivate_system.sh file
only_once = False
for i, line in enumerate(fileinput.input('deactivate_system.sh', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		to_out = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/pause"' %(ip_address,control_port)
		sys.stdout.write(to_out)	
		sys.stdout.write('\n')
		only_once = True		
	else:
		sys.stdout.write(line.replace('\r', ''))	
		
# Update the pause_motion.sh file
only_once = False
for i, line in enumerate(fileinput.input('pause_motion.sh', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		to_out = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/pause"' %(ip_address,control_port)
		sys.stdout.write(to_out)	
		sys.stdout.write('\n')
		only_once = True		
	else:
		sys.stdout.write(line.replace('\r', ''))	

# Update the start_motion.sh file
only_once = False
for i, line in enumerate(fileinput.input('start_motion.sh', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		to_out = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/start"' %(ip_address,control_port)
		sys.stdout.write(to_out)	
		sys.stdout.write('\n')
		only_once = True		
	else:
		sys.stdout.write(line.replace('\r', ''))			
		
# Update the check_system.sh file
only_once = False
only_once1 = False
for i, line in enumerate(fileinput.input('check_system.sh', inplace=1)):	
	if '/usr/bin/wget' in line and line[0] != '#' and 'start' in line and only_once == False:
		to_out = '  /usr/bin/wget -q -O /dev/null "%s:%s/0/detection/start"' %(ip_address,control_port)
		sys.stdout.write(to_out)
		sys.stdout.write('\n')
		only_once = True
	elif '/usr/bin/wget' in line and line[0] != '#' and 'pause' in line and only_once1 == False:
		to_out = '    /usr/bin/wget -q -O /dev/null "%s:%s/0/detection/pause"' %(ip_address,control_port)
		sys.stdout.write(to_out)
		sys.stdout.write('\n')	
		only_once1 = True
	else:
		sys.stdout.write(line.replace('\r', ''))		

# Update the vacation_return.py file
only_once = False
for i, line in enumerate(fileinput.input('vacation_away.py', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		abc_123 = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/start"' %(ip_address,control_port)
		to_out = "os.system('" + abc_123 + "')"
		sys.stdout.write(to_out)	
		sys.stdout.write('\n')
		only_once = True		
	else:
		sys.stdout.write(line.replace('\r', ''))			

# Update the vacation_return.py file
only_once = False
for i, line in enumerate(fileinput.input('vacation_return.py', inplace=1)):
	if '/usr/bin/wget' in line and line[0] != '#' and only_once == False:
		abc_123 = '/usr/bin/wget -q -O /dev/null "%s:%s/0/detection/pause"' %(ip_address,control_port)
		to_out = "os.system('" + abc_123 + "')"
		sys.stdout.write(to_out)	
		sys.stdout.write('\n')
		only_once = True		
	else:
		sys.stdout.write(line.replace('\r', ''))			
		
# Read user-supplied RF codes		
rf_name_list = []	
rf_code_list = []
rf_code_list_temp = []
to_stop = True
for yt in range(0,100):
	new_look = 'rf_code_%s' %(yt)
	for new_lines in content:
		if new_look in new_lines and new_lines[0] != "#":
			# Only select the name of the sensor
			rf_now = new_lines.split(" ")[0]
			rf_now += '_'
			rf_now += new_lines.split(" ")[1:][0].split(":")[1]
			rf_name_list.append(rf_now)
			rf_code_list.append(new_lines.split(" ")[1:][0].split(":")[0])
			rf_code_list_temp.append(new_lines.split(" ")[1:][0].split(":")[0])
			to_stop = False
	if to_stop == True:
		break

# Update the motion-mmalcam.conf file
for i, line in enumerate(fileinput.input('motion-mmalcam.conf', inplace=1)):
	if 'rotate' in line and line[0] != '#':
		temp_rotate = line.split(" ")[1:][0]
		sys.stdout.write(line.replace(temp_rotate, rotate_camera))
		sys.stdout.write('\n')
	elif 'stream_authentication' in line and line[0] != '#':
		temp_auth = line.split(" ")[1:][0]
		sys.stdout.write(line.replace(temp_auth, video_credentials))
		sys.stdout.write('\n')	
	elif 'stream_port' in line and line[0] != '#':
		temp_port = line.split(" ")[1:][0]
		sys.stdout.write(line.replace(temp_port, video_port))
		sys.stdout.write('\n')
	elif 'webcontrol_port' in line and line[0] != '#':
		temp_port = line.split(" ")[1:][0]
		sys.stdout.write(line.replace(temp_port, control_port))
		sys.stdout.write('\n')			
	else:
		sys.stdout.write(line.replace('\r', ''))	
		
# Update the automate_tasks.txt file
for i, line in enumerate(fileinput.input('automate_tasks.txt', inplace=1)):
	if '-exec' in line and line[0] != '#':
		newline1 = '31 1 * * * sudo find /home/pi/%s/Camera -type d -ctime +30 -exec rm -rf {} \; >/dev/null 2>&1' %(insync_email)
		sys.stdout.write(newline1)
		sys.stdout.write('\n')	
	else:
		sys.stdout.write(line.replace('\r', ''))			
		
# Read the RFSniffer.cpp file
with open('/home/pi/433Utils/RPi_utils/RFSniffer.cpp') as f:
	content = f.readlines()
	content = [x.strip() for x in content]
	
# Make sure the RF codes aren't already in the RFSniffer.cpp file
used_code_indices = []
for xt,new_code in enumerate(rf_code_list_temp):
	for new_line in content:
		if new_code in new_line:
			used_code_indices.append(xt)	
	
# Remove RF codes that are already in the RFSniffer.cpp file			
for index in sorted(used_code_indices, reverse=True):
	del rf_code_list_temp[index]
		
# If changes are detected copy over the original file and re-write	
to_loop = 0
changes = False	
if len(rf_code_list_temp) > 0:

	os.system('sudo cp /home/pi/433Utils/RPi_utils/RFSniffer_original.cpp /home/pi/433Utils/RPi_utils/RFSniffer.cpp')
	
	# Read the RFSniffer.cpp file and place new command in place of //new_line if not already there
	for i, line in enumerate(fileinput.input('/home/pi/433Utils/RPi_utils/RFSniffer.cpp', inplace=1)):

		if to_loop >= len(rf_code_list):
			sys.stdout.write(line.replace('\r', ''))
		elif '//new_line' in line:
			changes = True
			temp_state = 'if (value == %s) {system("%s /home/pi/Desktop/txt_files/%s.py");}' %(rf_code_list[to_loop],python_interpreter,rf_name_list[to_loop])
			sys.stdout.write(line.replace('//new_line', temp_state))
			to_loop += 1
		else:
			sys.stdout.write(line.replace('\r', ''))	
		
# Compile the RFSniffer.cpp file if changes were made
if changes == True:
	os.chdir('/home/pi/433Utils/RPi_utils')
	os.system('sudo make')
	os.chdir('/home/pi/Desktop')	

# Create the files used to control sensor activation
if changes == True:

	# Remove the python scripts in the /home/pi/Desktop/txt_files folder
	os.system('sudo rm /home/pi/Desktop/txt_files/*rf_code*')
	
	# Create the new python scripts
	import shutil
	for iter1,my_namer in enumerate(rf_name_list):
	
		if iter1 == 0:
		
			full_name_orig = '/home/pi/Desktop/txt_files/rf_code_0_Disarm_System.py'	
			shutil.copyfile('trigger_disarm.py',full_name_orig)	

		else:

			full_name_orig = '/home/pi/Desktop/txt_files/trigger_state.py'	
			shutil.copyfile('trigger_state.py',full_name_orig)
			
			new_namer = my_namer + '.py'	
			full_name_new = '/home/pi/Desktop/txt_files/%s' %(new_namer)
			os.rename(full_name_orig,full_name_new)
			
			# Update the python file
			for i, line in enumerate(fileinput.input(full_name_new, inplace=1)):
				if 'state' in line:
					to_add = my_namer + '_state'
					sys.stdout.write(line.replace('state', to_add))
				elif 'trigger' in line:
					to_add = my_namer + '_trigger'
					sys.stdout.write(line.replace('trigger', to_add))	
				else:
					sys.stdout.write(line.replace('\r', ''))
				
# Update the interpreter for each of the python files if needed
python_scripts = glob.glob("*.py*")
need_change = False
for py_file in python_scripts:	
	
	for i, line in enumerate(fileinput.input(py_file, inplace=1)):
		if line[0:3] == '#!/':
			if python_interpreter in line:
				sys.stdout.write(line.replace('\r', ''))
			else:
				need_change = True
				new_line = '#!%s' %(python_interpreter)
				sys.stdout.write(new_line)
				sys.stdout.write('\n')	
		else:
			sys.stdout.write(line.replace('\r', ''))				
	
	# If the first file doesn't need an update, none of them will
	if need_change == False:
		break
		
# Also update the scripts in /txt_files if needed
os.chdir('/home/pi/Desktop/txt_files')		

# Update the interpreter for each of the python files if needed
python_scripts = glob.glob("*.py*")
need_change = False
for py_file in python_scripts:	
	
	for i, line in enumerate(fileinput.input(py_file, inplace=1)):
		if line[0:3] == '#!/':
			if python_interpreter in line:
				sys.stdout.write(line.replace('\r', ''))
			else:
				need_change = True
				new_line = '#!%s' %(python_interpreter)
				sys.stdout.write(new_line)
				sys.stdout.write('\n')	
		else:
			sys.stdout.write(line.replace('\r', ''))	

	# If the first file doesn't need an update, none of them will
	if need_change == False:
		break	

# Update the monoxide file to wait 5 minutes after running rather than 10 seconds
types = ("*monoxide*","*Monoxide*","*MONOXIDE*")
python_scripts = []
for files in types:
	python_scripts.extend(glob.glob(files))
	
for py_file in python_scripts:	
	
	for i, line in enumerate(fileinput.input(py_file, inplace=1)):
		if 'time.sleep' in line and '#Keep' not in line:
			if 'time.sleep(500)' in line:
				sys.stdout.write(line.replace('\r', ''))
			else:
				new_line = '	time.sleep(500)'
				sys.stdout.write(new_line)
				sys.stdout.write('\n')	
		else:
			sys.stdout.write(line.replace('\r', ''))			

# Change back to the Desktop directory
os.chdir('/home/pi/Desktop')								
	
# Shutdown the system finally!
os.system('sudo shutdown -h now')
	