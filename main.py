import initant as ant
import plane
from plane import pos_arm,DEG_TO_RAD, RAD_TO_DEG
import time
from emath import sin, cos, atan2, atan, pi, pow, sqrt
ant.df_pos()

# def pos_arm(index, x,y,z):
#     plane.set_point(index, x, y ,z)
#     plane.kinematic_calculate_angles(index)
#     pl = plane.planes[index]
#     # print(str(pl._links[0]._angle) + " / " + str(pl._links[1]._angle) + " / " + str(pl._links[2]._angle))
#     ant.set_arm_ang(index,pl._links[0]._angle, pl._links[1]._angle, pl._links[2]._angle)

pos0 = plane.point_3d_t(150,-25,-20)
pos1 = plane.point_3d_t(150,10,120)


# pos_arm(0, 100, -50, 100)
# pos_arm(2, 100, -50, 100)
# pos_arm(3, 100, -50, 100)
# pos_arm(5, 100, -50, 100)

