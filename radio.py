import spidev
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import time

radio = NRF24(GPIO,spidev.SpiDev())

def initRadio(radioAddress):
	GPIO.setmode(GPIO.BCM)
	radio.begin(0,17)
	radio.setPayloadSize(32)
	radio.setChannel(0x76)
	radio.setDataRate(NRF24.BR_1MBPS)
	radio.setPALevel(NRF24.PA_MIN)
	radio.setAutoAck(True)
	radio.enableDynamicPayloads()
	radio.enableAckPayload()
	radio.openReadingPipe(1,radioAddress)
	radio.printDetails()
	radio.startListening()

def getRadioMsg():
	while not radio.available(0):
			time.sleep(1/100)
	receivedMessage = []
	radio.read(receivedMessage,radio.getDynamicPayloadSize())
	return receivedMessage