import pygame
import sys
import math
import ast


def rotate2d(pos, radian):
    x, y = pos
    sin, cos = math.sin(radian), math.cos(radian)
    return x * cos - y * sin, y * cos + x * sin


def load_map(txt):
    with open(txt, 'r') as file:
        return ast.literal_eval(file.read())
    

def remove_touching_faces(points, pane = False):
    cubes = []
    for x, y, z in points:
        if pane:
            sides = [False, False, False, True, False, False]
            cubes.append(Cube((x, -y, z), sides=sides))
            continue

        sides = [True, True, True, True, True, True]

        side_x = (x - 1, y, z)
        side_X = (x + 1, y, z)

        side_y = (x, y - 1, z)
        side_Y = (x, y + 1, z)

        side_z = (x, y, z - 1)
        side_Z = (x, y, z + 1)

        for pos in points:
            if pos == side_x:
                sides[2] = False
            if pos == side_X:
                sides[5] = False
            if pos == side_y:
                sides[4] = False
            if pos == side_Y:
                sides[3] = False
            if pos == side_z:
                sides[0] = False
            if pos == side_Z:
                sides[1] = False

        cubes.append(Cube((x, -y, z), sides=sides))
    return cubes
    

def generate_pane(points, camera, r):
    x, _, z = camera.pos
    for i in range(r):
        for y in range(r):
            points.append((int(x) - int(r / 2) + i, -1, int(z) - int(r / 2) + y))


class Camera:
    def __init__(self, pos = (0, 0, 0), rot = (0, 0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event, sensitivity):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= sensitivity
            y /= sensitivity

            self.rot[0] += y
            if self.rot[0] < -1.57:
                self.rot[0] = -1.57
            elif self.rot[0] > 1.57:
                self.rot[0] = 1.57
            print(self.pos)
            self.rot[1] += x

    def update(self, dt, key):
        velocity = dt * 10

        if key[pygame.K_SPACE]:
            self.pos[1] -= velocity
        if key[pygame.K_LSHIFT]:
            self.pos[1] += velocity

        x, y = velocity * math.sin(self.rot[1]), velocity * math.cos(self.rot[1])

        if key[pygame.K_w]:
            self.pos[0] += x
            self.pos[2] += y
        if key[pygame.K_s]:
            self.pos[0] -= x
            self.pos[2] -= y
        if key[pygame.K_a]:
            self.pos[2] += x
            self.pos[0] -= y
        if key[pygame.K_d]:
            self.pos[2] -= x
            self.pos[0] += y


class Cube:
    verticies = [
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ]

    edges = [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 4],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7]
    ]

    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 3, 7, 4],
        [0, 4, 5, 1],
        [2, 3, 7, 6],
        [1, 2, 6, 5]
    ]

    face_colors = [
        (150, 150, 150),
        (150, 150, 150),
        (150, 150, 150),
        (150, 100, 100),
        (150, 100, 100),
        (150, 150, 150),
    ]

    def __init__(self, pos = (0, 0, 0), sides = [True, True, True, True, True, True]):
        self.pos = pos
        self.sides = sides
        self.x, self.y, self.z = pos
        self.verts = [(self.x + X / 2, self.y + Y / 2, self.z + Z / 2) for X, Y, Z in self.verticies]
        self.face_order = []
        self.screen_coords = []

    def dist(self):
        return sum((x - camera.pos[i]) ** 2 for i, x in enumerate(self.pos))

    def get_cubes(self):
        vertex_list = []
        self.screen_coords = []

        self.face_list = []
        self.face_color = []
        self.depth = []

        for x, y, z in self.verts:
            x -= camera.pos[0]
            y -= camera.pos[1]
            z -= camera.pos[2]

            x, z = rotate2d((x, z), camera.rot[1])
            y, z = rotate2d((y, z), camera.rot[0])
            vertex_list.append((x, y, z))

            depth_ = abs(win_center[0] / 2 / z)
            x, y = x * depth_, y * depth_

            self.screen_coords.append([win_center[0] + x, win_center[1] + y])

        for f, face in enumerate(self.faces):
            face_dist = sum(sum(vertex_list[j][i] for j in face) ** 2 for i in range(3))
            on_screen = False

            for i in face:
                x, y = self.screen_coords[i]
                if vertex_list[i][2] > 0 and x > 0 and x < win_width and y > 0 and y < win_height:
                    on_screen = True
                    break
            
            if not self.sides[f]:
                self.face_list.append(None)
                self.face_color.append(None)
                self.depth.append(face_dist)
                continue

            if on_screen:
                r, g, b = self.face_colors[f]
                face_dist = sum(sum(vertex_list[j][i] for j in face) ** 2 for i in range(3))
                color = max(min(int(r * 300 / (face_dist + 500) - 30), r), 5), max(min(int(g * 300 / (face_dist + 500) - 30), g), 5), max(min(int(b * 300 / (face_dist + 500) - 30), b), 10)
                coords = [self.screen_coords[i] for i in face]
                self.face_list.append(coords)
                self.face_color.append(color)

                self.depth.append(face_dist)

        self.face_order = sorted(range(len(self.face_list)), key=lambda x: self.depth[x], reverse=True)[-3:]

pygame.init()
win_size = (640, 360)
win_width, win_height = win_size
win_center = (win_width / 2, win_height / 2)
screen = pygame.display.set_mode(win_size, pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

camera = Camera([5, -3, 15])
points = load_map('map.txt')
pane = []
generate_pane(pane, camera, 50)
cubes = remove_touching_faces(points)
pane_cubes = remove_touching_faces(pane, pane=True)

pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

while True:
    dt = clock.tick() / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        camera.events(event, win_center[0] - 100)

    screen.fill((5, 5, 10))
    camera.update(dt, keys)

    for obj in pane_cubes:
        if obj.dist() > 80:
            continue

        obj.get_cubes()
        try:
            pygame.draw.polygon(screen, obj.face_color[3], obj.face_list[3])
        except:
            pass

    for obj in sorted(cubes, key=lambda cube: cube.dist(), reverse=True):
        if obj.dist() > 80:
            continue

        obj.get_cubes()
        for i in obj.face_order:
            try:
                pygame.draw.polygon(screen, obj.face_color[i], obj.face_list[i])
            except:
                pass

    pygame.display.flip()