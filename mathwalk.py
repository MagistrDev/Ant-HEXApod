import initant as ant
import plane
from plane import *
import time
from math import *

# class sequence_iteration_t:
#     point_3d_t  point_list[SUPPORT_LIMB_COUNT];
#     path_type_t path_list[SUPPORT_LIMB_COUNT];
#     uint32_t    smooth_point_count;


# typedef struct {
	
#     bool is_sequence_looped;
#     uint32_t main_sequence_begin;
#     uint32_t finalize_sequence_begin;

#     uint32_t total_iteration_count;
#     sequence_iteration_t iteration_list[15];
#     sequence_id_t available_sequences[SUPPORT_SEQUENCE_COUNT];
	
# } sequence_info_t;
class MathWalk:
	def XYZ_LINAR(t, pos0, pos1):
		ret = point_3d_t()
		ret._x = t * (pos1._x - pos0._x) / 180.0 + pos0._x
		ret._y = t * (pos1._y - pos0._y) / 180.0 + pos0._y
		ret._z = t * (pos1._z - pos0._z) / 180.0 + pos0._z
		return ret
	def YZ_ARC_Y_LINEAR(t, pos0, pos1):
		ret = point_3d_t()
		R = sqrt(pos0._x * pos0._x + pos0._z * pos0._z)
		atan0 = degrees(atan2(pos0._x, pos0._z))
		atan1 = degrees(atan2(pos1._x, pos1._z))
		t_mapped_rad = radians(t * (atan1 - atan0) / 180.0 + atan0)
		ret._x = R * sin(t_mapped_rad); # Circle Y
		ret._y = t * (pos1._y - pos0._y) / 180.0 + pos0._y
		ret._z = R * cos(t_mapped_rad); # Circle X
		return ret
	def XZ_ELLIPTICAL_Y_SINUS(t, pos0, pos1):
		ret = point_3d_t()
		a = (pos1._z - pos0._z) / 2.0
		b = (pos1._x - pos0._x)
		c = (pos1._y - pos0._y)
		ret._x = b * sin(radians(180.0 - t)) + pos0._x # circle Y
		ret._y = c * sin(radians(t)) + pos0._y
		ret._z = a * cos(radians(180.0 - t)) + pos0._z + a
		return ret



pos0_f = point_3d_t(90,-120,30)
pos1_f = point_3d_t(90,-120,100)
pose_f = point_3d_t(90, 10,100)

pos0_m = point_3d_t(90,-120,-40)
pos1_m = point_3d_t(90,-120,20)
pose_m = point_3d_t(90, 10,20)

pos0_b = point_3d_t(90,-120,-150)
pos1_b = point_3d_t(90,-120,-90)
pose_b = point_3d_t(90, 10,-90)

inc = 5
def walk_up():
	while 1:
		phathe1()
		phathe2()

# подъем
# st1_se = XZ_ELLIPTICAL_Y_SINUS(t, pos0, pos1)

# перемещение 
# st1_m =  XYZ_LINAR(t, pos_sub, pos0)

def phathe1():
	for t in range(1,180,inc):
		ph1_f = XZ_ELLIPTICAL_Y_SINUS(t, pos0_f, pose_f)
		ph1_m = XZ_ELLIPTICAL_Y_SINUS(t, pos0_m, pose_m)
		ph1_b = XZ_ELLIPTICAL_Y_SINUS(t, pos0_b, pose_b)
		ph2_f = XYZ_LINAR(t, pos1_f, pos0_f)
		ph2_m = XYZ_LINAR(t, pos1_m, pos0_m)
		ph2_b = XYZ_LINAR(t, pos1_b, pos0_b)
		pos_arm(0, ph1_f._x,ph1_f._y, ph1_f._z)
		pos_arm(4, ph1_m._x,ph1_m._y, ph1_m._z)
		pos_arm(2, ph1_b._x,ph1_b._y, ph1_b._z)
		pos_arm(3, ph2_f._x,ph2_f._y, ph2_f._z)
		pos_arm(1, ph2_m._x,ph2_m._y, ph2_m._z)
		pos_arm(5, ph2_b._x,ph2_b._y, ph2_b._z)

def phathe2():
	for t in range(1,180,inc):
		ph1_f = XZ_ELLIPTICAL_Y_SINUS(t, pos0_f, pose_f)
		ph1_m = XZ_ELLIPTICAL_Y_SINUS(t, pos0_m, pose_m)
		ph1_b = XZ_ELLIPTICAL_Y_SINUS(t, pos0_b, pose_b)
		ph2_f = XYZ_LINAR(t, pos1_f, pos0_f)
		ph2_m = XYZ_LINAR(t, pos1_m, pos0_m)
		ph2_b = XYZ_LINAR(t, pos1_b, pos0_b)
		pos_arm(3, ph1_f._x,ph1_f._y, ph1_f._z)
		pos_arm(1, ph1_m._x,ph1_m._y, ph1_m._z)
		pos_arm(5, ph1_b._x,ph1_b._y, ph1_b._z)
		pos_arm(0, ph2_f._x,ph2_f._y, ph2_f._z)
		pos_arm(4, ph2_m._x,ph2_m._y, ph2_m._z)
		pos_arm(2, ph2_b._x,ph2_b._y, ph2_b._z)

for t in range(1,180,inc):
	ph1_m = XZ_ELLIPTICAL_Y_SINUS(t, pos0_m, pose_m)
	pos_arm(4, ph1_m._x,ph1_m._y, -ph1_m._z)

for t in range(1,180,inc):
	pt = XYZ_LINAR(t, st, end)
	pos_arm(0, pt._x, pt._y, pt._z)
	print(pt._x, pt._y, pt._z)
	sleep(.01)

def set_default_pos():
	pos_arm(0, -150, -80, -80)
	pos_arm(1, -150, -80, 0)
	pos_arm(2, -150, -80, 80)
	pos_arm(3, 150, -80, 80)
	pos_arm(4, 150, -80, 0)
	pos_arm(5, 150, -80, -80)

# set_default_pos()