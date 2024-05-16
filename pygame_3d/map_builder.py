import pygame
import sys
import ast


def get_grid(screen_size, grid_density):
    segment_size = int(screen_size / grid_density)
    screen_segments = [seg for seg in range(screen_size) if seg % segment_size == 0]

    return [(((0, seg), (screen_size, seg)), ((seg, 0), (seg, screen_size))) for seg in screen_segments]


def get_coords(mouse_pos, screen_size, grid_density):
    segment_size = int(screen_size / grid_density)
    return (abs(int((mouse_pos[0] - mouse_pos[0] % segment_size) / segment_size) - GRID_DENSITY) - 1, int((mouse_pos[1] - mouse_pos[1] % segment_size) / segment_size))


def invert_coords(coords):
    return (abs(coords[0] - GRID_DENSITY + 1), coords[1])


def save_map(map, txt):
    with open(txt, 'w') as file:
        file.write(str(MAP))


def load_map(txt):
    with open(txt, 'r') as file:
        return ast.literal_eval(file.read())


SCREEN_SIZE = 1000
SCREEN_COLOR = (40, 30, 50)
GRID_DENSITY = 50
MAP = []

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
grid = get_grid(SCREEN_SIZE, GRID_DENSITY)
y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_click = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    for seg in grid:
        pygame.draw.line(screen, (99, 99, 99), seg[0][0], seg[0][1], 1)
        pygame.draw.line(screen, (99, 99, 99), seg[1][0], seg[1][1], 1)

    coords = get_coords(mouse_pos, SCREEN_SIZE, GRID_DENSITY)

    if mouse_click[0] and not coords in MAP:
        MAP.append(coords)
        print(f'Added {coords}')
        print(MAP)

    elif mouse_click[2] and coords in MAP:
        MAP.remove(coords)
        print(f'Removed {coords}')
        print(MAP)

    SEGMENT_SIZE = SCREEN_SIZE / GRID_DENSITY
    for coord in MAP:
        inverted_coord = invert_coords(coord)
        pygame.draw.rect(screen, (199, 199, 199), (inverted_coord[0] * SEGMENT_SIZE, inverted_coord[1] * SEGMENT_SIZE, SEGMENT_SIZE, SEGMENT_SIZE))

    pygame.display.update()
    screen.fill(SCREEN_COLOR)
