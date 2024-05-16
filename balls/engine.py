import pygame
import vector
import objects
import math

class Solver:
	gravity = vector.Vector(0, 0.3)

	def __init__(self, master):
		self.master = master

	def update(self, dt = float):
		sub_steps = 2
		sub_dt = dt / sub_steps

		for i in range(sub_steps):
			self.apply_gravity()
			self.update_positions(sub_dt)
			self.apply_constraint()
			self.solve_collisions(sub_dt)
			for link in objects.Link.links:
				link.apply(sub_dt)

	def update_positions(self, dt = float):
		for obj in objects.Object.objects:
			obj.update_position(dt)
			if obj.position_current()[1] > self.master.win_size[1] + obj.radius and not obj.link:
				objects.Object.objects.remove(obj)
			elif obj.position_current()[0] > self.master.win_size[0] + obj.radius or obj.position_current()[0] < -obj.radius:
				objects.Object.objects.remove(obj)

	def apply_gravity(self):
		for obj in objects.Object.objects:
			if not obj.fixed:
				obj.accelerate(Solver.gravity)

	def apply_constraint(self):
		center = vector.Vector(self.master.win_size[0] / 2 -1000, 5000)
		radius = 5230
		for obj in objects.Object.objects:
			v = center - obj.position_current
			dist = math.sqrt(v.x * v.x + v.y * v.y)
			if dist > (radius - obj.radius):
				n = v / dist
				if not obj.fixed:
					obj.position_current = center - vector.Vector(n()[0] * (radius - obj.radius), n()[1] * (radius - obj.radius))

	def solve_collisions(self, dt):
		response_coef = 0.75
		objects_count = len(objects.Object.objects)

		for i in range(objects_count):
			object_1 = objects.Object.objects[i]

			for k in range(i + 1, objects_count):
				object_2 = objects.Object.objects[k]
				v = object_1.position_current - object_2.position_current
				dist2 = v.x * v.x + v.y * v.y
				min_dist = object_1.radius + object_2.radius

				if dist2 < min_dist * min_dist:
					dist = math.sqrt(dist2)
					n = v / dist
					mass_ratio_1 = object_1.radius / (object_1.radius + object_2.radius)
					mass_ratio_2 = object_2.radius / (object_1.radius + object_2.radius)
					delta = 0.5 * response_coef * (dist - min_dist)
					if not object_1.fixed:
						object_1.position_current -= vector.Vector(n()[0] * (mass_ratio_1 * delta), n()[1] * (mass_ratio_1 * delta))
					if not object_2.fixed:
						object_2.position_current += vector.Vector(n()[0] * (mass_ratio_2 * delta), n()[1] * (mass_ratio_2 * delta))

class Renderer:
	def __init__(self, win):
		self.win = win
	
	def render(self):
		for obj in objects.Object.objects:
			pygame.draw.circle(self.win, obj.color, obj.position_current(), obj.radius)
