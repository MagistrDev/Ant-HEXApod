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

direct_tmp = [1, 0, 1, 0, 1, 0]

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
	CurrentTrajectoryConfig.curvature = 1500
	CurrentTrajectoryConfig.distance = 50
	# стартовые позиции, надо подобрать
	MotionConfig.start_position = [Vector(-20, 0, 20), Vector(-35, 0, 0), Vector(-20, 0, -20),
									Vector(20, 0, 20), Vector(35, 0, 0), Vector(20, 0, -20)]
	# Одно из них направление движения. другое по воздуху или по земле
	MotionConfig.time_directions = [0, 0, 0,
									0, 0, 0]
	MotionConfig.trajectories = [0, 1, 0,
								1, 0, 1]
	global limbs_list
	for element in MotionConfig.start_position:
		limbs_list.append(LimbsList(element.x, element.y, element.z))

# Движение на шаг, использовать в цикле
def move(step: float):
	process_advanced_trajectory(step)
	if step == 1.0:
		MotionConfig.time_directions, MotionConfig.trajectories = MotionConfig.trajectories, MotionConfig.time_directions

# Сменить направление движения на противоположное
def change_direction():
	global direct_tmp
	direct_tmp, MotionConfig.time_directions = MotionConfig.time_directions, direct_tmp

# Сменить все стартовые позиции
def change_all_start_position():
	for i, element in zip(range(6), MotionConfig.start_position):
		xyz = input(f"write xyz for {i} leg\n").split(' ')
		element.x = int(xyz[0])
		element.y = int(xyz[1])
		element.z = int(xyz[2])

# Сменить одну выбранную стартовую позицию для определенной ноги
def change_one_start_position(num: int):
	xyz = input(f"write xyz\n").split(' ')
	MotionConfig.start_position[num].x = int(xyz[0])
	MotionConfig.start_position[num].y = int(xyz[1])
	MotionConfig.start_position[num].z = int(xyz[2])

# Сменить значения поворота и шага
def change_trajectory_config():
	CurrentTrajectoryConfig.curvature = int(input("write curvature\n"))
	CurrentTrajectoryConfig.distance = int(input("write distance\n"))

init_hexapod()
# change_direction()
# for element in MotionConfig.time_directions:
# 	print(element)
# change_start_position()

# for x in range(10):
# 	change_direction()
# 	for i in range(11):
# 		move(i / 10)
# 		print("----------------------")
# 		for j in range(6):
# 			print(limbs_list[j].position.x, limbs_list[j].position.y, limbs_list[j].position.z)
# 		print("-----------------------")
# 		# print(limbs_list[0].position.x, limbs_list[0].position.y, limbs_list[0].position.z)
# 		time.sleep(0.5)
# 	print("********************")


def cycle():
	change_trajectory_config()
	x = 0
	while 1:
		for step in range(11):
			move(step / 10)
			# for i in range(6):
			# 	pos_arm(i, limbs_list[i].position.x, limbs_list[i].position.y, limbs_list[i].position.z)
			x1 = int(limbs_list[0].position.x)
			y1 = int(limbs_list[0].position.y)
			z1 = int(limbs_list[0].position.z)
			x2 = int(limbs_list[1].position.x)
			y2 = int(limbs_list[1].position.y)
			z2 = int(limbs_list[1].position.z)
			x3 = int(limbs_list[2].position.x)
			y3 = int(limbs_list[2].position.y)
			z3 = int(limbs_list[2].position.z)
			x4 = int(limbs_list[3].position.x)
			y4 = int(limbs_list[3].position.y)
			z4 = int(limbs_list[3].position.z)
			x5 = int(limbs_list[4].position.x)
			y5 = int(limbs_list[4].position.y)
			z5 = int(limbs_list[4].position.z)
			x6 = int(limbs_list[5].position.x)
			y6 = int(limbs_list[5].position.y)
			z6 = int(limbs_list[5].position.z)
			print(str(step / 10) + "\t\t\t" + str(x1) + "/" + str(y1) + "/" + str(z1) + "\t\t" +str(x2) + "/" + str(y2) + "/" + str(z2) + "\t\t" + str(x3) + "/" + str(y3) + "/" + str(z3) +"\t\t" + str(x4) + "/" + str(y4) + "/" + str(z4) + "\t\t" +str(x5) + "/" + str(y5) + "/" + str(z5) + "\t\t" + str(x6) + "/" + str(y6) + "/" + str(z6))
		print()
		x += 1
		if x == 2:
			break

cycle()
print()
x1 = int(MotionConfig.start_position[0].x)
y1 = int(MotionConfig.start_position[0].y)
z1 = int(MotionConfig.start_position[0].z)
x2 = int(MotionConfig.start_position[1].x)
y2 = int(MotionConfig.start_position[1].y)
z2 = int(MotionConfig.start_position[1].z)
x3 = int(MotionConfig.start_position[2].x)
y3 = int(MotionConfig.start_position[2].y)
z3 = int(MotionConfig.start_position[2].z)
x4 = int(MotionConfig.start_position[3].x)
y4 = int(MotionConfig.start_position[3].y)
z4 = int(MotionConfig.start_position[3].z)
x5 = int(MotionConfig.start_position[4].x)
y5 = int(MotionConfig.start_position[4].y)
z5 = int(MotionConfig.start_position[4].z)
x6 = int(MotionConfig.start_position[5].x)
y6 = int(MotionConfig.start_position[5].y)
z6 = int(MotionConfig.start_position[5].z)
print(str(x1) + "/" + str(y1) + "/" + str(z1) + "\t" +str(x2) + "/" + str(y2) + "/" + str(z2) + "\t" + str(x3) + "/" + str(y3) + "/" + str(z3) +"\t" + str(x4) + "/" + str(y4) + "/" + str(z4) + "\t" +str(x5) + "/" + str(y5) + "/" + str(z5) + "\t" + str(x6) + "/" + str(y6) + "/" + str(z6))