import pygame
import vector
import random
import colorsys
import math

class Object:
	objects = []
	hue = 0.5
	i = 0.0001

	def __init__(self, pos, link = False, fixed = False, boost = False, mouse = False):
		self.position_current = pos
		self.position_old = self.position_current
		self.acceleration = vector.Vector(0, 0)
		self.radius = 20
		self.link = link
		if self.link:
			self.radius = 15
		self.fixed = fixed
		self.boost = boost
		self.mouse = mouse
		self.set_color()
		if self.link or self.mouse:
			self.color = (255, 255, 255)
			if self.mouse:
				self.radius = 40
		if self.boost:
			self.accelerate(vector.Vector(0, -10))

	def update_position(self, dt = float):
		if not self.fixed:
			velocity = self.position_current - self.position_old
			self.position_old = self.position_current
			self.position_current = self.position_current + velocity + self.acceleration * dt * dt
			self.acceleration = vector.Vector(0, 0)
		if self.mouse:
			if pygame.mouse.get_pressed()[2]:
				self.position_current = vector.Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
			else:
				self.position_current = vector.Vector(10, -100)
		if not self.mouse and not self.link:
			self.set_color()

	def accelerate(self, acc):
		self.acceleration += acc

	def set_color(self):
		(r, g, b) = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
		R, G, B = int(255 * r), int(255 * g), int(255 * b)
		self.color = (R, G, B)
		self.hue += Object.i
		if self.hue >= 1:
			self.hue = 0

class Link:
	links = []

	def __init__(self, object_1, object_2, target_dist):
		self.object_1 = object_1
		self.object_2 = object_2
		self.target_dist = target_dist
		Link.links.append(self)

	def apply(self, dt):
		axis = self.object_1.position_current - self.object_2.position_current
		dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
		n = axis / dist
		delta = self.target_dist - dist
		if not self.object_1.fixed:
			self.object_1.position_current += vector.Vector(n()[0] * 0.5 * delta * dt, n()[1] * 0.5 * delta * dt)
		if not self.object_2.fixed:
			self.object_2.position_current -= vector.Vector(n()[0] * 0.5 * delta * dt, n()[1] * 0.5 * delta * dt)

	def none(self):
		pass