from limb import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig, ax = plt.subplots(subplot_kw=dict(projection='3d') )

# points = [(1,0,0), (2,2,2), (-1,2,0), (1,2,1)]
# x,y,z = zip(*points)
# ax.scatter(x,y,z, s=100)
plt.ion()
# l1 = plt.plot(x,y,z)
plt.show()
x0 = (0,0,50)
fl = (limb_fl._defPos._x, limb_fl._defPos._z, limb_fl._defPos._y)
ml = (limb_ml._defPos._x, limb_ml._defPos._z, limb_ml._defPos._y)
rl = (limb_rl._defPos._x, limb_rl._defPos._z, limb_rl._defPos._y)
fr = (limb_fr._defPos._x, limb_fr._defPos._z, limb_fr._defPos._y)
mr = (limb_mr._defPos._x, limb_mr._defPos._z, limb_mr._defPos._y)
rr = (limb_rr._defPos._x, limb_rr._defPos._z, limb_rr._defPos._y)
x,y,z = zip(x0,fl)
plt.plot(x,y,z)
x,y,z = zip(x0,ml)
plt.plot(x,y,z)
x,y,z = zip(x0,rl)
plt.plot(x,y,z)
x,y,z = zip(x0,fr)
plt.plot(x,y,z)
x,y,z = zip(x0,mr)
plt.plot(x,y,z)
x,y,z = zip(x0,rr)
plt.plot(x,y,z)
x,y,z = zip(x0,(0,50,50)))
plt.plot(x,y,z)



ran = 11
def bla(num):
	table = []
	# ran = 23
	for i in range(ran):
		tt=round(i/(ran-1),2)
		bot.advanced_trajectory(1.9999,tt)
		point = (tt,round(limbs[num]._position._x,3), round(limbs[num]._position._z,3), round(limbs[num]._position._y,3))
		# print(point)
		table.append(point)
	return(table)
# p_fl = bla(0)
# tt_p,x,y,z = zip(*p_fl)
# plt.plot(x,y,z)
# advanced_trajectory(1.9999,0)


def draw_step(bot:Bot,t_time, curvature):
	global limbs
	points = []
	bot.advanced_trajectory(curvature, t_time)
	for i in range(len(limbs)):
		points.append((limbs[i]._position._x,limbs[i]._position._z,limbs[i]._position._y))
	# print(points)
	x,y,z = zip(*points)
	return ax.scatter(x,y,z)

step = 0
curvature = 1.9999
step_points = draw_step(step, curvature)
def next_step(bot:Bot,curvature):
	global step, step_points
	step += 0.05
	step_points.remove()
	step_points = draw_step(bot,step, curvature)
	if step >= 1:
		change_direction()
		step = 0

def animation(step):
	global step_points
	step_points.remove()
	step_points = draw_step(step, 1.9999)

inc = .5
from threading import Thread
def func():
	global step
	for i in range(40):
		step += 0.05
		print(step)
		draw_step(step, 1.9999)
		sleep(0.5)
		if step >= 1:
			change_direction()
			step = -.05
		# next_step(1.9999)
bot.ch

th = Thread(target=func)
th.start()

draw_step(0,1.9999)



import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as mcoll
import matplotlib.path as mpath

def colorline(
	x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
		linewidth=3, alpha=1.0):
	# Default colors equally spaced on [0,1]:
	if z is None:
		z = np.linspace(0.0, 1.0, len(x))
	# Special case if a single number:
	if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
		z = np.array([z])
	z = np.asarray(z)
	segments = make_segments(x, y)
	lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
							  linewidth=linewidth, alpha=alpha)
	ax = plt.gca()
	ax.add_collection(lc)
	return lc

def make_segments(x, y):
	points = np.array([x, y]).T.reshape(-1, 1, 2)
	segments = np.concatenate([points[:-1], points[1:]], axis=1)
	return segments
N = 10
np.random.seed(101)
x = np.random.rand(N)
y = np.random.rand(N)
fig, ax = plt.subplots()

path = mpath.Path(np.column_stack([x, y]))
verts = path.interpolated(steps=3).vertices
x, y = verts[:, 0], verts[:, 1]
z = np.linspace(0, 1, len(x))
colorline(x, y, z, cmap=plt.get_cmap('jet'), linewidth=2)

plt.show()

x,y,z = zip(x0,(0,50,50))
plt.plot(x,y,z, cmap=plt.get_cmap('jet'))