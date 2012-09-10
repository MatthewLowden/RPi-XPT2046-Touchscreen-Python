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

from SPIManager import SPIManager

class XPT2046(object):
	
	StartBit = 0b10000000 
	
	class ChannelSelect(object):
		X_POSITION = 0b01010000
		Y_POSITION = 0b00010000
		Z1_POSITION = 0b00110000
		Z2_POSITION = 0b01000000
		TEMPERATURE_0 = 0b00000000
		TEMPERATURE_1 = 0b01110000
		BATTERY_VOLTAGE = 0b00100000
		AUXILIARY = 0b01100000

	class ConversionSelect(object):
		_8_BIT = 0b00001000
		_12_BIT = 0b00000000
	
	def __init__(self):
		self._ConversionSelect = XPT2046.ConversionSelect._12_BIT
		self._SPIManager = SPIManager()
		
	def setMode(self, conversionSelect):
		self._ConversionSelect = conversionSelect
	
	def makeControlByte(self, channelSelect):
		# @@TODO Other elements in control byte.
		return XPT2046.StartBit | channelSelect | self._ConversionSelect
	
	def readValue(self, channelSelect):
		controlByte = self.makeControlByte(channelSelect)
		msg = bytearray()
		msg.append(controlByte)
		self._SPIManager.SPISelect()
		self._SPIManager.SPISend(msg)
		
		# Skip the 'busy' bit.
		self._SPIManager.SPIPulseClock();
		
		responseValue = 0
		
		if self._ConversionSelect == XPT2046.ConversionSelect._12_BIT:
			responseData = self._SPIManager.SPIReceive(12)
			responseValue = (responseData[0] << 4) | (responseData[1] >> 4) 
		else:
			responseData = self._SPIManager.SPIReceive(8)
			responseValue = responseData[0]
			
		self._SPIManager.SPIUnSelect()
		return responseValue
		
		
	def readX(self):
		return self.readValue(XPT2046.ChannelSelect.X_POSITION)
		
	def readY(self):
		return self.readValue(XPT2046.ChannelSelect.Y_POSITION)
		
	def readZ1(self):
		return self.readValue(XPT2046.ChannelSelect.Z1_POSITION)

	def readZ2(self):
		return self.readValue(XPT2046.ChannelSelect.Z2_POSITION)

	def readBatteryVoltage(self):
		return self.readValue(XPT2046.ChannelSelect.BATTERY_VOLTAGE)

	def readTemperature0(self):
		return self.readValue(XPT2046.ChannelSelect.TEMPERATURE_0)

	def readTemperature1(self):
		return self.readValue(XPT2046.ChannelSelect.TEMPERATURE_1)

	def readAuxiliary(self):
		return self.readValue(XPT2046.ChannelSelect.AUXILIARY)

	def readTouchPressure(self):
		# Formula (option 1) according to the datasheet (12bit conversion)
		# RTouch = RX-Plate.(XPosition/4096).((Z1/Z2)-1)
		# Not sure of the correct value of RX-Plate.
		# Assuming the ratio is sufficient.
		# Empirically this function seems to yield a values in the range of 0.4
		# for a firm touch, and 1.75 for a light touch.

		x = self.readX();
		z1 = self.readZ1();
		z2 = self.readZ2();
		
		# Avoid division by zero exception
		if (z1 == 0) :
			z1 = 1
		
		xDivisor = 4096;
		if (self._ConversionSelect == XPT2046.ConversionSelect._8_BIT) :
			xDivisor = 256;

		result = ( x / xDivisor) * (( z2 / z1) - 1);
		return result;