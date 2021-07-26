import time
# import smbus
# import PCA9685
# import ServoPCA9685
from ServoFPGA import *

fpga_chip = PWMFPGA()
FL_COXA = ServoFPGA(fpga_chip, 2, 1, 1520)
FL_FEMUR = ServoFPGA(fpga_chip, 1, 1, 1520)
FL_TIBIA = ServoFPGA(fpga_chip, 0, 1, 1520)

ML_COXA = ServoFPGA(fpga_chip, 4, 1, 1520)
ML_FEMUR = ServoFPGA(fpga_chip, 5, 1, 1520)
ML_TIBIA = ServoFPGA(fpga_chip, 3, 1, 1520)

RL_COXA = ServoFPGA(fpga_chip, 6, 1, 1520)
RL_FEMUR = ServoFPGA(fpga_chip, 7, 1, 1520)
RL_TIBIA = ServoFPGA(fpga_chip, 8, 1, 1520)

FR_COXA = ServoFPGA(fpga_chip, 9, 1, 1520)
FR_FEMUR = ServoFPGA(fpga_chip, 10, 1, 1520)
FR_TIBIA = ServoFPGA(fpga_chip, 11, 1, 1520)

MR_COXA = ServoFPGA(fpga_chip, 12, 1, 1520)
MR_FEMUR = ServoFPGA(fpga_chip, 13, 1, 1520)
MR_TIBIA = ServoFPGA(fpga_chip, 14, 1, 1520)

RR_COXA = ServoFPGA(fpga_chip, 15, 1, 1520)
RR_FEMUR = ServoFPGA(fpga_chip, 16, 1, 1520)
RR_TIBIA = ServoFPGA(fpga_chip, 17, 1, 1520)



# def init_servo():
# i2cBus = smbus.SMBus(1)
# l_pca9685 = PCA9685.PCA9685(i2cBus, 0x41)

# l1_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL11)
# l1_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL10)
# l1_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL09)

# l2_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL07)
# l2_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL06)
# l2_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL05)

# l3_wr = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL15)
# l3_fore = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL14)
# l3_sh = ServoPCA9685.ServoPCA9685(l_pca9685,PCA9685.CHANNEL13)

# r_pca9685 = PCA9685.PCA9685(i2cBus, 0x40)

# r1_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL11)
# r1_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL10)
# r1_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL09)

# r2_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL07)
# r2_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL06)
# r2_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL05)

# r3_wr = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL03)
# r3_fore = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL02)
# r3_sh = ServoPCA9685.ServoPCA9685(r_pca9685,PCA9685.CHANNEL01)

arms = [[FL_COXA, FL_FEMUR, FL_TIBIA],[ML_COXA, ML_FEMUR, ML_TIBIA],[RL_COXA, RL_FEMUR, RL_TIBIA],[FR_COXA, FR_FEMUR, FR_TIBIA],[MR_COXA, MR_FEMUR, MR_TIBIA],[RR_COXA, RR_FEMUR, RR_TIBIA]]

def set_arm_ang(index, sh, fore, wr):
	if index < 3:
		angle_sh = 90 + sh
		# print("!")
	else:
		angle_sh = 90 - sh
	# print(str(sh) + " " + str(angle_sh))
	arms[index][0].set_angle(angle_sh)
	arms[index][1].set_angle(fore)
	arms[index][2].set_angle(wr)

# def def_pos():
# 	l1_fore.set_angle(0)
# 	l2_fore.set_angle(0)
# 	l3_fore.set_angle(0)
# 	r1_fore.set_angle(0)
# 	r2_fore.set_angle(0)
# 	r3_fore.set_angle(0)

# 	time.sleep(1)

# 	l1_wr.set_angle(0)
# 	l2_wr.set_angle(0)
# 	l3_wr.set_angle(0)
# 	r1_wr.set_angle(0)
# 	r2_wr.set_angle(0)
# 	r3_wr.set_angle(0)

# 	time.sleep(1)

# 	l1_sh.set_angle(90)
# 	l2_sh.set_angle(90)
# 	l3_sh.set_angle(90)
# 	r1_sh.set_angle(90)
# 	r2_sh.set_angle(90)
# 	r3_sh.set_angle(90)

# def stand():
# 	l1_fore.set_angle(80)
# 	l2_fore.set_angle(80)
# 	l3_fore.set_angle(80)
# 	r1_fore.set_angle(80)
# 	r2_fore.set_angle(80)
# 	r3_fore.set_angle(80)

# 	l1_wr.set_angle(30)
# 	l2_wr.set_angle(30)
# 	l3_wr.set_angle(30)
# 	r1_wr.set_angle(30)
# 	r2_wr.set_angle(30)
# 	r3_wr.set_angle(30)

# 	l1_sh.set_angle(180)
# 	l3_sh.set_angle(40)
# 	r1_sh.set_angle(40)
# 	r3_sh.set_angle(180)

# def disable_all():
# 	l1_wr.disable()
# 	l1_fore.disable()
# 	l1_sh.disable()
	
# 	l2_wr.disable()
# 	l2_fore.disable()
# 	l2_sh.disable()

# 	l3_wr.disable()
# 	l3_fore.disable()
# 	l3_sh.disable()

# 	r1_wr.disable()
# 	r1_fore.disable()
# 	r1_sh.disable()

# 	r2_wr.disable()
# 	r2_fore.disable()
# 	r2_sh.disable()

# 	r3_wr.disable()
# 	r3_fore.disable()
# 	r3_sh.disable()

# # l1_wr.set_pulse(1000)

# def_pos()
