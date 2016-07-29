import radio
import sensors
import settings
import grafana

pipes = [[0xE8,0XE8,0xF0,0xF0,0xE1],[0xF0,0xF0,0xF0,0xF0,0xE1]]

def initAll():
	radio.initRadio(pipes[1])
	sensors.initStorage()
	grafana.init()