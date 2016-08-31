import json


def getSettingsData():
    json_data = open('settings.json').read()
    data = json.loads(json_data)
    return data


def getControllers():
    #данные пришли как string
    keys = getSettingsData()['controllers'].keys()
    #а нам нужны int
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
    return getSettingsData()['pipe']


def get_log_level():
    return getSettingsData()['log_level']
