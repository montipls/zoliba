import pygame
import sys
import math
import json

from vector import Vector
from const import WINDOW_SIZE, WALL_COLOR, STRING_COLOR, GRAVITY

pygame.init()

arrow_container = []
landed_arrow_container = []
hits = []
interaction = 'none'
pull_strength = 0
won = False
level = 1
level_label = f'{'0' * (3 - len(str(level)))}{level}'
completed_levels = []
collected_coins = []
coins = 0
assisted = False
font = pygame.font.Font('font/Hack.ttf', 22)
small_font = pygame.font.Font('font/Hack.ttf', 16)
lastangle = math.radians(45)
background_x_1 = 0
background_x_2 = WINDOW_SIZE[0]


try:
    with open(f'levels/{level_label}.json') as file:
        map = json.load(file)
except FileNotFoundError:
    map = {
        "walls": [],
        "targets": [],
        "coins": [],
        "player": {
            "x": WINDOW_SIZE[0] / 2,
            "y": WINDOW_SIZE[1] / 2
        }
    }
player_pos = Vector(map["player"]["x"], map["player"]["y"])
bow_point_1 = (Vector(math.cos(lastangle) * -20, math.sin(lastangle) * 20) + player_pos).true()
bow_point_2 = (Vector(math.cos(lastangle) * 20, math.sin(lastangle) * -20) + player_pos).true()

if __name__ == '__main__':
    class Arrow:
        def __init__(self, strength: float, shooting_angle: float) -> None:
            self.position = player_pos
            self.position_old = self.position
            self.acceleration = Vector(0, 0)
            self.strength = strength
            self.angle = shooting_angle
            self.image = pygame.image.load('img/arrow.png').convert_alpha()
            self.landed = False
            self.tip = self.position + Vector(11 * math.cos(self.angle), 11 * math.sin(self.angle))

        def update_position(self) -> None:
            velocity = self.position - self.position_old
            self.angle = math.atan2(self.position[1] - self.position_old[1], self.position[0] - self.position_old[0])
            self.position_old = self.position
            self.position = self.position + velocity + self.acceleration
            self.tip = self.position + Vector(11 * math.cos(self.angle), 11 * math.sin(self.angle))
            self.acceleration = Vector(0, 0)

        def neutralize(self) -> None:
            self.position_old = self.position
            self.accelerate(Vector(math.cos(self.angle), math.sin(self.angle)) * 1)

        def accelerate(self, acc: Vector) -> None:
            self.acceleration += acc


    def shoot_arrow(strength: float, angle: float) -> None:
        arrow = Arrow(strength, angle)
        arrow.accelerate(Vector(math.sin(arrow.angle), math.cos(arrow.angle)) * arrow.strength)
        arrow_container.append(arrow)


    def rotate_center(image: pygame.Surface, angle) -> pygame.Surface:
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    

    def blit_rotate(surf: pygame.Surface, image: pygame.Surface, pos: tuple[float, float], angle: float) -> None:
        image_rect = image.get_rect(center = (pos[0], pos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)


    def availability(cost: int) -> tuple[int, int, int]:
        if coins >= cost:
            return (255, 255, 255)
        return (80, 80, 80)


    win = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN | pygame.SCALED)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Boltz')

    endscreen_png = pygame.image.load('img/endscr.png').convert_alpha()
    coin_png = pygame.image.load('img/coin.png').convert_alpha()
    player_png = pygame.image.load('img/player.png').convert_alpha()
    arrow_png = pygame.image.load('img/arrow.png').convert_alpha()
    target_png = pygame.image.load('img/target.png').convert_alpha()
    target_hit_png = pygame.image.load('img/target_hit.png').convert_alpha()
    background_png = pygame.image.load('img/background.png').convert_alpha()
    transparent_coin_png = pygame.image.load('img/transparent_coin.png').convert_alpha()

    while True:
        mouse_position = pygame.mouse.get_pos()
        angle = math.atan2(mouse_position[0] - player_pos[0], mouse_position[1] - player_pos[1])

        clock.tick(120)

        background_x_1 -= 0.1
        background_x_2 -= 0.1

        if background_x_1 <= 0 and background_x_2 < background_x_1:
            background_x_2 = background_x_1 + WINDOW_SIZE[0]
        elif background_x_2 <= 0 and background_x_1 < background_x_2:
            background_x_1 = background_x_2 + WINDOW_SIZE[0]

        if len(map["targets"]) == len(hits):
            won = True
            interaction = 'none'
        else:
            landed_arrows = 0
            for arrow in reversed(landed_arrow_container):
                landed_arrows += 1
                if landed_arrows > 50:
                    landed_arrow_container.remove(arrow)
                    arrow_container.remove(arrow)
                    break

        if interaction != 'pull':
            if math.dist(player_pos.true(), mouse_position) < 30:
                interaction = 'hover'
            else:
                interaction = 'none'
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if interaction == 'hover' and not won:
                    interaction = 'pull'
            if event.type == pygame.MOUSEBUTTONUP:
                if interaction == 'pull':
                    if math.dist(player_pos.true(), mouse_position) < 30:
                        interaction = 'hover'
                    else:
                        interaction = 'none'
                    if pull_strength > 0:
                        shoot_arrow(pull_strength, angle + math.pi)
                        if assisted:
                            assisted = False
                    pull_strength = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and won:
                    if len(arrow_container) == 0:
                        won = False
                        hits = []
                if event.key == pygame.K_n:
                    level += 1
                    level_label = f'{'0' * (3 - len(str(level)))}{level}'
                    try:
                        with open(f'levels/{level_label}.json') as file:
                            map = json.load(file)
                    except FileNotFoundError:
                        map = {
                            "walls": [],
                            "targets": [],
                            "coins": [],
                            "player": {
                                "x": WINDOW_SIZE[0] / 2,
                                "y": WINDOW_SIZE[1] / 2
                            }
                        }
                    player_pos = Vector(map["player"]["x"], map["player"]["y"])
                    bow_point_1 = (Vector(math.cos(lastangle) * -20, math.sin(lastangle) * 20) + player_pos).true()
                    bow_point_2 = (Vector(math.cos(lastangle) * 20, math.sin(lastangle) * -20) + player_pos).true()
                    won = False
                    hits = []
                if event.key == pygame.K_1 and not assisted:
                    if coins >= 5:
                        assisted = True
                        coins -= 5
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        if interaction == 'pull':
            pull_strength = min((math.dist(player_pos.true(), mouse_position) // 1.5) / 10, 10)
            lastangle = angle
            bow_point_1 = (Vector(math.cos(lastangle) * -20, math.sin(lastangle) * 20) + player_pos).true()
            bow_point_2 = (Vector(math.cos(lastangle) * 20, math.sin(lastangle) * -20) + player_pos).true()
        elif interaction == 'hover':
            pygame.mouse.set_cursor(pygame.cursors.broken_x)
        elif interaction == 'none':
            pygame.mouse.set_cursor()

        win.blit(background_png, (background_x_1, 0))
        win.blit(background_png, (background_x_2, 0))
        
        for arrow in arrow_container:
            if arrow.position[0] > WINDOW_SIZE[0] or arrow.position[1] > WINDOW_SIZE[1]:
                arrow_container.remove(arrow)
                if arrow in landed_arrow_container:
                    landed_arrow_container.remove(arrow)
                continue
                
            if not arrow.landed and not won:
                for target in map["targets"]:
                    if arrow.landed:
                        continue
                    target_coords = (target["coords"]["x"], target["coords"]["y"])
                    if math.dist(target_coords, arrow.tip.true()) <= target["radius"]:
                        arrow.landed = True
                        arrow.neutralize()
                        landed_arrow_container.append(arrow)
                        if not target in hits:
                            hits.append(target)

            if arrow.landed and won:
                try:
                    for coin in map["coins"]:
                        if coin in collected_coins:
                            continue
                        if math.dist((coin["x"], coin["y"]), arrow.tip.true()) <= 10:
                            coins += 1
                            collected_coins.append(coin)
                except KeyError:
                    pass

            if not arrow.landed and not won:
                for wall in map["walls"]:
                    if arrow.landed:
                        continue
                    wall_coords = (wall["coords"]["x"], wall["coords"]["y"])
                    wall_size = (wall["size"]["width"], wall["size"]["height"])
                    if wall_coords[0] <= arrow.tip[0] <= wall_coords[0] + wall_size[0]:
                        if wall_coords[1] <= arrow.tip[1] <= wall_coords[1] + wall_size[1]:
                            arrow.landed = True
                            arrow.neutralize()
                            landed_arrow_container.append(arrow)
            
            if not arrow.landed or won:
                arrow.accelerate(GRAVITY)
                arrow.update_position()
            
            blit_rotate(win, arrow.image,
                        (arrow.position[0] - (4 * math.cos(arrow.angle)),
                        arrow.position[1] - (4 * math.sin(arrow.angle))),
                        math.degrees(-arrow.angle))
            
        try:
            for coin in map["coins"]:
                if coin not in collected_coins:
                    if not won:
                        win.blit(transparent_coin_png, (coin["x"] - 10, coin["y"] - 10))
                    else:
                        if len(arrow_container) != 0:
                            win.blit(coin_png, (coin["x"] - 10, coin["y"] - 10))
        except KeyError:
            pass

        if not won:
            for wall in map["walls"]:
                pygame.draw.rect(win, WALL_COLOR, (wall["coords"]["x"], wall["coords"]["y"], wall["size"]["width"], wall["size"]["height"]))
            for target in map["targets"]:
                if not target in hits:
                    win.blit(target_png, (target["coords"]["x"] - 20, target["coords"]["y"] - 20))
                else:
                    win.blit(target_hit_png, (target["coords"]["x"] - 20, target["coords"]["y"] - 20))
            if interaction == 'pull':
                pygame.draw.line(win, STRING_COLOR, bow_point_1,
                    (player_pos[0] + math.sin(angle) * pull_strength * 15, 
                    player_pos[1] + math.cos(angle) * pull_strength * 15))
                pygame.draw.line(win, STRING_COLOR, bow_point_2,
                    (player_pos[0] + math.sin(angle) * pull_strength * 15, 
                    player_pos[1] + math.cos(angle) * pull_strength * 15))
                if assisted and pull_strength != 0:
                    assist = Arrow(pull_strength, angle + math.pi)
                    assist.accelerate(Vector(math.sin(assist.angle), math.cos(assist.angle)) * pull_strength)
                    for step in range(8, 70):
                        assist.accelerate(GRAVITY)
                        assist.update_position()
                        if step % 7 == 0 and step != 0:
                            pygame.draw.circle(win, (150, 150, 150), (assist.tip[0], assist.tip[1]), 2)
                if not assisted:
                    pull_strength_text = small_font.render('power: {:.1f}'.format(pull_strength), True, (255, 255, 255))
                    angle_text = small_font.render('angle: {:.1f}°'.format(math.degrees(angle)), True, (255, 255, 255))
                    win.blit(pull_strength_text, (mouse_position[0] + 10, mouse_position[1] + 10))
                    win.blit(angle_text, (mouse_position[0] + 10, mouse_position[1] + 30))
            else:
                pygame.draw.line(win, STRING_COLOR, bow_point_1, bow_point_2, 1)
            blit_rotate(win, arrow_png,
                    (player_pos[0] + math.sin(lastangle) * (pull_strength * 15 - 8), 
                    player_pos[1] + math.cos(lastangle) * (pull_strength * 15 - 8)),
                    math.degrees(lastangle) + 90)
            blit_rotate(win, player_png, player_pos.true(), math.degrees(lastangle) - 45)
            targets_text = font.render(f'targets hit: {len(hits)}/{len(map["targets"])}', True, (255, 255, 255))
            win.blit(targets_text, (5, 30))
        else:
            if len(arrow_container) == 0:
                win.blit(endscreen_png, (0, 0))
        coins_text = font.render(f'coins: {coins}', True, (255, 255, 255))
        win.blit(coins_text, (5, 1))
        if not assisted:
            help_text = font.render('[1] Aim Assist (5 coins)', True, availability(5))
            win.blit(help_text, (WINDOW_SIZE[0] - 318, 1))

        pygame.display.update()