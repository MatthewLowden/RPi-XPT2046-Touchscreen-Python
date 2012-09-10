# Copyright 2012 Matthew Lowden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import RPi.GPIO as GPIO
import time

class SPIManager(object):
	
	SPI_MOSI = 10
	SPI_MISO = 9
	SPI_SCLK = 11
	SPI_CE0 = 8
		
	def __init__(self):
		self.SPISetupGPIO();
	
	def SPISetupGPIO(self):
		GPIO.setmode(GPIO.BCM)
	
		GPIO.setup(SPIManager.SPI_MOSI, GPIO.OUT)
		GPIO.output(SPIManager.SPI_MOSI, GPIO.LOW)
	
		GPIO.setup(SPIManager.SPI_MISO, GPIO.IN)
	
		GPIO.setup(SPIManager.SPI_SCLK, GPIO.OUT)
		GPIO.output(SPIManager.SPI_SCLK, GPIO.LOW)
	
		GPIO.setup(SPIManager.SPI_CE0, GPIO.OUT)
		GPIO.output(SPIManager.SPI_CE0, GPIO.HIGH)
	
	
	def SPISelect(self):
		GPIO.output(SPIManager.SPI_CE0, GPIO.LOW)
		
	def SPIUnSelect(self):
		GPIO.output(SPIManager.SPI_CE0, GPIO.HIGH)
	
	def SPIPulseClock(self):		
		GPIO.output(SPIManager.SPI_SCLK, GPIO.HIGH)	
		GPIO.output(SPIManager.SPI_SCLK, GPIO.LOW)
		
	def SPISend(self, data):
		currentMOSIstate = False
		
		for i in range (len(data)):
			byteToSend = data[i]
			for j in range (8):

				desiredState = False
				if (byteToSend & 0x80) > 0 :
					desiredState = True

				if desiredState == True and currentMOSIstate == False :	
					GPIO.output(SPIManager.SPI_MOSI, GPIO.HIGH)
					currentMOSIstate = True
				elif desiredState == False and currentMOSIstate == True :
					GPIO.output(SPIManager.SPI_MOSI, GPIO.LOW)
					currentMOSIstate = False
				
				# Pulse the clock.
				self.SPIPulseClock()

				# Shift to the next bit.
				byteToSend <<= 1;
		if currentMOSIstate == True :
			GPIO.output(SPIManager.SPI_MOSI, GPIO.LOW)

		
	def SPIReceive(self, numBits):
		numBytes = (numBits + 7) // 8

		buffer = bytearray()

		# Array is filled in received byte order.
		# Any padding bits are the least significant bits, of the last byte.

		currentBit = 0;
		for i in range (numBytes):
			receiveByte = 0x00
			for j in range(8):
				# Shift to the next bit.
				receiveByte <<= 1

				# Skip padding bits
				currentBit += 1				
				if currentBit > numBits:
					continue

				# Set the clock high.
				GPIO.output(SPIManager.SPI_SCLK, GPIO.HIGH)

				# Read the value.
				bit = GPIO.input(SPIManager.SPI_MISO)

				# Set the clock low.
				GPIO.output(SPIManager.SPI_SCLK, GPIO.LOW)
				
				# Set the received bit.
				if bit == True : 
					receiveByte |= 1
				
			buffer.append(receiveByte)

		return buffer;
