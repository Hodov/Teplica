from httpReceiver import application
import httpReceiver
import init
import radio
import sensors
from threading import Thread

if __name__ == "__main__":
	init.initAll()
	th1 = Thread(name = 'th1', target = radio.listenRadio)
	th2 = Thread(name = 'th2', target = sensors.checkAllRelays)
	th3 = Thread(name = 'th3', target = httpReceiver.runFlaskServer)
	#application.run(debug=True, use_reloader = False, host='0.0.0.0')
	th1.start()
	th2.start()
	th3.start()
	th1.join()
	th2.join()
	th3.join()
	print 'Exit main thread'