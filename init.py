import radio
import sensors
import settings
import grafana
import log

#pipes = [[0xE8, 0XE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]


def initAll():
    print 'Init'
    log.init()
    print 'Init end'
    radio.initRadio(radio.getPipeFromString(settings.get_pipe()))
    sensors.initStorage()
    grafana.init()
    sensors.initAllRelays()
