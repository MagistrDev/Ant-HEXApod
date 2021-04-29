import initant as ant
import plane
import time
import math
ant.def_pos()

def pos_arm(index, x,y,z):
    plane.set_point(index, x, y ,z)
    plane.kinematic_calculate_angles(index)
    pl = plane.planes[index]
    ant.set_arm_ang(index,pl._links[0]._angle, pl._links[1]._angle, pl._links[2]._angle)



# pos_arm(0, 100, -50, 100)
# pos_arm(2, 100, -50, 100)
# pos_arm(3, 100, -50, 100)
# pos_arm(5, 100, -50, 100)

