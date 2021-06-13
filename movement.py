import math
import initant as ant
LINK_COXA = 0
LINK_FEMUR = 1
LINK_TIBIA = 2

class LinkInfo():
    def __init__(self, length = 0, zero_rotate = 0, min_angle = 0, max_angle = 0, angle = 0):
        #  Current link state
        self._angle = 0.0
        #  Link configuration
        self._length = 0
        self._zero_rotate = 0
        self._min_angle = 0
        self._max_angle = 0


class Vector():
	def __init__(self, x = 0, y = 0, z = 0):
		self._x = x
		self._y = y
		self._z = z


class LimbInfo():
	def __init__(self):
		self._position = Vector()
		self._links = [LinkInfo(),LinkInfo(),LinkInfo()]
		self._defPosition = Vector()


def RAD_TO_DEG(rad):
    return ((rad) * 180.0 / math.pi)


def DEG_TO_RAD(deg):
    return ((deg) * math.pi / 180.0)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# planes = [LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo()]
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Hexapod(object):
	# Можно вынести в дефайны некоторые значения
	supportLimbsCount = 6
	timeDirReverse = 1
	trajectoryYCONST = 0
	trajectoryYSINUS = 1
	limbStepHeight = 10
	hexapodDirection = 0
	directionTmp = [0, 1, 0, 1, 0, 1]

	def __init__(self, curvature = 0, distance = 50,
				timeDirections = [1, 0, 1, 0, 1, 0], trajectories =
				[0, 1, 0, 1, 0, 1]):
		self._curvature = curvature
		self._distance = distance
		self._timeDirections = timeDirections
		self._trajectories = trajectories

	def calcAdvancedXYZ(self, motionTime, planes):
		curvature = self._curvature / 1000.0
		if self._curvature == 0:
			curvature = 0.001
		elif self._curvature > 1999:
			curvature = 1.999
		elif self._curvature < -1999:
			curvature = -1.999
		
		# 
		# Calculate XZ
		# 
		distance = self._distance

		# Calculation radius of curvature
		curvatureRadius = math.tan((2.0 - curvature) * math.pi / 4.0) * distance

		# Common calculations
		trajectoryRadius = []
		startAngleRadius = []
		maxTrajectoryRadius = 0.0
		for i in range(self.supportLimbsCount):

			x0 = planes[i]._defPosition._x
			z0 = planes[i]._defPosition._z

			# Calculation trajectory radius
			elementTrajectoryRadius = math.sqrt((curvatureRadius - x0) * (curvatureRadius - x0) + z0 * z0)
			trajectoryRadius.append(elementTrajectoryRadius)

			# Search max trajectory radius
			if elementTrajectoryRadius > maxTrajectoryRadius:
				maxTrajectoryRadius = elementTrajectoryRadius
			
			# Calculation limb start angle
			startAngleRadius.append(math.atan2(z0, -(curvatureRadius - x0)))
		
		# Avoid division by zero
		if maxTrajectoryRadius == 0:
			return False
		
		# Calculation max angle of arc
		curvatureRadiusSign = 1 if curvatureRadius >= 0 else -1
		maxArcAngle = curvatureRadiusSign * distance / maxTrajectoryRadius

		# Calculation points by time
		for i in range(self.supportLimbsCount):
			# Inversion motion time if need
			relativeMotionTime = motionTime
			if self._timeDirections[i] == self.timeDirReverse:
				relativeMotionTime = 1.0 - relativeMotionTime
			
			# Calculation arc angle for current time
			arcAngleRad = (relativeMotionTime - 0.5) * maxArcAngle + startAngleRadius[i]

			# Calculation XZY points by time
			positionX = curvatureRadius + trajectoryRadius[i] * math.cos(arcAngleRad)
			positionZ = trajectoryRadius[i] * math.sin(arcAngleRad)
			positionY = planes[i]._defPosition._y

			if self._trajectories[i] == self.trajectoryYSINUS:
				positionY += self.limbStepHeight * math.sin(relativeMotionTime * math.pi)
			
			planes[i]._position._x = positionX
			planes[i]._position._y = positionY
			planes[i]._position._z = positionZ
		return True

	def kinematic_calculate_angles(self, pindex, planes):
		info = planes[pindex]
		coxa_zero_rotate_deg = info._links[LINK_COXA]._zero_rotate
		femur_zero_rotate_deg = info._links[LINK_FEMUR]._zero_rotate
		tibia_zero_rotate_deg = info._links[LINK_TIBIA]._zero_rotate
		coxa_length = info._links[LINK_COXA]._length
		femur_length = info._links[LINK_FEMUR]._length
		tibia_length = info._links[LINK_TIBIA]._length
		x = info._position._x
		y = info._position._y
		z = info._position._z
		# print("Position xyz" +  str(x) + " / " + str(y) + " / " + str(z))
		# Move to (X*, Y*, Z*) coordinate system - rotate
		coxa_zero_rotate_rad = DEG_TO_RAD(coxa_zero_rotate_deg)
		x1 = x * math.cos(coxa_zero_rotate_rad) + z * math.sin(coxa_zero_rotate_rad)
		y1 = y
		z1 = -x * math.sin(coxa_zero_rotate_rad) + z * math.cos(coxa_zero_rotate_rad)
		# Calculate COXA angle
		coxa_angle_rad = math.atan2(z1, x1)
		info._links[LINK_COXA]._angle = RAD_TO_DEG(coxa_angle_rad)
		# Prepare for calculation FEMUR and TIBIA angles
		# Move to (X*, Y*) coordinate system (rotate on axis Y)
		x1 = x1 * math.cos(coxa_angle_rad) + z1 * math.sin(coxa_angle_rad)
		# Move to (X**, Y**) coordinate system (remove coxa from calculations)
		x1 = x1 - coxa_length
		# Calculate angle between axis X and destination point
		fi = math.atan2(y1, x1)
		# Calculate distance to destination point
		d = math.sqrt(x1 * x1 + y1 * y1)
		if (d > femur_length + tibia_length):
		    return False # Point not attainable
		# Calculate triangle angles
		a = tibia_length
		b = femur_length
		c = d
		alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
		gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
		# Calculate FEMUR and TIBIA angle
		info._links[LINK_FEMUR]._angle = femur_zero_rotate_deg - RAD_TO_DEG(alpha) - RAD_TO_DEG(fi)
		info._links[LINK_TIBIA]._angle = RAD_TO_DEG(gamma) - tibia_zero_rotate_deg
		# print(info._links[LINK_COXA]._angle)
		# print(info._links[LINK_FEMUR]._angle)
		# print(info._links[LINK_TIBIA]._angle)
		# Check angles
		if (info._links[LINK_COXA]._angle < info._links[LINK_COXA]._min_angle or info._links[LINK_COXA]._angle > info._links[LINK_COXA]._max_angle):
		    return False
		if (info._links[LINK_FEMUR]._angle < info._links[LINK_FEMUR]._min_angle or info._links[LINK_FEMUR]._angle > info._links[LINK_FEMUR]._max_angle):
		    return False
		if (info._links[LINK_TIBIA]._angle < info._links[LINK_TIBIA]._min_angle or info._links[LINK_TIBIA]._angle > info._links[LINK_TIBIA]._max_angle):
		    return False
		return True
	
	def changeDefPostition(self, planes):
		for i in range(6):
			tmp = input().split(' ')
			planes[i]._defPosition = Vector(int(tmp[0], int(tmp[1], int(tmp[2]))))
	
	def changeDirection(self, curvature:):
		self._curvature = curvature
	
	def changeDistance(self, distance):
		self._distance = distance
	
	def changeHeightStep(self, height):
		self.limbStepHeight = height
	
	def stop(self, planes):
		for i in range(self.supportLimbsCount):
			planes[i]._position = planes[i]._defPosition
	
	def swapDirection(self):
		self._timeDirections, self.directionTmp = self.directionTmp, self._timeDirections
	
	def move(self, direction, curvature, step, planes):
		if self.hexapodDirection != direction:
			self.stop(planes)
			self.swapDirection()
		self.changeDirection(int(curvature / 100 * 1999))
		self.calcAdvancedXYZ(step, planes)
		for index in range(self.supportLimbsCount):
			self.kinematic_calculate_angles(index, planes)
			ant.set_arm_ang(index, pl[index]._links[0]._angle, pl[index]._links[1]._angle, pl[index]._links[2]._angle)
		if step == 1.0:
			self._timeDirections, self._trajectories = self._trajectories, self._timeDirections

	
def getPlanes():
	planes = [LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo()]

	planes[0]._links[LINK_COXA]._length = 46.7
	planes[0]._links[LINK_COXA]._zero_rotate = 25.56
	planes[0]._links[LINK_COXA]._min_angle = -90
	planes[0]._links[LINK_COXA]._max_angle = 90

	planes[0]._links[LINK_FEMUR]._length = 90
	planes[0]._links[LINK_FEMUR]._zero_rotate = 90
	planes[0]._links[LINK_FEMUR]._min_angle = 0
	planes[0]._links[LINK_FEMUR]._max_angle = 180

	planes[0]._links[LINK_TIBIA]._length = 122.558
	planes[0]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[0]._links[LINK_TIBIA]._min_angle = 0
	planes[0]._links[LINK_TIBIA]._max_angle = 180


	planes[1]._links[LINK_COXA]._length = 46.7
	planes[1]._links[LINK_COXA]._zero_rotate = 0
	planes[1]._links[LINK_COXA]._min_angle = -50
	planes[1]._links[LINK_COXA]._max_angle = 50

	planes[1]._links[LINK_FEMUR]._length = 90
	planes[1]._links[LINK_FEMUR]._zero_rotate = 90
	planes[1]._links[LINK_FEMUR]._min_angle = 0
	planes[1]._links[LINK_FEMUR]._max_angle = 180

	planes[1]._links[LINK_TIBIA]._length = 122.558
	planes[1]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[1]._links[LINK_TIBIA]._min_angle = 0
	planes[1]._links[LINK_TIBIA]._max_angle = 180



	planes[2]._links[LINK_COXA]._length = 46.7
	planes[2]._links[LINK_COXA]._zero_rotate = -25.56
	planes[2]._links[LINK_COXA]._min_angle = 90
	planes[2]._links[LINK_COXA]._max_angle = -90

	planes[2]._links[LINK_FEMUR]._length = 90
	planes[2]._links[LINK_FEMUR]._zero_rotate = 90
	planes[2]._links[LINK_FEMUR]._min_angle = 0
	planes[2]._links[LINK_FEMUR]._max_angle = 180

	planes[2]._links[LINK_TIBIA]._length = 122.558
	planes[2]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[2]._links[LINK_TIBIA]._min_angle = 0
	planes[2]._links[LINK_TIBIA]._max_angle = 180




	planes[3]._links[LINK_COXA]._length = 46.7
	planes[3]._links[LINK_COXA]._zero_rotate = 25.56
	planes[3]._links[LINK_COXA]._min_angle = -90
	planes[3]._links[LINK_COXA]._max_angle = 90

	planes[3]._links[LINK_FEMUR]._length = 90
	planes[3]._links[LINK_FEMUR]._zero_rotate = 90
	planes[3]._links[LINK_FEMUR]._min_angle = 0
	planes[3]._links[LINK_FEMUR]._max_angle = 180

	planes[3]._links[LINK_TIBIA]._length = 122.558
	planes[3]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[3]._links[LINK_TIBIA]._min_angle = 0
	planes[3]._links[LINK_TIBIA]._max_angle = 180


	planes[4]._links[LINK_COXA]._length = 46.7
	planes[4]._links[LINK_COXA]._zero_rotate = 0
	planes[4]._links[LINK_COXA]._min_angle = -50
	planes[4]._links[LINK_COXA]._max_angle = 50

	planes[4]._links[LINK_FEMUR]._length = 90
	planes[4]._links[LINK_FEMUR]._zero_rotate = 90
	planes[4]._links[LINK_FEMUR]._min_angle = 0
	planes[4]._links[LINK_FEMUR]._max_angle = 180

	planes[4]._links[LINK_TIBIA]._length = 122.558
	planes[4]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[4]._links[LINK_TIBIA]._min_angle = 0
	planes[4]._links[LINK_TIBIA]._max_angle = 180



	planes[5]._links[LINK_COXA]._length = 46.7
	planes[5]._links[LINK_COXA]._zero_rotate = -25.56
	planes[5]._links[LINK_COXA]._min_angle = -90
	planes[5]._links[LINK_COXA]._max_angle = 90

	planes[5]._links[LINK_FEMUR]._length = 90
	planes[5]._links[LINK_FEMUR]._zero_rotate = 90
	planes[5]._links[LINK_FEMUR]._min_angle = 0
	planes[5]._links[LINK_FEMUR]._max_angle = 180

	planes[5]._links[LINK_TIBIA]._length = 122.558
	planes[5]._links[LINK_TIBIA]._zero_rotate = 16.7
	planes[5]._links[LINK_TIBIA]._min_angle = 0
	planes[5]._links[LINK_TIBIA]._max_angle = 180

	planes[0]._defPosition = Vector(-80, -50, 0)
	planes[1]._defPosition = Vector(-70,-50, -70)
	planes[2]._defPosition = Vector(70, -50, 70)
	planes[3]._defPosition = Vector(80, -50, 0)
	planes[4]._defPosition = Vector(80, -50, 0)
	planes[5]._defPosition = Vector(70, -50, -70)
	return planes


# check = Hexapod()
# check.calcAdvancedXYZ(0.1)
# print(check._limbsList[0]._x, check._limbsList[0]._y, check._limbsList[0]._z)
# print(check._limbsList[1]._x, check._limbsList[1]._y, check._limbsList[1]._z)
# print(check._limbsList[2]._x, check._limbsList[2]._y, check._limbsList[2]._z)
# print(check._limbsList[3]._x, check._limbsList[3]._y, check._limbsList[3]._z)
# print(check._limbsList[4]._x, check._limbsList[4]._y, check._limbsList[4]._z)
# print(check._limbsList[5]._x, check._limbsList[5]._y, check._limbsList[5]._z)
