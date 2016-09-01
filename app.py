
import httpReceiver
import init
import radio
import sensors
from threading import Thread
from log import logger
import sys

if __name__ == "__main__":
    try:
        init.initAll()
        th1 = Thread(name='th1', target=radio.listenRadio)
        th2 = Thread(name='th2', target=sensors.checkAllRelays)
        th3 = Thread(name='th3', target=httpReceiver.runFlaskServer)
        th1.start()
        th2.start()
        th3.start()
        th1.join()
        th2.join()
        th3.join()
        logger.info('Exit main thread')
    except Exception as e:
        logger.exception(e)
        sys.exit(0)
