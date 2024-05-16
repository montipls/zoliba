import pygame
import math

from particle import ParticleSystem

W, H = 50, 30
win = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

smoke = ParticleSystem(W, H, 10.0, 3000, spread=6)
smoke.add_particles(15000)

def narrow(min_val: int, val: int, max_val: int) -> int:
    return max(min_val, min(val, max_val))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    smoke.update()
    matrix = smoke.matrix

    win.fill((0, 0, 0))

    for pos in matrix.keys():
        y, x = pos
        count = matrix[pos]
        step = 5
        r = narrow(0, math.floor(step * count), 255)
        g = narrow(0, math.floor(step * count) - 200, 255)
        b = narrow(0, math.floor(step * count) - 400, 255)
        win.set_at((x, H-y), (r, g, b))

    pygame.display.flip()
    clock.tick(60)