import math
import time
import pygame
import numpy
from pygame import Vector2

from player import Player


def cast_ray(start_pos: Vector2, angle: float, max_length: float, tilemap: list[tuple[int, int]]) -> float:
    dir: Vector2 = Vector2(-math.sin(angle - math.pi / 2), math.cos(angle - math.pi / 2))

    if dir.x == 0:
        dir.x = 0.001
    elif dir.y == 0:
        dir.y = 0.001

    unit_step_size = Vector2(
        math.sqrt(1 + (dir.y / dir.x) * (dir.y / dir.x)),
        math.sqrt(1 + (dir.x / dir.y) * (dir.x / dir.y))
    )

    map_check: Vector2 = Vector2(int(start_pos.x), int(start_pos.y))
    step_length: Vector2 = Vector2()
    step: Vector2 = Vector2()

    if dir.x < 0:
        step.x = -1
        step_length.x = (start_pos.x - map_check.x) * unit_step_size.x
    else:
        step.x = 1
        step_length.x = (map_check.x + 1 - start_pos.x) * unit_step_size.x

    if dir.y < 0:
        step.y = -1
        step_length.y = (start_pos.y - map_check.y) * unit_step_size.y
    else:
        step.y = 1
        step_length.y = (map_check.y + 1 - start_pos.y) * unit_step_size.y

    tile_found: bool = False
    distance: float = 0.0
    while not tile_found and distance < max_length:
        if step_length.x < step_length.y:
            map_check.x += step.x
            distance = step_length.x
            step_length.x += unit_step_size.x
        else:
            map_check.y += step.y
            distance = step_length.y
            step_length.y += unit_step_size.y
        
        if (map_check.x, map_check.y) in tilemap:
            tile_found = True
    
    if tile_found and distance < max_length:
        return distance
    else:
        return max_length


W, H = (640, 480)
CTR = (W / 2, H / 2)
win = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED)
pygame.mouse.set_visible(0)
pygame.event.set_grab(True)
clock = pygame.time.Clock()

MAP: set[tuple[int, int]] = {(30, 21), (30, 20), (30, 19), (29, 18), (28, 18), (27, 18), (26, 19), (26, 20), (26, 21), (31, 22), (32, 22), (33, 22), (34, 22), (35, 22), (36, 23), (36, 24), (25, 22), (21, 22), (20, 23), (20, 24), (35, 29), (34, 29), (33, 29), (32, 29), (31, 29), (30, 29), (29, 29), (28, 29), (27, 29), (26, 29), (25, 29), (20, 28), (20, 27), (20, 26), (20, 25), (36, 22), (38, 27), (39, 26), (39, 25), (39, 24), (39, 23), (39, 22), (39, 21), (39, 20), (39, 19), (39, 18), (38, 17), (37, 17), (36, 17), (35, 17), (34, 17), (33, 17), (33, 19), (36, 20), (33, 20), (36, 19), (37, 28), (36, 29), (35, 25), (34, 26), (28, 23), (29, 24), (27, 24), (28, 25), (20, 31), (20, 32), (32, 16), (31, 15), (30, 15), (29, 15), (28, 15), (27, 15), (26, 15), (25, 15), (24, 15), (23, 15), (22, 15), (21, 15), (20, 16), (20, 17), (20, 18), (20, 19), (20, 20), (20, 21), (21, 33), (22, 34), (23, 34), (24, 34), (25, 34), (26, 34), (27, 34), (28, 33), (29, 32), (30, 32), (31, 32), (32, 32), (33, 32), (34, 32), (42, 29), (42, 30), (42, 31), (41, 32), (40, 32), (38, 32), (37, 32), (36, 32), (35, 32), (40, 27), (41, 28), (40, 33), (39, 34), (38, 34), (37, 34), (36, 34), (35, 34), (34, 34), (33, 34), (32, 34), (31, 34), (30, 34), (29, 35), (28, 36), (27, 36), (26, 36), (25, 36), (24, 36), (23, 36), (22, 36), (21, 36), (20, 35), (19, 34), (18, 33), (18, 32), (18, 31), (18, 30), (18, 29), (19, 29), (21, 30)}
TILE_SIZE = 40
TILE_COLOR = 100
PIXEL_WIDTH = math.ceil(W / 158)
MAX_RAY_LENGTH = 10

player: Player = Player(Vector2(28, 20))
mouse_angle = 0
ray_angles = numpy.arange(-math.pi / 4, math.pi / 4, 0.01)
ray_angle_count = len(ray_angles)

timer = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_angle += event.rel[0] / 100

    delta = time.time() - timer
    timer = time.time()
    pygame.mouse.set_pos(CTR)
    player.update_position(mouse_angle, MAP, delta)

    rays: list[Vector2] = []
    for i in ray_angles:
        rays.append(cast_ray(player.position, mouse_angle + i, MAX_RAY_LENGTH, MAP))

    win.fill((0, 0, 10))
    pygame.draw.rect(win, (100, 100, 100), (0, H / 2, W, H / 2))
    for i, ray in enumerate(rays):
        w = math.ceil(W / ray_angle_count)
        h = H / ray + 1
        x = i * w
        y = (H - h) / 2
        color = TILE_COLOR / (ray + 1)
        pygame.draw.rect(win, (color, color, color), (x, y, w, h))
    pygame.display.update()
    if delta != 0:
        print(1 / delta)