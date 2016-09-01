import json
from log import logger


def getSettingsData():
    json_data = open('settings.json').read()
    data = json.loads(json_data)
    return data


def getControllers():
    keys = getSettingsData()['controllers'].keys()
    new_keys = [int(i) for i in keys]
    return new_keys


def getName():
    return getSettingsData()['name']


def getGraphiteURL():
    return getSettingsData()['graphiteURL']


def getGraphitePort():
    return getSettingsData()['graphitePort']


def getAddr(controller):
    return getSettingsData()['controllers'][str(controller)]['pipe']


def getNameController(controller):
    return getSettingsData()['controllers'][str(controller)]['name']


def get_pipe():
    pipe = getSettingsData()['pipe']
    logger.debug('Pipe of main controller: ' + pipe)
    return pipe


def get_log_level():
    return getSettingsData()['log_level']
