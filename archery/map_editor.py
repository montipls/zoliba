import pygame
import sys
import json

from const import WINDOW_SIZE, BACKGROUND_COLOR, PLAYER_COLOR, TARGET_COLORS, WALL_COLOR, COIN_COLORS

win = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN | pygame.SCALED)
editing = False
wall_start = (0, 0)
level = 1
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

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                wall_start = mouse_pos
                editing = True
            elif event.button == 2 and not editing:
                map["player"]["x"] = mouse_pos[0]
                map["player"]["y"] = mouse_pos[1]
            elif event.button == 3 and not editing:
                map["targets"].append({"coords": {"x": mouse_pos[0], "y": mouse_pos[1]}, "radius": 20})
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and editing:
                editing = False
                map["walls"].append({
                        "coords": {
                            "x": min(wall_start[0], mouse_pos[0]), 
                            "y": min(wall_start[1], mouse_pos[1])
                        }, 
                        "size": {
                            "width": abs(mouse_pos[0] - wall_start[0]), 
                            "height": abs(mouse_pos[1] - wall_start[1])
                        }
                    })
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                map = {
                    "walls": [],
                    "targets": [],
                    "coins": [],
                    "player": {
                        "x": WINDOW_SIZE[0] / 2,
                        "y": WINDOW_SIZE[1] / 2
                    }
                }
            if event.key == pygame.K_s:
                with open(f"levels/{level_label}.json", "w+") as file: 
                    json.dump(map, file)
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
            if event.key == pygame.K_p:
                level -= 1
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
            if event.key == pygame.K_c:
                map["coins"].append({"level": level, "x": mouse_pos[0], "y": mouse_pos[1]})
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    win.fill(BACKGROUND_COLOR)
    if editing:
        pygame.draw.rect(win, WALL_COLOR, (
            min(wall_start[0], mouse_pos[0]), 
            min(wall_start[1], mouse_pos[1]), 
            abs(mouse_pos[0] - wall_start[0]), 
            abs(mouse_pos[1] - wall_start[1])))
    for wall in map["walls"]:
        pygame.draw.rect(win, WALL_COLOR, (wall["coords"]["x"], wall["coords"]["y"], wall["size"]["width"], wall["size"]["height"]))
    try:
        for coin in map["coins"]:
            pygame.draw.circle(win, COIN_COLORS[0], (coin["x"], coin["y"]), 10)
            pygame.draw.circle(win, COIN_COLORS[1], (coin["x"], coin["y"]), 9)
    except KeyError:
        map["coins"] = []
    for target in map["targets"]:
        pygame.draw.circle(win, TARGET_COLORS[0], (target["coords"]["x"], target["coords"]["y"]), target["radius"])
        pygame.draw.circle(win, TARGET_COLORS[1], (target["coords"]["x"], target["coords"]["y"]), target["radius"] * (2/3))
        pygame.draw.circle(win, TARGET_COLORS[0], (target["coords"]["x"], target["coords"]["y"]), target["radius"] * (1/3))
    pygame.draw.circle(win, PLAYER_COLOR, (map["player"]["x"], map["player"]["y"]), 8)
    pygame.display.update()