import json

def getControllers():
	json_data = open('settings.json').read()
	data = json.loads(json_data)
	return data['controllers']