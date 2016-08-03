import re
import sensors
import radio
import httpReceiver
from flask import jsonify

def parseRemoteCommand(command):
	if re.search(r'\w+;\w+;\w+;',command):
		parseRelayCommand(command)
	elif re.search(r'off',command):
		parseOffCommand()
	else:
		print 'Unknown command'

def parseRelayCommand(command):
	parseCommand = re.split(r';',command)
	controller = int(parseCommand[0])
	relay = parseCommand[1]
	action = parseCommand[2]
	if action in ['auto','on','off']:
		print 'Set Relay'
		sensors.setRelayMode(controller, relay, action)

def parseOffCommand():
	radio.do_Radio = False
	sensors.do_checkSensor = False
	httpReceiver.shutdown_server()

def getStorage():
	return jsonify(sensors.storage)