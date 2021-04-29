import initant as ant
import plane
from plane import DEG_TO_RAD, RAD_TO_DEG
import time
from math import sin, cos, atan2, atan, pi, pow, sqrt

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

def XYZ_LINAR(t, pos0, pos1):
	ret = plane.point_3d_t()
	ret._x = t * (pos1._x - pos0._x) / 180.0 + pos0._x
	ret._y = t * (pos1._y - pos0._y) / 180.0 + pos0._y
	ret._z = t * (pos1._z - pos0._z) / 180.0 + pos0._z
	return ret

def YZ_ARC_Y_LINEAR(t, pos0, pos1):
	ret = plane.point_3d_t()
	R = sqrt(pos0._x * pos0._x + pos0._z * pos0._z)
	atan0 = RAD_TO_DEG(atan2(pos0._x, pos0._z))
	atan1 = RAD_TO_DEG(atan2(pos1._x, pos1._z))
	t_mapped_rad = DEG_TO_RAD(t * (atan1 - atan0) / 180.0 + atan0)
	ret._x = R * sin(t_mapped_rad); # Circle Y
	ret._y = t * (pos1._y - pos0._y) / 180.0 + pos0._y
	ret._z = R * cos(t_mapped_rad); # Circle X
	return ret

def XZ_ELLIPTICAL_Y_SINUS(t, pos0, pos1):
	ret = plane.point_3d_t()
	a = (pos1._z - pos0._z) / 2.0
	b = (pos1._x - pos0._x)
	c = (pos1._y - pos0._y)
	ret._x = b * sin(DEG_TO_RAD(180.0 - t)) + pos0._x # circle Y
	ret._y = c * sin(DEG_TO_RAD(t)) + pos0._y
	ret._z = a * cos(DEG_TO_RAD(180.0 - t)) + pos0._z + a
	return ret

for t in range(181):
	# rr = XYZ_LINAR(t, pos0, pos1)
	rr = XZ_ELLIPTICAL_Y_SINUS(t, pos0, pos1)
	print ("x-"+str(rr._x)+"\t\ty-"+str(rr._y)+"\t\tz-"+str(rr._z))