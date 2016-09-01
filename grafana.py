import socket
import settings
import time
import logging

graphiteURL = ''
graphitePort = 0
graphiteName = ''


def init():
    global graphiteURL
    global graphitePort
    graphiteURL = settings.getGraphiteURL()
    graphitePort = settings.getGraphitePort()
    global graphiteName
    graphiteName = settings.getName()


def sendSensor(controller, sensor, value):
    try:
        conn = socket.create_connection((graphiteURL, graphitePort))
        time_string = str(int(time.time()))
        send_string = graphiteName + "." + str(controller) + "." + sensor + " " + str(value) + " " + time_string + "\n"
        conn.send(send_string)
        conn.close()
    except socket.error:
        logging.warning('Grafana send error: socket error')
