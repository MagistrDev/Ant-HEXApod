import spidev
import time

class PWMFPGA(object):
	def __init__(self, spi_ch = 0, cs = 0, speed_hz = 4000000):
		self.__ch = spi_ch
		self.__cs = cs
		self.__speed = speed_hz
		self._bus = spidev.SpiDev()
		self.open()
		self.set_speed(self.__speed)
	def __del__(self):
		self.close()
	def open(self):
		self._bus.open(self.__ch, self.__cs)
	def close(self):
		self._bus.close()
	def set_speed(self, speed_hz):
		self._bus.max_speed_hz = speed_hz
	def send(self, arr):
		self._bus.xfer(arr)
	def send16(self, address, data):
		self.send([(address & 0xff), (data >> 8), (data & 0xff)])

class ServoFPGA(object):
	def __init__(self, spi_bus, ch, pulse = 1400, min_pulse = 440, max_pulse = 2600, max_angle = 180, on = 0):
		self.__ch = ch
		self.__bus = spi_bus
		self.__minPulse = min_pulse
		self.__maxPulse = max_pulse
		self.__maxAngle = max_angle
		self.disable()
		self.set_pulse(pulse)
		if on:
			self.enable()
	def map(self,x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min
	def	disable(self):
		self.__bus.send16(29, self.__ch)
	def enable(self):
		self.__bus.send16(29, self.__ch + (1 << 15))
	def set_pulse(self, pulse):
		self.__bus.send16(self.__ch, int(pulse))
	def set_angle(self, angle):
		self.set_pulse(self.map(angle, 0, self.__maxAngle, self.__minPulse, self.__maxPulse))
	def set_minpulse(self, minPulse):
		self.__minPulse = minPulse
	def set_minpulse(self, maxPulse):
		self.__maxPulse = maxPulse
	def set_minpulse(self, maxAngle):
		self.__maxAngle = maxAngle