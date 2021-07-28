import math
import time

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# Пока так, потом буду функции приводить к юзер френдли, если понадобится #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #

# Don't know from where it is
SUPPORT_LIMBS_COUNT = 6
TIME_DIR_REVERSE = 1
TRAJECTORY_XZ_ADV_Y_CONST = 0
TRAJECTORY_XZ_ADV_Y_SINUS = 1
# Высота шага константа меняй через нее
LIMB_STEP_HEIGHT = 10
HEXAPOD_DIRECTION = 0

direct_tmp = [0, 1, 0, 1, 0, 1]

class CurrentTrajectoryConfig:
	curvature: float = 0
	distance: float = 0

class Vector:
	x: float = 0
	y: float = 0
	z: float = 0
	def __init__(self, x: float, y: float, z: float):
		self.x = x
		self.y = y
		self.z = z

class MotionConfig:
	start_position: Vector = []
	time_directions = []
	trajectories: int = []

class LimbsList:
	position: Vector
	def __init__(self, x: float, y: float, z: float):
		self.position = Vector(x, y, z)

limbs_list: LimbsList = []

def process_advanced_trajectory(motion_time: float) -> bool:

	# Check curvature value
	curvature: float = CurrentTrajectoryConfig.curvature / 1000.0
	if CurrentTrajectoryConfig.curvature == 0:
		curvature = 0.001
	if CurrentTrajectoryConfig.curvature > 1999:
		curvature = 1.999
	if CurrentTrajectoryConfig.curvature < -1999:
		curvature = -1.999
	
	# 
	# Calculate XZ
	# 
	distance: float = CurrentTrajectoryConfig.distance

	# Calculation radius of curvature
	curvature_radius = math.tan((2.0 - curvature) * math.pi / 4.0) * distance

	# Common calculations
	trajectory_radius: float = []
	start_angle_rad: float = []
	max_trajectory_radius: float = 0
	for i in range(SUPPORT_LIMBS_COUNT):
		
		x0: float = MotionConfig.start_position[i].x
		z0: float = MotionConfig.start_position[i].z

		# Calculation trajectory radius
		element_trajectory_radius = math.sqrt((curvature_radius - x0) * (curvature_radius - x0) + z0 * z0)
		trajectory_radius.append(element_trajectory_radius)

		# Search max trajectory radius
		if element_trajectory_radius > max_trajectory_radius:
			max_trajectory_radius = element_trajectory_radius
		
		# Calculation limb start angle
		start_angle_rad.append(math.atan2(z0, -(curvature_radius - x0)))

	# Avoid division by zero
	if max_trajectory_radius == 0:
		return False
	
	# Calculation max angle of arc
	curvatur_radius_sign = 1 if curvature_radius >= 0 else -1
	max_arc_angle: float = curvatur_radius_sign * distance / max_trajectory_radius

	# Calculation points by time
	global limbs_list
	for i in range(SUPPORT_LIMBS_COUNT):

		# Inversion motion time if need
		relative_motion_time: float = motion_time
		if MotionConfig.time_directions[i] == TIME_DIR_REVERSE:
			relative_motion_time = 1.0 - relative_motion_time
		
		# Calculation arc angle for current time
		arc_angle_rad: float = (relative_motion_time - 0.5) * max_arc_angle + start_angle_rad[i]

		# Calculation XZY points by time
		position_x = curvature_radius + trajectory_radius[i] * math.cos(arc_angle_rad)
		position_z = trajectory_radius[i] * math.sin(arc_angle_rad)

		# Be careful in position_y
		# Double check //aapricot
		position_y = MotionConfig.start_position[i].y
		# if MotionConfig.trajectories[i] == TRAJECTORY_XZ_ADV_Y_CONST:
		# 	position_y = MotionConfig.start_position[i].y
		if MotionConfig.trajectories[i] == TRAJECTORY_XZ_ADV_Y_SINUS:
			position_y += LIMB_STEP_HEIGHT * math.sin(relative_motion_time * math.pi)
		# limbs_list.append(LimbsList(position_x, position_y, position_z))
		limbs_list[i].position.x = position_x
		limbs_list[i].position.y = position_y
		limbs_list[i].position.z = position_z
	return True

def	init_hexapod():
	CurrentTrajectoryConfig.curvature = 500
	CurrentTrajectoryConfig.distance = 50
	# стартовые позиции, надо подобрать
	MotionConfig.start_position = [Vector(-70, -50, 70), Vector(-80, -50, 0), Vector(-70,-50, -70),
									Vector(70, -50,70), Vector(80, -50, 0), Vector(70, -50, -70)]
	# Одно из них направление движения. другое по воздуху или по земле
	MotionConfig.time_directions = [1, 0, 1,
									0, 1, 0]
	MotionConfig.trajectories = [0, 1, 0,
								1, 0, 1]
	global limbs_list
	for element in MotionConfig.start_position:
		limbs_list.append(LimbsList(element.x, element.y, element.z))

def chose_back_forward():
	global direct_tmp
	MotionConfig.time_directions, direct_tmp = direct_tmp, MotionConfig.time_directions

# возможно поменяю на приходящие данные
# пока замена руками в терминале
def change_start_position():
	for i in range(6):
		tmp = input().split(' ')
		MotionConfig.start_position[i] = Vector(int(tmp[0], int(tmp[1], int(tmp[2]))))

def change_direction(direction: int):
	CurrentTrajectoryConfig.curvature = direction
	
def change_speed(speed: int):
	CurrentTrajectoryConfig.distance = speed

def change_high_step(high: int):
	global LIMB_STEP_HEIGHT
	LIMB_STEP_HEIGHT = high

def stop():
	for i in range(SUPPORT_LIMBS_COUNT):
		limbs_list[i].position.x = MotionConfig.start_position[i].x
		limbs_list[i].position.y = MotionConfig.start_position[i].y
		limbs_list[i].position.z = MotionConfig.start_position[i].z

# Движение на шаг, использовать в цикле
def move(step: float):
	process_advanced_trajectory(step)
	if step == 1.0:
		MotionConfig.time_directions, MotionConfig.trajectories = MotionConfig.trajectories, MotionConfig.time_directions

def control(direction: int, trajectroy: int, step: float):
	global HEXAPOD_DIRECTION
	if HEXAPOD_DIRECTION != direction:
		chose_back_forward()
	change_direction(trajectroy / 100 * 1999)
	move(step)
# init_hexapod()

# for x in range(10):
# 	for i in range(11):
# 		move_forward(i / 10)
# 		# print("----------------------")
# 		# for j in range(6):
# 		# 	print(limbs_list[j].position.x, limbs_list[j].position.y, limbs_list[j].position.z)
# 		# print("-----------------------")
# 		print(limbs_list[0].position.x, limbs_list[0].position.y, limbs_list[0].position.z)
# 		time.sleep(0.5)

# for i in range(5):
# 	process_advanced_trajectory(0.7)
# 	print(f"--------{i}----------")
# 	for j, element in zip(range(6), limbs_list):
# 		print(element.position.x, element.position.y, element.position.z)
# 		MotionConfig.start_position[j].x = element.position.x
# 		MotionConfig.start_position[j].y = element.position.y
# 		MotionConfig.start_position[j].z = element.position.z
	# print("---------------------")

# process_advanced_trajectory(1.0)