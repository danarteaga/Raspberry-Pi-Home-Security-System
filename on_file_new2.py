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

