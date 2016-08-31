import radio
import sensors
import settings
import grafana

pipes = [[0xE8, 0XE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]


def initAll():
    radio.initRadio(radio.getPipeFromString(settings.getPipe()))
    sensors.initStorage()
    grafana.init()
    sensors.initAllRelays()
