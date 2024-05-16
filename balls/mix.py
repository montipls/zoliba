import pygame
import sys
import objects
import main
import vector

class static:

	@staticmethod
	def check_events():
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					#pass
					objects.Object.objects.append(objects.Object(vector.Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					objects.Object.objects.clear()

	@staticmethod
	def create_chain():
		x_start, x_end = 760, 1360
		y = 800
		step = 30
		prev = None
		for x in range(x_start, x_end + 1, step):
			if x == x_start:
				objects.Object.objects.append(objects.Object(vector.Vector(x, y), link=True, fixed=True))
			if x == x_end:
				objects.Object.objects.append(objects.Object(vector.Vector(x, y + 80), link=True, fixed=True))
			else:
				objects.Object.objects.append(objects.Object(vector.Vector(x, y), link=True))

		for l_obj in objects.Object.objects:
			if l_obj.link:
				if prev != None:
					objects.Link(prev, l_obj, step-10).none()
				prev = l_obj

	@staticmethod
	def shoot(t):
		if t % 8 == 0:
			objects.Object.objects.append(objects.Object(vector.Vector(1400, -20), boost=True))

	@staticmethod
	def mouse_ball():
		objects.Object.objects.append(objects.Object(vector.Vector(10, -100), fixed=True, mouse=True))