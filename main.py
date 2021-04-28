import initant as ant
import plane
import time
import math
ant.def_pos()

def pos_arm(index, x,y,z):
    plane.set_point(index, x, y ,z)
    plane.kinematic_calculate_angles(index)
    pl = plane.planes[index]
    ant.set_arm_ang(index,pl.links[0].angle, pl.links[1].angle, pl.links[2].angle)



# pos_arm(0, 100, -50, 100)
# pos_arm(2, 100, -50, 100)
# pos_arm(3, 100, -50, 100)
# pos_arm(5, 100, -50, 100)

angle = 0
x1 = 100
z1 = 100

while 1:
    x = x1 + (r * math.cos(angle))
    y = z1 + (r + math.sin(angle))
    pos_arm(0, x, 0, y)
    angle = angle + 0.1