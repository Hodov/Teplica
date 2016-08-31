import spidev
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import time
import sensors
import logging

radio = NRF24(GPIO, spidev.SpiDev())
do_Radio = True
pause_between_send = 0.1


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
        time.sleep(1 / 10)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    logging.debug(receivedMessage)
    return receivedMessage


def sendRadioMsg(addr, msg):
    radio.openWritingPipe(addr)
    radio.stopListening()
    if not (radio.write(msg)):
        print 'Error send message'
    time.sleep(pause_between_send)
    radio.startListening()


def getPipeFromString(stringPipe):
    return map(ord, stringPipe.decode("hex"))


def listenRadio():
    print 'Begin listening radio'
    while do_Radio:
        sensors.saveData(getRadioMsg())
    print 'End listening radio'
