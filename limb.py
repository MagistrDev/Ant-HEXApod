# from matplotlib.pyplot import step
from ServoFPGA import *
from math import *
from time import sleep
from initant import *

TIME_DIR_REVERSE = -1
LIMB_STEP_HEIGHT = 60
class point_3d_t:
	def __init__(self,x = 0,y = 0,z = 0):
		self._x = x
		self._y = y
		self._z = z
	def change_point(self,x,y,z):
		self._x = x
		self._y = y
		self._z = z

class LinkInfo():
	def __init__(self, servo : ServoFPGA, length = 0, zero_rotate = 0, min_angle = 0, max_angle = 0, angle = 0):
		#  Current link state
		self._servo = servo
		self._angle = angle
		#  Link configuration
		self._length = length
		self._zero_rotate = zero_rotate
		self._min_angle = min_angle
		self._max_angle = max_angle
	def set_angle(self, angle):
		self._servo.set_angle(angle)

class LimbInfo():
	LINK_COXA = 0
	LINK_FEMUR = 1
	LINK_TIBIA = 2
	def __init__(self, coxa : LinkInfo, femur : LinkInfo, tibia : LinkInfo, defPos : point_3d_t, time_directions = 0, trajectories = 1):
		self._position = point_3d_t()
		self._defPos = defPos
		self._coxa = coxa
		self._femur = femur
		self._tibia = tibia
		self._start_angle_r = 0
		self._time_directions = time_directions
		self._trajectories = trajectories
	def calculate_angles(self, point = None):
		coxa_zero_rotate_deg = self._coxa._zero_rotate
		femur_zero_rotate_deg = self._femur._zero_rotate
		tibia_zero_rotate_deg = self._tibia._zero_rotate
		coxa_length = self._coxa._length
		femur_length = self._femur._length
		tibia_length = self._tibia._length
		if point == None:
			# print("!!!!!!!!!def_point")
			x = self._position._x
			y = self._position._y
			z = -self._position._z
		elif isinstance(point, point_3d_t):
			# print("!!!!!!!!!pointd_3d")
			x = point._x
			y = point._y
			z = -point._z
			self._position.change_point(x,y,-z)
		elif isinstance(point, list):
			# print("!!!!!!!!!list")
			x = point[0]
			y = point[1]
			z = -point[2]
			self._position.change_point(x,y,-z)
		elif isinstance(point, dict):
			# print("!!!!!!!!!dict")
			x = point["x"]
			y = point["y"]
			z = -point["z"]
			self._position.change_point(x,y,-z)
		# print("point", self._position._x, self._position._y, self._position._z)
		# Move to (X*, Y*, Z*) coordinate system - rotate
		coxa_zero_rotate_rad = radians(coxa_zero_rotate_deg)
		x1 = x * cos(coxa_zero_rotate_rad) + z * sin(coxa_zero_rotate_rad)
		y1 = -y
		z1 = -x * sin(coxa_zero_rotate_rad) + z * cos(coxa_zero_rotate_rad)
		# Calculate COXA angle
		coxa_angle_rad = atan2(z1, x1)
		# Prepare for calculation FEMUR and TIBIA angles
		# Move to (X*, Y*) coordinate system (rotate on axis Y)
		x1 = x1 * cos(coxa_angle_rad) + z1 * sin(coxa_angle_rad)
		# Move to (X**, Y**) coordinate system (remove coxa from calculations)
		x1 = x1 - coxa_length
		# Calculate angle between axis X and destination point
		fi = atan2(y1, x1)
		# Calculate distance to destination point
		d = sqrt(x1 * x1 + y1 * y1)
		if (d > femur_length + tibia_length):
			return False # Point not attainable
		# Calculate triangle angles
		a = tibia_length
		b = femur_length
		c = d
		alpha = acos((b * b + c * c - a * a) / (2 * b * c))
		gamma = acos((a * a + b * b - c * c) / (2 * a * b))
		# Calculate FEMUR and TIBIA angle
		# Check angles
		a1 = -(degrees(coxa_angle_rad))
		a2 = self._femur._max_angle - (femur_zero_rotate_deg - (degrees(alpha) - degrees(fi)))
		a3 = self._tibia._max_angle - (degrees(gamma) - tibia_zero_rotate_deg)
		print("angles_to",a1,a2,a3,"\t",x,-y,-z)
		# if (a1 < self._coxa._min_angle or a1 > self._coxa._max_angle):
		# 	return False
		# if (a2 < self._femur._min_angle or a2 > self._femur._max_angle):
		# 	return False
		# if (a3 < self._tibia._min_angle or a3 > self._tibia._max_angle):
		# 	return False
		self._coxa._angle = a1
		# print(self._femur._max_angle, femur_zero_rotate_deg, degrees(alpha), degrees(fi))
		self._femur._angle = a2
		self._tibia._angle = a3
		# print("angles",self._coxa._angle,self._femur._angle,self._tibia._angle)
		return True
	def set_angles(self, coxa_angle = None, femur_angle = None, tibia_angle = None):
		if coxa_angle == None:
			coxa_angle = self._coxa._angle
		if femur_angle == None:
			femur_angle = self._femur._angle
		if tibia_angle == None:
			tibia_angle = self._tibia._angle
		print("set_angles", coxa_angle,femur_angle,tibia_angle)
		self._coxa.set_angle(coxa_angle)
		self._femur.set_angle(femur_angle)
		self._tibia.set_angle(tibia_angle)
	def move(self, point = None):
		if point == None:
			pt = self._position
		elif isinstance(point, point_3d_t):
			pt = point
			self._position = point
		elif isinstance(point, list):
			pt = point_3d_t(point[0], point[1], point[2])
			self._position = pt
		elif isinstance(point, dict):
			pt = point_3d_t(point["x"], point["y"], point["z"])
			self._position = pt
		self.calculate_angles()
		self.set_angles()
	def invers_direct(self):
		self._time_directions = not self._time_directions 
	def invers_trajectory(self):
		self._trajectories = not self._trajectories

class Bot():
	def __init__(self, limb_fl : LimbInfo, limb_ml : LimbInfo, limb_rl : LimbInfo,
			limb_fr : LimbInfo, limb_mr : LimbInfo, limb_rr : LimbInfo, delay = 0.2,
												inc_step = 0.05,distance = 60, hight_step = 50, curvature = 0.00001):
		self._limbs = (limb_fl, limb_ml, limb_rl, limb_fr, limb_mr, limb_rr)
		self._step = 0.0
		self._delay = delay
		self._inc_step = inc_step
		self._curvature = curvature
		self._distance = distance
		self._hight_step = hight_step
	def advanced_trajectory(self, curvature = None, motion_time = None, distance = None):
		if motion_time == None:
			motion_time = self._step
		else:
			self.set_step(motion_time)
		if curvature == None:
			curvature = self._curvature
		else:
			self._curvature = curvature
		if distance == None:
			distance = self._distance
		else:
			self._distance = distance
		# Check Curvature
		if curvature == 0:
			curvature = 0.000000001
		elif curvature > 1.9999999999:
			curvature = 1.9999999999
		elif curvature < -1.999999999:
			curvature = -1.999999999
		distance = distance
		#  ???????????? ?????????????????? ???????????? ???????????????? ?????????????????? 
		curvature_radius = tan((2.0 - curvature) * pi / 4.0) * abs(distance)
		# print(curvature_radius)
		trajectory_radius = []
		start_angle_rad = []
		max_trajectory_radius = 0
		for i in range(len(self._limbs)):
			defpos = self._limbs[i]._defPos
			tr_r = sqrt((curvature_radius - defpos._x) * (curvature_radius - defpos._x) + defpos._z * defpos._z)
			trajectory_radius.append(tr_r)
			if tr_r > max_trajectory_radius:
				max_trajectory_radius = tr_r
			start_angle_rad.append(atan2(defpos._z,-(curvature_radius - defpos._x)))
			# print("start angle rad "+ str(i) + " - " + str(round(start_angle_rad[i],5)) + "\tradius " + str(trajectory_radius[i]))
		if max_trajectory_radius == 0:
			return False
		# Calculation max angle of arc
		curvature_radius_sign = 0
		curvature_radius_sign = 1 if  (curvature_radius >= 0) else -1
		max_arc_angle = curvature_radius_sign * distance / max_trajectory_radius
		# print(max_trajectory_radius,max_arc_angle)
		#  Calculation points by time
		for i in range(len(self._limbs)):
			# Inversion motion time if need
			relative_motion_time = motion_time
			if self._limbs[i]._time_directions == 1:
				relative_motion_time = 1.0 - relative_motion_time
			# relative_motion_time = limbs[i]._time_directions - motion_time
			# Calculation arc angle for current time
			arc_angle_rad = (relative_motion_time - 0.5) * max_arc_angle + start_angle_rad[i]
			# Calculation XZ points by time
			self._limbs[i]._position._x = curvature_radius + trajectory_radius[i] * cos(arc_angle_rad)
			# print("x'"+str(round(self._limbs[i]._position._x,5)) + "' = curv_r'"+str(round(curvature_radius,5))+"' + tr_r'"+str(round(trajectory_radius[i],5))+"' * cos(arc_ang_rad'"+str(round(arc_angle_rad,5))+"')")
			self._limbs[i]._position._z = trajectory_radius[i] * sin(arc_angle_rad)
			# Calculation Y points by time
			if self._limbs[i]._trajectories == 1:
				self._limbs[i]._position._y = defpos._y
			else:
				self._limbs[i]._position._y = defpos._y + self._hight_step * sin(pi*relative_motion_time)
			# print("arc_angle_" + str(i) + " - " + str(arc_angle_rad))
		return True
	def invers_direct(self):
		for i in range(len(self._limbs)):
			self._limbs[i].invers_direct()
	def set_curvature(self,curvature):
		if curvature == 0:
			curvature = 0.000000001
		elif curvature > 1.9999999999:
			curvature = 1.9999999999
		elif curvature < -1.999999999:
			curvature = -1.999999999
		self._curvature = curvature
	def invers_trajectory(self):
		for i in range(len(self._limbs)):
			self._limbs[i].invers_trajectory()
	def move(self):
		for i in range(len(self._limbs)):
			self._limbs[i].move()
	def inc_step(self):
		self._step += self._inc_step
		if self._step > 1:
			self._step = 0
			self.invers_trajectory()
			self.invers_direct()
	def set_step(self,step):
		self._step = step
	def full_step(self, curvature = None, distance = None):
		if not curvature == None:
			self.set_curvature(curvature)
		if not distance == None and distance < 70:
			self._distance = distance
		while self._step < 1:
			self.advanced_trajectory()
			self.move()
			self.inc_step()
			sleep(self._delay)
		self.advanced_trajectory()
		self.move()
		self.inc_step()

link_fl_coxa =  LinkInfo(FL_COXA, 55, -135, 90, -90,0)
link_fl_femur = LinkInfo(FL_FEMUR, 75, 85, 0, 180, 0)
link_fl_tibia = LinkInfo(FL_TIBIA, 121, 11.8, 0, 180, 0)

link_ml_coxa =  LinkInfo(ML_COXA, 55, 180, 90, -90, 0)
link_ml_femur = LinkInfo(ML_FEMUR, 75, 85, 0, 180, 0)
link_ml_tibia = LinkInfo(ML_TIBIA, 121, 11.8, 0, 180, 0)

link_rl_coxa =  LinkInfo(RL_COXA, 55, 135, 90, -90, 0)
link_rl_femur = LinkInfo(RL_FEMUR, 75, 85, 0, 180, 0)
link_rl_tibia = LinkInfo(RL_TIBIA, 121, 11.8, 0, 180, 0)

link_fr_coxa =  LinkInfo(FR_COXA, 55, -45, -90, 90, 0)
link_fr_femur = LinkInfo(FR_FEMUR, 75, 85, 0, 180, 0)
link_fr_tibia = LinkInfo(FR_TIBIA, 121, 11.8, 0, 180, 0)

link_mr_coxa =  LinkInfo(MR_COXA, 55, 0, -90, 90, 0)
link_mr_femur = LinkInfo(MR_FEMUR, 75, 85, 0, 180, 0)
link_mr_tibia = LinkInfo(MR_TIBIA, 121, 11.8, 0, 180, 0)

link_rr_coxa =  LinkInfo(RR_COXA, 55, 45, -90, 90, 0)
link_rr_femur = LinkInfo(RR_FEMUR, 75, 85, 0, 180, 0)
link_rr_tibia = LinkInfo(RR_TIBIA, 121, 11.8, 0, 180, 0)

limb_fl = LimbInfo(link_fl_coxa, link_fl_femur, link_fl_tibia, point_3d_t(-120, -120, 50),0,1)
limb_ml = LimbInfo(link_ml_coxa, link_ml_femur, link_ml_tibia, point_3d_t(-120, -120, 0),1,0)
limb_rl = LimbInfo(link_rl_coxa, link_rl_femur, link_rl_tibia, point_3d_t(-120, -120, -50),0,1)
limb_fr = LimbInfo(link_fr_coxa, link_fr_femur, link_fr_tibia, point_3d_t(120, -120, 50),1,0)
limb_mr = LimbInfo(link_mr_coxa, link_mr_femur, link_mr_tibia, point_3d_t(120, -120, 0),0,1)
limb_rr = LimbInfo(link_rr_coxa, link_rr_femur, link_rr_tibia, point_3d_t(120, -120, -50),1,0)

bot = Bot(limb_fl, limb_ml, limb_rl, limb_fr, limb_mr, limb_rr,0.05,0.05,70,50,0.00001)


delay_step = 0.05

def walk():
	bot.advanced_trajectory()
	bot.move()
	bot.inc_step()
	sleep(delay_step)

def start():
	while 1:
		walk()