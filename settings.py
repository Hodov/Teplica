import json

def getSettingsData():
	json_data = open('settings.json').read()
	data = json.loads(json_data)
	return data

def getControllers():
	return getSettingsData()['controllers']

def getName():
	return getSettingsData()['name']	

def getGraphiteURL():
	return getSettingsData()['graphiteURL']

def getGraphitePort():
	return getSettingsData()['graphitePort']	

def getPipe():
	return getSettingsData()['radioPipe']	

def getAddr(controller):
	return getSettingsData()[str(controller)]