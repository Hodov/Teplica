import socket
import settings
import time

graphiteURL = ''
graphitePort = 0
graphiteName = ''


def init():
    global graphiteURL
    global graphitePort
    graphitePort = settings.getGraphitePort()
    global graphiteName
    graphiteName = settings.getName()


def sendSensor(controller, sensor, value):
    try:
        conn = socket.create_connection((graphiteURL, graphitePort))
        timeString = str(int(time.time()))
        sendString = graphiteName + "." + str(controller) + "." + sensor + " " + str(value) + " " + timeString + "\n"
        conn.send(sendString)
        conn.close()
    except socket.error:
        print("Socket error")
