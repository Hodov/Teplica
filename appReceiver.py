from threading import Thread
import radio
import sensors

pipes = [[0xE8,0XE8,0xF0,0xF0,0xE1],[0xF0,0xF0,0xF0,0xF0,0xE1]]


def listenRadio():
	i = 0;
	while i<50:
		i+=1
		sensors.saveData(radio.getRadioMsg())

if __name__ == "__main__":
	radio.initRadio(pipes[1])
	sensors.initSensors()
	th1 = Thread(name = 'th1', target = listenRadio())
	th2 = Thread(name = 'th2', target = sensors.checkAllRelays())


