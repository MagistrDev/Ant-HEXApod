
from start_on_pi import IsRunningOnPi

if IsRunningOnPi():
	import smbus

class INA219:
	ADDRESS         = 0x40
	# registers    
	CONF_REG        = 0x00 # Configuration Register
	SHUNT_REG       = 0x01 # Shunt Voltage Register
	BUS_REG         = 0x02 # Bus Voltage Register
	PWR_REG         = 0x03 # Power Register 
	CURRENT_REG     = 0x04 # Current flowing through Shunt
	CAL_REG         = 0x05 # Calibration Register 

	# parametrs 
	INA219_RST      = 0x8000

	# P_GAIN
	PG_40           = 0x0000
	PG_80           = 0x0800
	PG_160          = 0x1000
	PG_320          = 0x1800

	# mask for bus ADC resolution bits
	BADCRES_MASK = 0x0780

	# ADC_MODE
	BIT_MODE_9      = 0b00000000
	BIT_MODE_10     = 0b00000001
	BIT_MODE_11     = 0b00000010
	BIT_MODE_12     = 0b00000011
	SAMPLE_MODE_2   = 0b00001001
	SAMPLE_MODE_4   = 0b00001010
	SAMPLE_MODE_8   = 0b00001011
	SAMPLE_MODE_16  = 0b00001100
	SAMPLE_MODE_32  = 0b00001101
	SAMPLE_MODE_64  = 0b00001110
	SAMPLE_MODE_128 = 0b00001111

	# MEASURE_MODE
	POWER_DOWN      = 0b00000000
	TRIGGERED       = 0b00000011
	ADC_OFF         = 0b00000100
	CONTINUOUS      = 0b00000111
	CONTINOUS       = 0b00000111

	# PGAIN
	PG_40           = 0x0000
	PG_80           = 0x0800
	PG_160          = 0x1000
	PG_320          = 0x1800

	# BUS_RANGE
	BRNG_16         = 0x0000
	BRNG_32         = 0x2000

	# mask for shunt ADC resolution bits
	SADCRES_MASK = 0x0078

	CONFIG_BADCRES_12BIT_128S_69MS = 0x0780

	# mask for operating mode bits
	MODE_MASK       = 0x0007

	def __init__(self, bus, addr = ADDRESS):
		self._addr = addr
		self._bus = bus
		self._pwrMultiplier_mW = 0.0
		self._currentDivider_mA = 0.0
		self._calc_overflow = False
		self._deviceADCMode = 0
		self._calValue = 0
		self.setADCMode(INA219.BIT_MODE_12)
		self.setMeasureMode(INA219.CONTINUOUS)
		self.setPGain(INA219.PG_320)
		self.setBusRange(INA219.BRNG_32)
		self._calc_overflow = False

	def read_register(self, reg):
		ret = 0
		if IsRunningOnPi():
			ret = self._bus.read_word_data(self._addr, reg)
		ret = ((ret & 0xff) << 8) | (ret >> 8)
		return ret

	def write_register(self, reg, data):
		send_data = ((data & 0xff) << 8) | (data >> 8)
		if IsRunningOnPi():
			self._bus.write_word_data(self._addr, reg, send_data)

	def setADCMode(self, mode):
		self._deviceADCMode = mode
		currentConfReg = self.read_register(INA219.CONF_REG)
		currentConfReg &= ~(INA219.BADCRES_MASK)
		currentConfReg &= ~(INA219.SADCRES_MASK)
		adcMask = mode << 3
		currentConfReg |= adcMask
		adcMask = mode << 7
		currentConfReg |= adcMask
		self.write_register(INA219.CONF_REG, currentConfReg)

	def setMeasureMode(self, mode):
		deviceMeasureMode = mode
		currentConfReg = self.read_register(INA219.CONF_REG)
		currentConfReg &= ~(INA219.MODE_MASK)
		currentConfReg |= deviceMeasureMode
		self.write_register(INA219.CONF_REG, currentConfReg)

	def setPGain(self, gain):
		global pwrMultiplier_mW, currentDivider_mA
		devicePGain = gain
		currentConfReg = self.read_register(INA219.CONF_REG)
		currentConfReg &= ~(0x1800)
		currentConfReg |= devicePGain
		self.write_register(INA219.CONF_REG, currentConfReg)
		if devicePGain == INA219.PG_40:
			calVal = 20480
			currentDivider_mA = 50.0
			pwrMultiplier_mW = 0.4
		elif devicePGain == INA219.PG_80:
			calVal = 10240
			currentDivider_mA = 25.0
			pwrMultiplier_mW = 0.8
		elif devicePGain == INA219.PG_160:
			calVal = 8192
			currentDivider_mA = 20.0
			pwrMultiplier_mW = 1.0
		elif devicePGain == INA219.PG_320:
			calVal = 4096
			currentDivider_mA = 10.0
			pwrMultiplier_mW = 2.0
		self.write_register(INA219.CAL_REG, calVal)

	def setBusRange(self, range):
		global calc_overflow
		deviceBusRange = range
		currentConfReg = self.read_register(INA219.CONF_REG)
		currentConfReg &= ~(0x2000)
		currentConfReg |= deviceBusRange
		self.write_register(INA219.CONF_REG, currentConfReg)
		calc_overflow = False
		return True

	def reset_ina219(self):
		self.write_register(INA219.CONF_REG, INA219.RST)

	def getShuntVoltage_mV(self):
		val = self.read_register(INA219.SHUNT_REG)
		return (val * 0.01);    

	def getBusVoltage_V(self):
		val = self.read_register(INA219.BUS_REG)
		val = ((val>>3) * 4)
		return (val * 0.001)

	def getCurrent_mA(self):
		val = self.read_register(INA219.CURRENT_REG)
		return (val / currentDivider_mA)

	def getBusPower(self):
		val = self.read_register(INA219.PWR_REG)
		return (val * pwrMultiplier_mW)

	def getOverflow(self):
		val = self.read_register(INA219.BUS_REG)
		ovf = (val & 1)
		return ovf