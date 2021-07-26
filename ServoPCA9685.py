import time
# Servo with PCA9685 implementation
 
 
def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min + 1) / (in_max - in_min + 1) + out_min
 
class ServoPCA9685(object):
# Configure min and max servo pulse lengths
	# servo_min = 130 # Min pulse length out of 4096 / 150/112
	# servo_max = 510 # Max pulse length out of 4096 / 600/492

	def __init__(self, pca9685, channel, servo_min = 800, servo_max = 4091, angel_max = 180):
		self.pca9685 = pca9685
		self.channel = channel
		self.set_pwm_freq(400)
		self.servo_min = servo_min
		self.servo_max = servo_max
		self.angel_max = angel_max
		# self.set_pulse(300)
 
	def set_pwm_freq(self, freq=400):
		self.pca9685.set_pwm_freq(freq)
		time.sleep(0.001)
 
	def set_angle(self, angle):
		self.set_pulse(map(angle, 0, self.angel_max, self.servo_min, self.servo_max))
 
	def set_pulse(self, pulse):
		# if pulse >= self.servo_min and pulse <= self.servo_max:
		self.pca9685.set_pwm(self.channel, 0, pulse)
		# time.sleep(0.005)
 
	def servomin(self):
		return self.servo_min
 
	def servomax(self):
		return self.servo_max
 
	def disable(self):
		self.pca9685.set_pwm(self.channel, 0, 0)
		time.sleep(0.005)
def test():
	while 1:
		testserv.set_pulse(800)
		testserv2.set_pulse(800)
		time.sleep(1)
		testserv.set_pulse(4090)
		testserv2.set_pulse(4090)
		time.sleep(1)