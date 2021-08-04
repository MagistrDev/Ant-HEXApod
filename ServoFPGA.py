from start_on_pi import IsRunningOnPi
import time

if IsRunningOnPi():
	import spidev

class PWMFPGA(object):
	def __init__(self, spi_ch = 0, cs = 0, speed_hz = 4000000):
		self._run_on_pi = IsRunningOnPi()
		self.__ch = spi_ch
		self.__cs = cs
		self.__speed = speed_hz
		if self._run_on_pi:
			self._bus = spidev.SpiDev()
		self.open()
		self.set_speed(self.__speed)
	def __del__(self):
		self.close()
	def open(self):
		if self._run_on_pi:
			self._bus.open(self.__ch, self.__cs)
	def close(self):
		if self._run_on_pi:
			self._bus.close()
	def set_speed(self, speed_hz):
		if self._run_on_pi:
			self._bus.max_speed_hz = speed_hz
	def send(self, arr):
		if self._run_on_pi:
			self._bus.xfer(arr)
	def send16(self, address, data):
		self.send([(address & 0xff), (data >> 8), (data & 0xff)])

class ServoFPGA():
	def __init__(self, spi_bus, ch, on = 0, min_angle = 0, max_angle = 180, pulse = 1400, min_pulse = 530, max_pulse = 2420):
		self.__ch = ch
		self.__bus = spi_bus
		self.__minPulse = min_pulse
		self.__maxPulse = max_pulse
		self.__maxAngle = max_angle
		self.__minAngle = min_angle
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
		self.set_pulse(self.map(angle, self.__minAngle, self.__maxAngle, self.__minPulse, self.__maxPulse))
	def set_minPulse(self, minPulse):
		self.__minPulse = minPulse
	def set_maxPulse(self, maxPulse):
		self.__maxPulse = maxPulse
	def set_maxAngle(self, maxAngle):
		self.__maxAngle = maxAngle