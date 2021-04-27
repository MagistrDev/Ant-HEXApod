import logging
import time
import math
 
# Based on Adafruit Lib:
# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py
 
# Default address:
PCA9685_ADDRESS    = 0x40

ink_coxa = 0
ink_femur = 1
ink_tibia = 2
 
# Registers/etc:
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD
 
# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
 
# Channels
CHANNEL00          = 0x00
CHANNEL01          = 0x01
CHANNEL02          = 0x02
CHANNEL03          = 0x03
CHANNEL04          = 0x04
CHANNEL05          = 0x05
CHANNEL06          = 0x06
CHANNEL07          = 0x07
CHANNEL08          = 0x08
CHANNEL09          = 0x09
CHANNEL10          = 0x0A
CHANNEL11          = 0x0B
CHANNEL12          = 0x0C
CHANNEL13          = 0x0D
CHANNEL14          = 0x0E
CHANNEL15          = 0x0F
 
class PCA9685(object):
    def __init__(self, i2cBus, address=PCA9685_ADDRESS):
        self.i2cBus = i2cBus
        self.address = address
        self.begin()
 
    def begin(self):
        """Initialize device"""
        self.set_all_pwm(0, 0)
        self.i2cBus.write_byte_data(self.address, MODE2, OUTDRV)
        self.i2cBus.write_byte_data(self.address, MODE1, ALLCALL)
        time.sleep(0.005)                                         # wait for oscillator
        mode1 = self.i2cBus.read_byte_data(self.address, MODE1)
        mode1 = mode1 & ~SLEEP                                    # wake up (reset sleep)
        self.i2cBus.write_byte_data(self.address, MODE1, mode1)
        time.sleep(0.005)                                         # wait for oscillator
 
    def reset(self):
        self.i2cBus.write_byte_data(self.address, MODE1, RESTART)
        time.sleep(0.01)
 
    def set_address(self, address):
        """Sets device address."""
        self.address = address
 
    def set_i2c_bus(self, i2cBus):
        """Sets I2C Bus."""
        self.i2cBus = i2cBus
 
    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self.i2cBus.write_byte_data(self.address, LED0_ON_L + 4 * channel, on & 0xFF)
        self.i2cBus.write_byte_data(self.address, LED0_ON_H + 4 * channel, on >> 8)
        self.i2cBus.write_byte_data(self.address, LED0_OFF_L + 4 * channel, int(off) & 0xFF)
        self.i2cBus.write_byte_data(self.address, LED0_OFF_H + 4 * channel, int(off) >> 8)
 
    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self.i2cBus.write_byte_data(self.address, ALL_LED_ON_L, on & 0xFF)
        self.i2cBus.write_byte_data(self.address, ALL_LED_ON_H, on >> 8)
        self.i2cBus.write_byte_data(self.address, ALL_LED_OFF_L, off & 0xFF)
        self.i2cBus.write_byte_data(self.address, ALL_LED_OFF_H, off >> 8)
 
    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0                                  # 25MHz
        prescaleval /= 4096.0                                     # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = self.i2cBus.read_byte_data(self.address, MODE1)
        newmode = (oldmode & 0x7F) | 0x10                         # sleep
        self.i2cBus.write_byte_data(self.address, MODE1, newmode) # go to sleep
        self.i2cBus.write_byte_data(self.address, PRESCALE, prescale)
        self.i2cBus.write_byte_data(self.address, MODE1, oldmode)
        time.sleep(0.005)
        self.i2cBus.write_byte_data(self.address, MODE1, oldmode | 0x80)
 
    def __enter__(self):
        return self
 
    def __exit__(self, exception_type, exception_value, traceback):
        self.reset()
