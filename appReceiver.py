from threading import Thread
import init
import sensors
import radio
import httpReceiver

def listenRadio():
	print 'Begin listening radio'
	i = 0;
	while i<50:
		i+=1
		sensors.saveData(radio.getRadioMsg())
	print 'End listening radio'

if __name__ == "__main__":
	init.initAll()
	th1 = Thread(name = 'th1', target = listenRadio())
	th2 = Thread(name = 'th2', target = sensors.checkAllRelays())
	


