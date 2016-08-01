import re
import sensors
import radio
import httpReceiver

def parseRemoteCommand(command):
	if re.search(r'\w+;\w+;\w+;',command):
		parseCommand = re.split(r';',command)
		controller = int(parseCommand[0])
		relay = parseCommand[1]
		action = parseCommand[2]
		if action in ['auto','on','off']:
			print 'Set Relay'
			sensors.setRelayMode(controller, relay, command)
	if re.search(r'off',command):
		radio.do_Radio = False
		sensors.do_checkSensor = False
		httpReceiver.shutdown_server()
