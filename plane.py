import math

LINK_COXA = 0
LINK_FEMUR = 1
LINK_TIBIA = 2

class LinkInfo:
    #  Current link state
    angle = 0.0
    #  Link configuration
    length = 0
    zero_rotate = 0
    min_angle = 0
    max_angle = 0

class point_3d_t:
    x = 0.0
    y = 0.0
    z = 0.0

class LimbInfo:
    position = point_3d_t
    # path_3d_t  movement_path
    # link_info_t links[3]
    links = [LinkInfo(),LinkInfo(),LinkInfo()]

planes = [LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo(),LimbInfo()]

def RAD_TO_DEG(rad):
    return ((rad) * 180.0 / math.pi)

def DEG_TO_RAD(deg):
    return ((deg) * math.pi / 180.0)

def set_point(index,x,y,z):
    global planes
    obj = planes[index]
    obj.position.x = x
    obj.position.y = y
    obj.position.z = z

# ***************************************************************************
# @brief  Calculate angles
# @param  info: limb info @ref limb_info_t
# @return true - calculation success, false - no
# ***************************************************************************
def kinematic_calculate_angles(pindex):
    global planes
    info = planes[pindex]
    print(info.links[0].length)
    coxa_zero_rotate_deg = info.links[LINK_COXA].zero_rotate
    femur_zero_rotate_deg = info.links[LINK_FEMUR].zero_rotate
    tibia_zero_rotate_deg = info.links[LINK_TIBIA].zero_rotate
    coxa_length = info.links[LINK_COXA].length
    femur_length = info.links[LINK_FEMUR].length
    tibia_length = info.links[LINK_TIBIA].length
    x = info.position.x
    y = info.position.y
    z = info.position.z
    # Move to (X*, Y*, Z*) coordinate system - rotate
    coxa_zero_rotate_rad = DEG_TO_RAD(coxa_zero_rotate_deg)
    x1 = x * math.cos(coxa_zero_rotate_rad) + z * math.sin(coxa_zero_rotate_rad)
    y1 = y
    z1 = -x * math.sin(coxa_zero_rotate_rad) + z * math.cos(coxa_zero_rotate_rad)
    # Calculate COXA angle
    coxa_angle_rad = math.atan2(z1, x1)
    info.links[LINK_COXA].angle = RAD_TO_DEG(coxa_angle_rad)
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
    alpha = math.acos( (b * b + c * c - a * a) / (2 * b * c))
    gamma = math.acos( (a * a + b * b - c * c) / (2 * a * b))
    # Calculate FEMUR and TIBIA angle
    info.links[LINK_FEMUR].angle = femur_zero_rotate_deg - RAD_TO_DEG(alpha) - RAD_TO_DEG(fi)
    info.links[LINK_TIBIA].angle = RAD_TO_DEG(gamma) - tibia_zero_rotate_deg
    # print(info.links[LINK_COXA].angle)
    # print(info.links[LINK_FEMUR].angle)
    # print(info.links[LINK_TIBIA].angle)
    # Check angles
    if (info.links[LINK_COXA].angle < info.links[LINK_COXA].min_angle or info.links[LINK_COXA].angle > info.links[LINK_COXA].max_angle):
        return False
    if (info.links[LINK_FEMUR].angle < info.links[LINK_FEMUR].min_angle or info.links[LINK_FEMUR].angle > info.links[LINK_FEMUR].max_angle):
        return False
    if (info.links[LINK_TIBIA].angle < info.links[LINK_TIBIA].min_angle or info.links[LINK_TIBIA].angle > info.links[LINK_TIBIA].max_angle):
        return False
    return True

def kca(info):
    kinematic_calculate_angles(info)



planes[0].links[LINK_COXA].length = 46.7
planes[0].links[LINK_COXA].zero_rotate = 35.8
planes[0].links[LINK_COXA].min_angle = -90
planes[0].links[LINK_COXA].max_angle = 90

planes[0].links[LINK_FEMUR].length = 90
planes[0].links[LINK_FEMUR].zero_rotate = 90
planes[0].links[LINK_FEMUR].min_angle = 0
planes[0].links[LINK_FEMUR].max_angle = 180

planes[0].links[LINK_TIBIA].length = 122.558
planes[0].links[LINK_TIBIA].zero_rotate = 16.7
planes[0].links[LINK_TIBIA].min_angle = 0
planes[0].links[LINK_TIBIA].max_angle = 180


planes[1].links[LINK_COXA].length = 46.7
planes[1].links[LINK_COXA].zero_rotate = 0
planes[1].links[LINK_COXA].min_angle = -50
planes[1].links[LINK_COXA].max_angle = 50

planes[1].links[LINK_FEMUR].length = 90
planes[1].links[LINK_FEMUR].zero_rotate = 90
planes[1].links[LINK_FEMUR].min_angle = 0
planes[1].links[LINK_FEMUR].max_angle = 180

planes[1].links[LINK_TIBIA].length = 122.558
planes[1].links[LINK_TIBIA].zero_rotate = 16.7
planes[1].links[LINK_TIBIA].min_angle = 0
planes[1].links[LINK_TIBIA].max_angle = 180



planes[2].links[LINK_COXA].length = 46.7
planes[2].links[LINK_COXA].zero_rotate = -35.8
planes[2].links[LINK_COXA].min_angle = -90
planes[2].links[LINK_COXA].max_angle = 90

planes[2].links[LINK_FEMUR].length = 90
planes[2].links[LINK_FEMUR].zero_rotate = 90
planes[2].links[LINK_FEMUR].min_angle = 0
planes[2].links[LINK_FEMUR].max_angle = 180

planes[2].links[LINK_TIBIA].length = 122.558
planes[2].links[LINK_TIBIA].zero_rotate = 16.7
planes[2].links[LINK_TIBIA].min_angle = 0
planes[2].links[LINK_TIBIA].max_angle = 180




planes[3].links[LINK_COXA].length = 46.7
planes[3].links[LINK_COXA].zero_rotate = 35.8
planes[3].links[LINK_COXA].min_angle = -90
planes[3].links[LINK_COXA].max_angle = 90

planes[3].links[LINK_FEMUR].length = 90
planes[3].links[LINK_FEMUR].zero_rotate = 90
planes[3].links[LINK_FEMUR].min_angle = 0
planes[3].links[LINK_FEMUR].max_angle = 180

planes[3].links[LINK_TIBIA].length = 122.558
planes[3].links[LINK_TIBIA].zero_rotate = 16.7
planes[3].links[LINK_TIBIA].min_angle = 0
planes[3].links[LINK_TIBIA].max_angle = 180


planes[4].links[LINK_COXA].length = 46.7
planes[4].links[LINK_COXA].zero_rotate = 0
planes[4].links[LINK_COXA].min_angle = -50
planes[4].links[LINK_COXA].max_angle = 50

planes[4].links[LINK_FEMUR].length = 90
planes[4].links[LINK_FEMUR].zero_rotate = 90
planes[4].links[LINK_FEMUR].min_angle = 0
planes[4].links[LINK_FEMUR].max_angle = 180

planes[4].links[LINK_TIBIA].length = 122.558
planes[4].links[LINK_TIBIA].zero_rotate = 16.7
planes[4].links[LINK_TIBIA].min_angle = 0
planes[4].links[LINK_TIBIA].max_angle = 180



planes[5].links[LINK_COXA].length = 46.7
planes[5].links[LINK_COXA].zero_rotate = -35.8
planes[5].links[LINK_COXA].min_angle = -90
planes[5].links[LINK_COXA].max_angle = 90

planes[5].links[LINK_FEMUR].length = 90
planes[5].links[LINK_FEMUR].zero_rotate = 90
planes[5].links[LINK_FEMUR].min_angle = 0
planes[5].links[LINK_FEMUR].max_angle = 180

planes[5].links[LINK_TIBIA].length = 122.558
planes[5].links[LINK_TIBIA].zero_rotate = 16.7
planes[5].links[LINK_TIBIA].min_angle = 0
planes[5].links[LINK_TIBIA].max_angle = 180
print("hello")

