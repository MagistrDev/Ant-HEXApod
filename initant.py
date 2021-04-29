import time
import smbus
import PCA9685
import ServoPCA9685

# def init_servo():
i2cBus = smbus.SMBus(1)
l_pca9685 = PCA9685.PCA9685(i2cBus, 0x41)

l1_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL11)
l1_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL10)
l1_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL09)

l2_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL07)
l2_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL06)
l2_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL05)

l3_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL15)
l3_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL14)
l3_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL13)

r_pca9685 = PCA9685.PCA9685(i2cBus, 0x40)

r1_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL11)
r1_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL10)
r1_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL09)

r2_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL07)
r2_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL06)
r2_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL05)

r3_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL03)
r3_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL02)
r3_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL01)

arms = [[l1_sh, l1_fore, l1_wr],[l3_sh, l2_fore, l2_wr],[l3_sh, l3_fore, l3_wr],[r1_sh, r1_fore, r1_wr],[r2_sh, r2_fore, r2_wr],[r3_sh, r3_fore, r3_wr]]

def set_arm_ang(index, sh, fore, wr):
	angle_sh = 90 + sh
	arms[index][0].set_angle(angle_sh)
	arms[index][1].set_angle(fore)
	arms[index][2].set_angle(wr)

def def_pos():
	l1_fore.set_angle(0)
	l2_fore.set_angle(0)
	l3_fore.set_angle(0)
	r1_fore.set_angle(0)
	r2_fore.set_angle(0)
	r3_fore.set_angle(0)

	time.sleep(1)

	l1_wr.set_angle(0)
	l2_wr.set_angle(0)
	l3_wr.set_angle(0)
	r1_wr.set_angle(0)
	r2_wr.set_angle(0)
	r3_wr.set_angle(0)

	time.sleep(1)

	l1_sh.set_angle(90)
	l2_sh.set_angle(90)
	l3_sh.set_angle(90)
	r1_sh.set_angle(90)
	r2_sh.set_angle(90)
	r3_sh.set_angle(90)

def stand():
	l1_fore.set_angle(80)
	l2_fore.set_angle(80)
	l3_fore.set_angle(80)
	r1_fore.set_angle(80)
	r2_fore.set_angle(80)
	r3_fore.set_angle(80)

	l1_wr.set_angle(30)
	l2_wr.set_angle(30)
	l3_wr.set_angle(30)
	r1_wr.set_angle(30)
	r2_wr.set_angle(30)
	r3_wr.set_angle(30)

	l1_sh.set_angle(180)
	l3_sh.set_angle(40)
	r1_sh.set_angle(40)
	r3_sh.set_angle(180)

def disable_all():
	l1_wr.disable()
	l1_fore.disable()
	l1_sh.disable()
	
	l2_wr.disable()
	l2_fore.disable()
	l2_sh.disable()

	l3_wr.disable()
	l3_fore.disable()
	l3_sh.disable()

	r1_wr.disable()
	r1_fore.disable()
	r1_sh.disable()

	r2_wr.disable()
	r2_fore.disable()
	r2_sh.disable()

	r3_wr.disable()
	r3_fore.disable()
	r3_sh.disable()

# # l1_wr.set_pulse(1000)

# def_pos()