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

class point_3d_t:
    def __init__(self,x = 0,y = 0,z = 0):
        self._x = x
        self._y = y
        self._z = z

class LimbInfo():
    def __init__(self):
        self._position = point_3d_t()
        self._links = [LinkInfo(),LinkInfo(),LinkInfo()]

        # path_3d_t  movement_path
        # link_info_t links[3]

planes = [LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo()]

def RAD_TO_DEG(rad):
    return ((rad) * 180.0 / math.pi)

def DEG_TO_RAD(deg):
    return ((deg) * math.pi / 180.0)

def set_point(index,x,y,z):
    global planes
    obj = planes[index]
    obj._position._x = x
    obj._position._y = y
    obj._position._z = z

def pos_arm(index, x,y,z):
    set_point(index, x, y ,z)
    kinematic_calculate_angles(index)
    pl = planes[index]
    # print(str(pl._links[0]._angle) + " / " + str(pl._links[1]._angle) + " / " + str(pl._links[2]._angle))
    ant.set_arm_ang(index,pl._links[0]._angle, pl._links[1]._angle, pl._links[2]._angle)

# ***************************************************************************
# @brief  Calculate angles
# @param  info: limb info @ref limb_info_t
# @return true - calculation success, false - no
# ***************************************************************************
def kinematic_calculate_angles(pindex):
    global planes
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

def kca(info):
    kinematic_calculate_angles(info)



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


class Point:
    def __init__(self):
        self._x = 0
        self._y = 0

class pt2:
    def __init__(self):
        self._pt = [Point(),Point(),Point()]
