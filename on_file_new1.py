#!/usr/local/bin/python

# Created by Dan Arteaga

# This script manages the images that are collected by motion

# Load data from the input_variable.txt file:
with open('/home/pi/Desktop/input_variables.txt') as f:
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
			if 'camera_name' in new_lines:
				camera_name = new_lines.split(" ")[1:][0]			
			if 'insync_email' in new_lines:
				insync_email = new_lines.split(" ")[1:][0]		
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

# Remove all '_' from the name
camera_name = camera_name.replace('_',' ')	

# Import required libraries
import os,glob,datetime,time
import sys,subprocess
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

# The following functions are used to compare consecutive images to look for motion
def my_function(file1,file2):
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = to_grayscale(imread(file1).astype(float))
    img2 = to_grayscale(imread(file2).astype(float))
    # compare 2 images
    n_m, n_0 = compare_images(img1, img2)
    #print "Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size
    #print "Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size
    return n_m
	
def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng
	
# Import push notification library
if use_pushbullet == True:
	from pushbullet import Pushbullet
	try:
		for access_token in token_list:
			pushbullet_list.append(Pushbullet(access_token))
	except:
		use_pushbullet = False
	
# Import arguments sent to this script
new_fold = sys.argv[1]

# Move to temporary Camera directory
to_change = '/home/pi/Desktop/Camera_%s' %(new_fold)
os.chdir(to_change)

# Create name of new folder based on current date and time
today = datetime.date.today()
folder = today.strftime('%y.') + today.strftime('%m.') + today.strftime('%d')

# Create this new directory if one is not already present 
directory_me = '/home/pi/%s/Camera/%s' %(insync_email,folder)
if os.path.exists(directory_me):
	pass
else:
	mkdir1 = 'sudo mkdir -p %s' %(directory_me)
	os.system(mkdir1)
	
# Identify the filenames for the current motion event
jpg_files = sorted(glob.glob('*jpg'), reverse=False)
new_file_name = jpg_files[0]

# Move the jpg file to the insync directory
to_move1 = 'sudo cp %s %s' %(new_file_name,directory_me) 
os.system(to_move1)

# Now rename all files for simplicity
for xt,my_file1 in enumerate(jpg_files):
	to_do = 'sudo mv %s image_' %(my_file1)
	to_do += '%05d' %(xt)
	to_do += '.jpg >/dev/null 2>&1'
	os.system(to_do)
	
# Resort files based upon these new names	
jpg_files = sorted(glob.glob('*jpg'), reverse=False)	

# Create avi (video) file by using ffmpeg - msmpeg4?
to_avi = "sudo ffmpeg -framerate 5 -i 'image_%05d.jpg' -vcodec mpeg4" 
to_avi += " %s.avi" %(new_file_name[:-4])
#subprocess.Popen(to_avi, shell=True, stdout=subprocess.PIPE)
os.system(to_avi)
	
# Determine the name of the last jpeg file to use as a reference for motion comparisons	
last_jpg_file = jpg_files[len(jpg_files)-1]

# Determine the frame with the most motion, reviewing every 10 frames to save time
diff_jpg = []
max_value = 0
motion_iter = 0
for iter in xrange(0,len(jpg_files),10):
	temp_val = my_function(last_jpg_file,jpg_files[iter])
	if temp_val > max_value:
		max_value = temp_val
		motion_iter = iter
	
# Middle image will actually be the frame with the most motion	
middle_image = jpg_files[int(motion_iter)]	

# Rename middle image 
to_name = 'sudo cp %s %s' %(middle_image,new_file_name)
os.system(to_name)

# Send image as push notification	
new_motion = "New Motion in %s" %(camera_name)
if use_pushbullet == True:
	for itir,pushme1 in enumerate(pushbullet_list):
		with open(new_file_name, "rb") as picture:
			file_data = pushme1.upload_file(picture, new_motion)	
		pushme1.push_file(**file_data)

		# Save the identity of the push to delete after 2 days
		new_push = pushme1.get_pushes()
		identity1 = new_push[0].get("iden")
		to_identity = 'echo "%s %s" >> /home/pi/Desktop/txt_files/push_list%s.txt' %(identity1, time.time(),itir)
		os.system(to_identity)
	
if send_email == True:
	for my_email in email_list:
		to_send1 = "mpack -s '%s' %s %s" %(camera_name,new_file_name,my_email)
		os.system(to_send1)	

# Remove all the other jpg files
os.system('sudo rm *jpg* >/dev/null 2>&1')

# Identify the AVI video file, and don't move on until this file exists
ab = False
while ab == False:
	avi_file = glob.glob('*avi*')
	if len(avi_file) < 1:
		time.sleep(0.2)
	else:
		break
#avi_file = to_change + '/' + avi_file[0]

# Movie the avi video file to the insync directory
to_do = 'sudo mv *avi* %s' %(directory_me) 
os.system(to_do)

# Delete this temporary Camera directory
to_delete = 'sudo rm -r /home/pi/Desktop/Camera_%s' %(new_fold)
os.chdir('/home/pi/Desktop/')
os.system(to_delete)

# Remove this directory
#cwd = os.getcwd()
#os.chdir('/home/pi/Desktop/')
#os.system(cwd)
