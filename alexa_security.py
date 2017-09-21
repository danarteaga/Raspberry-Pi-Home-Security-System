import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.intent('SecureIntent', mapping={'status': 'status'})
def secure_control(status):
	if status == "on":
		os.system('cd /home/pi/Desktop; bash check_arm.sh')
	elif status == "off":
		os.system('cd /home/pi/Desktop; bash check_disarm.sh')

	return statement('Turning pi {}'.format(status))
	