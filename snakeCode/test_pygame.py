import pygame
import new_movments
import time


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
(width, height) = (500, 500)
screen = pygame.display.set_mode((width, height))
# surface = pygame.Surface((width, height))
pygame.display.flip()
running = True

new_movments.init_hexapod()

# for x in range(10):
def kek():
	for i in range(11):
		new_movments.move_forward(i / 10)
		# for j in range(6):
		# 	screen.set_at((int(new_movments.limbs_list[j].position.x), int(new_movments.limbs_list[j].position.y)), (255, 255, 255))
		# print(new_movments.limbs_list[0].position.x, new_movments.limbs_list[0].position.y, new_movments.limbs_list[0].position.z)
		if i > 0:
			for n in range(6):
				x0 = int(tmp[n].position.x)
				z0 = int(tmp[n].position.z)
				x1 = int(new_movments.limbs_list[n].position.x)
				z1 = int(new_movments.limbs_list[n].position.z)
				x0 = 250 + x0
				z0 = 250 + z0
				x1 = 250 + x1
				z1 = 250 + z1
				pygame.draw.line(screen, (255, 255, 255), (x0, z0), (x1, z1))
		tmp = new_movments.limbs_list.copy()
		# pygame.time.wait(1000)

def puk():
	for j in range(6):
		x1 = int(new_movments.MotionConfig2.start_position[j].x)
		z1 = int(new_movments.MotionConfig2.start_position[j].z)
		x1 = 250 + x1
		z1 = 250 + z1
		screen.set_at((x1, z1), (255, 0, 0))
		screen.set_at((x1 + 1, z1), (255, 0, 0))
		screen.set_at((x1 - 1, z1), (255, 0, 0))
		screen.set_at((x1, z1 + 1), (255, 0, 0))
		screen.set_at((x1, z1 - 1), (255, 0, 0))
		# screen.set_at((x1, z1), (255, 0, 0))
		# screen.set_at((x1, z1), (255, 0, 0))
		# screen.set_at((x1, z1), (255, 0, 0))
		# screen.set_at((x1, z1), (255, 0, 0))
		# print(new_movments.limbs_list[0].position.x, new_movments.limbs_list[0].position.y, new_movments.limbs_list[0].position.z)
		# if i > 0:
		# 	for n in range(6):
		# 		x0 = int(tmp[n].position.x)
		# 		z0 = int(tmp[n].position.z)
		# 		x1 = int(new_movments.limbs_list[n].position.x)
		# 		z1 = int(new_movments.limbs_list[n].position.z)
		# 		x0 = 250 + x0
		# 		z0 = 250 + z0
		# 		x1 = 250 + x1
		# 		z1 = 250 + z1
		# 		pygame.draw.line(screen, (255, 255, 255), (x0, z0), (x1, z1))
		# tmp = new_movments.limbs_list.copy()

kek()
puk()
# for i in range(10):
# 	# screen.set_at((10 * i, 10 * i), (255, 255, 255))
# 	# (x1, y1) = (10 * i, 10 * i)
# 	if i > 0:
# 		(x1, y1) = (10 * i, 10 * i)
# 		pygame.draw.line(screen, (255, 255, 255), (x0, y0), (x1, y1))
# 	(x0, y0) = (10 * i, 10 * i)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False