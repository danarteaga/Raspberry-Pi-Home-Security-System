#!/bin/bash

# Created by Dan Arteaga

# This script will pause motion detection

# Change to the Desktop directory
cd /home/pi/Desktop

/usr/bin/wget -q -O /dev/null "192.168.1.110:8086/0/detection/start"
