import csv
import time
import re
from struct import *
import settings
import grafana
import radio

do_checkSensor = True

lastHour = 0;

storage = {}

turnOn = 1
turnOff = 0

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

auto = 'auto'
on = 'on'
off = 'off'
fileFolder = 'configs/'

cunningCounterMaxValue = 4
sleepPeriod = 10


def getFileName(controller):
    return fileFolder + str(controller) + '_' + time.strftime("%W") + ".csv"


def updateControllerThresholds():
    global lastHour
    if (time.localtime().tm_hour != lastHour):
        lastHour = time.localtime().tm_hour
        for each in storage:
            try:
                updateThresholds(each, getFileName(each))
            except IOError:
                print "There is no config file {}".format(getFileName(each))
                quit()


def updateThresholds(controller, filename):
    curHourInTable = time.localtime().tm_hour + 2
    with open(filename, 'rb') as csvfile:
        fileReader = csv.reader(csvfile)
        for row in fileReader:
            m = re.split(r';', row[0])
            relay = m[0]
            lowerValue = int(m[curHourInTable]) - int(m[1])
            upperValue = int(m[curHourInTable]) + int(m[1])
            saveThreshold(controller, relay, lowerValue, upperValue)


def saveThreshold(controller, relay, lowerValue, upperValue):
    storage[controller]['relays'][relay][cUpperBoundThreshold] = upperValue
    storage[controller]['relays'][relay][cLowerBoundThreshold] = lowerValue


def initSensorCell(controller):
    addr = radio.getPipeFromString(settings.getAddr(controller))
    storage[controller] = {
        'actionAddress': addr,
        'sensors':
            {
                cAirTemperature: {},
                cAirHumidity: {},
                cSoilHumidity: {},
                cLight: {},
                cLDR: {}
            },
        'relays':
            {
                cHeater: {},
                cCooler: {},
                cHumidifier: {},
                cIlluminator: {},
                cSprinkler: {}
            }
    }
    for each in storage[controller]['relays']:
        storage[controller]['relays'][each]['mode'] = auto
        storage[controller]['relays'][each]['switcher'] = None
        storage[controller]['relays'][each]['cunningCounter'] = {cLowerBoundCounter: 0, cUpperBoundCounter: 0}


def initStorage():
    for each in settings.getControllers():
        initSensorCell(each)


def getSensorName(number):
    switcher = {
        1: cAirTemperature,
        2: cAirHumidity,
        3: cSoilHumidity,
        4: cLight,
        5: cLDR
    }
    if number in switcher:
        return switcher[number]
    else:
        return None


def setRelayMode(controller, relay, command):
    storage[controller]['relays'][relay]['mode'] = command


def saveData(receivedMessage):
    string = byteArrayToStr(receivedMessage)
    controller = unpack('hhh', string)[0]
    if controller in storage:
        sensorName = getSensorName(unpack('hhh', string)[1])
        if not (sensorName is None):
            value = unpack('hhh', string)[2]
            if ('value' in storage[controller]['sensors'][sensorName]):
                storage[controller]['sensors'][sensorName]['oldValue'] = storage[controller]['sensors'][sensorName][
                    'value']
            storage[controller]['sensors'][sensorName]['value'] = value
            grafana.sendSensor(controller, sensorName, value)


def byteArrayToStr(receivedMessage):
    string = ""
    for n in receivedMessage:
        string += chr(n)
    return string


def checkAllRelays():
    print 'Begin check all relays'
    updateControllerThresholds()
    while do_checkSensor:
        time.sleep(sleepPeriod)
        for controller in storage:
            checkControllerRelay(controller)
    print 'End check all relays'


def turnRelaySwitcher(controller, relay, position):
    storage[controller]['relays'][relay]['switcher'] = position


def autoMode(controller, relay):
    if storage[controller]['relays'][relay]['mode'] == auto:
        return True
    else:
        return False


def relaySwitchOn(controller, relay):
    if storage[controller]['relays'][relay]['mode'] == on:
        return True
    else:
        return False


def relaySwitchOff(controller, relay):
    if storage[controller]['relays'][relay]['mode'] == off:
        return True
    else:
        return False


def checkControllerRelay(controller):
    checkHeater(controller)
    checkCooler(controller)
    checkHumidifier(controller)
    checkIlluminator(controller)


def checkHeater(controller):
    checkValueCrossingThreshold(controller, cAirTemperature, cHeater)
    if needTurnOnHeater(controller, cHeater):
        turnOnHeater(controller)
    if needTurnOffHeater(controller, cHeater):
        turnOffHeater(controller)


def checkCooler(controller):
    checkValueCrossingThreshold(controller, cAirTemperature, cCooler)
    if needTurnOnCooler(controller, cCooler):
        turnOnCooler(controller)
    if needTurnOffCooler(controller, cCooler):
        turnOffCooler(controller)


def checkHumidifier(controller):
    checkValueCrossingThreshold(controller, cAirHumidity, cHumidifier)
    if needTurnOnHumidifier(controller, cHumidifier):
        turnOnHumidifier(controller)
    if needTurnOffHumidifier(controller, cHumidifier):
        turnOffHumidifier(controller)


def checkIlluminator(controller):
    checkValueCrossingThreshold(controller, cLight, cIlluminator)
    if needTurnOnIlluminator(controller, cIlluminator):
        turnOnIlluminator(controller)
    if needTurnOffIlluminator(controller, cIlluminator):
        turnOffIlluminator(controller)


def checkValueCrossingThreshold(controller, sensor, relay):
    if 'value' in storage[controller]['sensors'][sensor]:
        if storage[controller]['sensors'][sensor]['value'] > storage[controller]['relays'][relay][cUpperBoundThreshold]:
            if storage[controller]['sensors'][sensor]['oldValue'] > storage[controller]['relays'][relay][
                cUpperBoundThreshold]:
                storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] += 1
                storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 0
            else:
                storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 1
                storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 0
        if storage[controller]['sensors'][sensor]['value'] < storage[controller]['relays'][relay][cLowerBoundThreshold]:
            if storage[controller]['sensors'][sensor]['oldValue'] < storage[controller]['relays'][relay][
                cLowerBoundThreshold]:
                storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] += 1
                storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 0
            else:
                storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] = 1
                storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] = 0
    else:
        print 'There is no value of {}'.format(sensor)


def needAutoTurnOffHeater(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOnHeater(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOnCooler(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOffCooler(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOffHumidifier(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOnHumidifier(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOffIlluminator(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cUpperBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needAutoTurnOnIlluminator(controller, relay):
    if storage[controller]['relays'][relay]['cunningCounter'][cLowerBoundCounter] > cunningCounterMaxValue:
        return True
    else:
        return False


def needTurnOffHeater(controller, relay):
    if (needAutoTurnOffHeater(controller, relay) and autoMode(controller, relay)) or relaySwitchOff(controller, relay):
        return True
    else:
        return False


def needTurnOnHeater(controller, relay):
    if (needAutoTurnOnHeater(controller, relay) and autoMode(controller, relay)) or relaySwitchOn(controller, relay):
        return True
    else:
        return False


def needTurnOnCooler(controller, relay):
    if (needAutoTurnOnCooler(controller, relay) and autoMode(controller, relay)) or relaySwitchOn(controller, relay):
        return True
    else:
        return False


def needTurnOffCooler(controller, relay):
    if (needAutoTurnOffCooler(controller, relay) and autoMode(controller, relay)) or relaySwitchOff(controller, relay):
        return True
    else:
        return False


def needTurnOffHumidifier(controller, relay):
    if (needAutoTurnOffHumidifier(controller, relay) and autoMode(controller, relay)) or relaySwitchOff(controller,
                                                                                                        relay):
        return True
    else:
        return False


def needTurnOnHumidifier(controller, relay):
    if (needAutoTurnOnHumidifier(controller, relay) and autoMode(controller, relay)) or relaySwitchOn(controller,
                                                                                                      relay):
        return True
    else:
        return False


def needTurnOffIlluminator(controller, relay):
    if (needAutoTurnOffIlluminator(controller, relay) and autoMode(controller, relay)) or relaySwitchOff(controller,
                                                                                                         relay):
        return True
    else:
        return False


def needTurnOnIlluminator(controller, relay):
    if (needAutoTurnOnIlluminator(controller, relay) and autoMode(controller, relay)) or relaySwitchOn(controller,
                                                                                                       relay):
        return True
    else:
        return False


def makeMsgForActionController(controller, relay, action):
    relayNum = {
        cHeater: 6,
        cCooler: 9,
        cHumidifier: 7,
        cIlluminator: 10
    }
    grafana.sendSensor(controller, relay, action)
    turnRelaySwitcher(controller, relay, action)
    return pack('hhh', controller, relayNum[relay], action)


def turnOnHeater(controller):
    print str(controller) + ": TurnOnHeater"
    radio.sendRadioMsg(storage[controller]['actionAddress'], makeMsgForActionController(controller, cHeater, turnOn))


def turnOffHeater(controller):
    print str(controller) + ": TurnOffHeater"
    radio.sendRadioMsg(storage[controller]['actionAddress'], makeMsgForActionController(controller, cHeater, turnOff))


def turnOnCooler(controller):
    print str(controller) + ": TurnOnCooler"
    radio.sendRadioMsg(storage[controller]['actionAddress'], makeMsgForActionController(controller, cCooler, turnOn))


def turnOffCooler(controller):
    print str(controller) + ": TurnOffCooler"
    radio.sendRadioMsg(storage[controller]['actionAddress'], makeMsgForActionController(controller, cCooler, turnOff))


def turnOnHumidifier(controller):
    print str(controller) + ": TurnOnHumidifier"
    radio.sendRadioMsg(storage[controller]['actionAddress'],
                       makeMsgForActionController(controller, cHumidifier, turnOn))


def turnOffHumidifier(controller):
    print str(controller) + ": TurnOffHumidifier"
    radio.sendRadioMsg(storage[controller]['actionAddress'],
                       makeMsgForActionController(controller, cHumidifier, turnOff))


def turnOnIlluminator(controller):
    print str(controller) + ": TurnOnIlluminator"
    radio.sendRadioMsg(storage[controller]['actionAddress'],
                       makeMsgForActionController(controller, cIlluminator, turnOn))


def turnOffIlluminator(controller):
    print str(controller) + ": TurnOffIlluminator"
    radio.sendRadioMsg(storage[controller]['actionAddress'],
                       makeMsgForActionController(controller, cIlluminator, turnOff))


def turnOnAll(controller):
    print str(controller) + ": TurnOnAll"
    turnOnHeater(controller)
    turnOnCooler(controller)
    turnOnHumidifier(controller)
    turnOnIlluminator(controller)


def turnOffAll(controller):
    print str(controller) + ": TurnOffAll"
    turnOffHeater(controller)
    time.sleep(0.5)
    turnOffCooler(controller)
    time.sleep(0.5)
    turnOffHumidifier(controller)
    time.sleep(0.5)
    turnOffIlluminator(controller)
    time.sleep(0.5)


def initAllRelays():
    for each in storage:
        turnOffAll(each)


def checkRelay(controller, relay):
    if relay == cHeater:
        checkHeater(controller)
    if relay == cCooler:
        checkCooler(controller)
    if relay == cHumidifier:
        checkHumidifier(controller)
    if relay == cIlluminator:
        checkIlluminator(controller)
