import csv
import time
import re
from struct import *

storage = {}

thresholdFile = 'threshold.csv'

cAirTemperature = 'airTemperature'
cAirHumidity = 'airHumidity'
cSoilHumidity = 'soilHumidity'
cLight = 'light'
cLDR = 'LDR'

cHeater = 'heater'
cCooler = 'cooler'
cHumidifier = 'humidifier'
cIlluminator = 'illuminator'
cSprinkler = 'sprinkler'

cLowerBoundThreshold = 'lowerBoundThreshold'
cUpperBoundThreshold = 'upperBoundThreshold'

cLowerBoundCounter = 'cLowerBoundCounter'
cUpperBoundCounter = 'cUpperBoundCounter'

cunningCounterMaxValue = 4
sleepPeriod = 5

def initSensors():
	initThresholds(thresholdFile)

def initThresholds(filename):
	with open (filename, 'rb') as csvfile:
		fileReader = csv.reader(csvfile)
		for row in fileReader:
			m = re.split(r';',row[0])
			controller = int(m[1])
			relay = m[2]
			lowerValue = int(m[3])
			upperValue = int(m[4])
			if not (controller in storage):
				initSensorCell(controller)
			if (time.strftime("%d.%m.%Y") == m[0]):
				saveThreshold(controller, relay, lowerValue, upperValue)

def saveThreshold(controller, relay, lowerValue, upperValue):
	storage[controller]['relays'][relay][cUpperBoundThreshold] = upperValue
	storage[controller]['relays'][relay][cLowerBoundThreshold] = lowerValue

def initSensorCell(controller):
	storage[controller] = { 
		'sensors' : 
		{ 
			cAirTemperature : {}, 
			cAirHumidity : {}, 
			cSoilHumidity : {}, 
			cLight : {}, 
			cLDR : {} 
		}, 
		'relays' : 
		{ 
			cHeater : {}, 
			cCooler : {}, 
			cHumidifier : {}, 
			cIlluminator : {}, 
			cSprinkler : {} 
		} 
	}
	for each in storage[controller]['relays']:
		storage[controller]['relays'][each]['mode'] = 'auto'
		storage[controller]['relays'][each]['cunningCounter'] = { cLowerBoundCounter : 0, cUpperBoundCounter : 0 }


def getSensorName(number):
	switcher = {
		1 : cAirTemperature,
		2 : cAirHumidity,
		3 : cSoilHumidity,
		4 : cLight,
		5 : cLDR
	}
	return switcher[number]


def saveData(receivedMessage):
	string = ""
	for n in receivedMessage:
		string += chr(n)
	controller = unpack('hhh', string)[0]
	sensorName = getSensorName(unpack('hhh', string)[1])
	value = unpack('hhh', string)[2]
	if ('value' in storage[controller]['sensors'][sensorName]):
		storage[controller]['sensors'][sensorName]['oldValue'] = storage[controller]['sensors'][sensorName]['value']
	storage[controller]['sensors'][sensorName]['value'] = value


def checkAllRelays():
	i = 0
	while i<5:
		i+=1
		for controller in storage:
			checkControllerRelay(controller)
		time.sleep(sleepPeriod)

def checkControllerRelay(controller):
	checkHeater(controller)
	checkCooler(controller)
	checkHumidifier(controller)
	checkIlluminator(controller)


def checkHeater(controller):
	checkValueCrossingThreshold(controller, cAirTemperature, cHeater)
	if needTurnOnHeater(controller, cHeater):
		turnOnHeater()
	if needTurnOffHeater(controller, cHeater):
		turnOffHeater()

def checkCooler(controller):
	checkValueCrossingThreshold(controller, cAirTemperature, cCooler)
	if needTurnOnCooler(controller, cCooler):
		turnOnCooler()
	if needTurnOffCooler(controller, cCooler):
		turnOffCooler()
	
def checkHumidifier(controller):
	checkValueCrossingThreshold(controller, cAirHumidity, cHumidifier)
	if needTurnOnHumidifier(controller, cHumidifier):
		turnOnHumidifier()
	if needTurnOffHumidifier(controller, cHumidifier):
		turnOffHumidifier()

def checkIlluminator(controller):
	checkValueCrossingThreshold(controller, cLDR, cIlluminator)
	if needTurnOnIlluminator(controller, cIlluminator):
		turnOnIlluminator()
	if needTurnOffIlluminator(controller, cIlluminator):
		turnOffIlluminator()

def checkValueCrossingThreshold(controller, sensor, relay):
	if storage[controller]['sensors'][sensor]['value'] > storage[controller]['relays'][relay][cUpperBoundThreshold]:
		if storage[controller]['sensors'][sensor]['oldValue'] > storage[controller]['relays'][relay][cUpperBoundThreshold]:
			storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] += 1
			storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 0
		else:
			storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 1
			storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 0
	if storage[controller]['sensors'][sensor]['value'] < storage[controller]['relays'][relay][cLowerBoundThreshold]:
		if storage[controller]['sensors'][sensor]['oldValue'] < storage[controller]['relays'][relay][cLowerBoundThreshold]:
			storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] += 1
			storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 0
		else:
			storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 1
			storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 0


def needTurnOffHeater(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOnHeater(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOnCooler(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOffCooler(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOffHumidifier(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOnHumidifier(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOffIlluminator(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def needTurnOnIlluminator(controller, relay):
	if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
		return True
	else:
		return False

def turnOnHeater():
	print "TurnOnHeater"

def turnOffHeater():
	print "TurnOffHeater"

def turnOnCooler():
	print "TurnOnCooler"

def turnOffCooler():
	print "TurnOffCooler"

def turnOnHumidifier():
	print "TurnOnHumidifier"

def turnOffHumidifier():
	print "TurnOffHumidifier"

def turnOnIlluminator):
	print "TurnOnIlluminator"

def turnOffHumidifier():
	print "TurnOffHIlluminator"
