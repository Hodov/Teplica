import spidev
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import time
import sensors
from log import logger
from struct import *

radio = NRF24(GPIO, spidev.SpiDev())
do_Radio = True
pause_between_send = 0.2
pause_between_get = 0.2


def initRadio(radioAddress):
    GPIO.setmode(GPIO.BCM)
    radio.begin(0, 17)
    radio.setRetries(15, 15)
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openReadingPipe(1, radioAddress)
    radio.printDetails()
    radio.startListening()


def getRadioMsg():
    while not radio.available(0):
        time.sleep(pause_between_get)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    logger.debug(receivedMessage)
    return receivedMessage


def sendRadioMsg(addr, msg):
    radio.openWritingPipe(addr)
    radio.stopListening()
    if not (radio.write(msg)):
        str = unpack('hhh', msg)
        logger.warning('Error send message: {}'.format(str))
    time.sleep(pause_between_send)
    radio.startListening()


def getPipeFromString(stringPipe):
    return map(ord, stringPipe.decode("hex"))


def listenRadio():
    logger.info('Begin listening radio')
    while do_Radio:
        sensors.saveData(getRadioMsg())
    logger.info('End listening radio')
