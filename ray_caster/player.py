import math
import pygame
from pygame import Vector2


class Player:
    def __init__(self, position: Vector2) -> None:
        self.position: Vector2 = position

    def update_position(self, mouse_angle: float, tilemap, dt: float) -> None:
        dir_x, dir_y = -math.sin(mouse_angle - math.pi / 2), math.cos(mouse_angle - math.pi / 2)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.position += Vector2(dir_x, dir_y) * dt
        if keys[pygame.K_a]:
            self.position += Vector2(dir_y, -dir_x)*  dt
        if keys[pygame.K_s]:
            self.position -= Vector2(dir_x, dir_y) * dt
        if keys[pygame.K_d]:
            self.position -= Vector2(dir_y, -dir_x) * dt