import pygame
import sys
import mix
import engine
import objects
import vector
import time

class App:
	def __init__(self):
		pygame.init()
		self.win_size = (1920, 1080)
		self.win_title = 'Monti\'s Graphics Engine'
		self.clock = pygame.time.Clock()
		self.window_init()
		self.create_scene()
		self.timer = 0

	def create_scene(self):
		mix.static.create_chain()
		mix.static.mouse_ball()
		self.solver = engine.Solver(self)
		self.renderer = engine.Renderer(self.win)
		click = pygame.mouse.get_pressed()

	def update_scene(self):
		self.solver.update(1)
		self.renderer.render()
		self.timer += 1
		if self.timer > 100:
			self.timer = 1
		mix.static.shoot(self.timer)

	def window_init(self):
		self.win = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN)
		pygame.display.set_caption(self.win_title)

	def redraw_window(self):
		pygame.mouse.set_visible(0)
		self.win.fill((0, 0, 0))
		self.update_scene()
		pygame.display.update()

	def run(self):
		while True:
			mix.static.check_events()
			self.redraw_window()
			self.clock.tick(60)

if __name__ == '__main__':
	app = App()
	app.run()
