import pygame
import math
import random
import os

import vector

pygame.joystick.init()


class Point:
    def __init__(self, pos: vector.Vector, radius: int, fixed = False, mouse = False):
        self.position_current = pos
        self.position_old = self.position_current
        self.acceleration = vector.Vector(0, 0)
        self.radius = radius
        self.fixed = fixed
        self.mouse = mouse
        self.friction = 0.94
        self.grab = False
        self.standing = False
        self.bouncy = 1

    def update_position(self, floor_y): # dt
        if not self.fixed:
            velocity = self.position_current - self.position_old
            self.position_old = self.position_current
            self.position_current = self.position_current + velocity * self.friction + self.acceleration * 50 # * dt * dt
            self.acceleration = vector.Vector(0, 0)

        if self.mouse:
            if pygame.mouse.get_pressed()[1]:
                self.grab = True
                x, y = pygame.mouse.get_pos()
                if y > floor_y - 1:
                    y = floor_y - 1
                mouse_vec = vector.Vector.new((x, y))
                acc = mouse_vec - self.position_current
                self.accelerate(acc/10000)
            else:
                self.grab = False

    def apply_constraint(self, left: int, right: int, bottom: int, fix_points: list):
        pos = self.position_current.tup()

        self.standing = False
        self.friction = 0.99
        
        if pos[0] > right - self.radius:
            self.position_current += vector.Vector((right - self.radius - self.position_current.x) * self.bouncy, 0)
        elif pos[0] < left + self.radius:
            self.position_current += vector.Vector((left + self.radius - self.position_current.x) * self.bouncy, 0)
        pos = self.position_current.tup()
        if pos[1] > bottom - self.radius:
            self.position_current += vector.Vector(0, (bottom - self.radius - self.position_current.y) * self.bouncy)
            self.friction = 0.94
            self.standing = True

        for pt in fix_points:
            axis = self.position_current - vector.Vector.new(pt.pos)
            dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
            if dist < pt.r:
                n = axis / dist
                x = n.x
                if abs(n.x) < abs(n.y) * 0.8:
                    x = n.x / 3
                    self.friction = pt.slip
                    self.standing = True
                    if abs(n.x) < abs(n.y) * 0.5:
                        x = 0
                delta = pt.r - dist
                self.position_current += vector.Vector(x * delta, n.y * delta) * self.bouncy

    def accelerate(self, acc):
        self.acceleration += acc


class Link:
    def __init__(self, object_1, object_2, target_vec, strength, single = False, closing=False):
        self.object_1 = object_1
        self.object_2 = object_2
        self.target_vec = target_vec
        self.strength = strength
        self.single = single
        self.target_dist = math.sqrt(self.target_vec.tup()[0] * self.target_vec.tup()[0] + self.target_vec.tup()[1] * self.target_vec.tup()[1])
        self.closing = closing

    def apply(self, modifier): # dt
        v = self.object_2.position_current - self.object_1.position_current
        diff = v - self.target_vec

        axis = self.object_1.position_current - self.object_2.position_current
        dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
        n = axis / dist
        delta = self.target_dist - dist

        if not self.closing or dist > self.target_dist:
            if not self.single:
                if not self.object_1.fixed:
                    self.object_1.position_current += vector.Vector(n.x * 0.23 * delta, n.y * 0.23 * delta)
                if not self.object_2.fixed:
                    self.object_2.position_current -= vector.Vector(n.x * 0.23 * delta, n.y * 0.23 * delta)
                
                if not self.object_1.fixed:
                    self.object_1.position_current += (vector.Vector(diff.x * self.strength[0], diff.y * self.strength[1]) / 170) * modifier
                if not self.object_2.fixed:
                    self.object_2.position_current -= (vector.Vector(diff.x * self.strength[0], diff.y * self.strength[1]) / 170) * modifier
            else:
                if not self.object_2.fixed:
                    self.object_2.position_current -= vector.Vector(n.x * delta, n.y * delta)


class Fighter:
    colors = [
        (160, 160, 200),
        (160, 200, 160),
        (200, 160, 160),
    ]

    deflect_sprites = [pygame.image.load(f"assets/deflect/{f}") for f in os.listdir("assets/deflect")]
    flipped_deflect_sprites = [pygame.transform.flip(image.copy(), True, False) for image in deflect_sprites]

    def __init__(self, head_pos: vector.Vector, constraint: tuple[int, int, int], head_type: int, sounds):
        self.constraint = constraint
        self.modifier = 0.6
        self.construct(head_pos)
        self.foot = "left"
        self.dead = False
        self.head_type = head_type
        self.bomb_color = random.choice(Fighter.colors)
        Fighter.colors.remove(self.bomb_color)
        self.bomb = Bomb(self.head_pos, 3, self.bomb_color)
        self.explosion_radius = -1
        self.last_explosion_pos = (0, 0)
        self.sounds = sounds
        self.health = 100
        self.dead = False
        self.bomb_reload = 0
        self.gravity = vector.Vector(0, 0.0006)
        self.jumped = False
        self.head_hit = False
        # self.sword_cooldown = 0
        # self.deflect_cooldown = 0
        # self.deflect_started = False
        # self.deflect_animation_index = 0
        # self.deflect_animation_start = False
        # self.last_deflect_direction = 1

    def construct(self, head_pos):
        self.head_pos = head_pos
        self.neck_pos = self.head_pos + vector.Vector(0, 3)

        self.left_knee_pos = self.neck_pos + vector.Vector(-2, 4)
        self.right_knee_pos = self.neck_pos + vector.Vector(2, 4)
        self.left_foot_pos = self.left_knee_pos + vector.Vector(0, 5)
        self.right_foot_pos = self.left_knee_pos + vector.Vector(0, 5)

        self.sword_pos = self.neck_pos + vector.Vector(-3, 18)

        self.head = Point(self.head_pos, 1, mouse=True)
        self.neck = Point(self.neck_pos, 1)

        self.left_knee = Point(self.left_knee_pos, 1)
        self.right_knee = Point(self.right_knee_pos, 1)
        self.left_foot = Point(self.left_foot_pos, 1)
        self.right_foot = Point(self.right_foot_pos, 1)

        self.main_foot = self.right_foot
        self.rest_foot = self.left_foot

        self.sword_point = Point(self.sword_pos, 3)

        self.joints = [
            self.head,
            self.neck,
            self.left_knee,
            self.right_knee,
            self.left_foot,
            self.right_foot,
            self.sword_point
        ]

        self.neck_link = Link(self.head, self.neck, vector.Vector(0, 3), (5, 4))

        self.left_upper_leg = Link(self.neck, self.left_knee, vector.Vector(-2, 4), (1, 6))
        self.right_upper_leg = Link(self.neck, self.right_knee, vector.Vector(2, 4), (1, 6))
        self.left_lower_leg = Link(self.left_knee, self.left_foot, vector.Vector(0, 5), (7, 5))
        self.right_lower_leg = Link(self.right_knee, self.right_foot, vector.Vector(0, 5), (7, 5))

        self.sword_link = Link(self.neck, self.sword_point, vector.Vector(-3, 18), (1, 1), single=True, closing=True)

        self.links = [
            self.left_upper_leg,
            self.right_upper_leg,
            self.left_lower_leg,
            self.right_lower_leg
        ]

    def update(self, floor_y, fix_points):
        if self.health < 0:
            self.dead = True

        for joint in self.joints:
            joint.accelerate(self.gravity)
            joint.update_position(floor_y)
            joint.apply_constraint(self.constraint[0], self.constraint[1], self.constraint[2], fix_points)

        for link in self.links:
            link.apply(self.modifier)
        self.sword_link.apply(self.modifier)
        self.neck_link.apply(self.modifier)

        if self.modifier != 1:
            if self.left_foot.standing or self.right_foot.standing:
                self.modifier = 1
        else:
            if self.head.grab:
                self.modifier = 0.6

        self.bomb.friction += 0.01
        self.bomb.accelerate(vector.Vector(0, 0.0006))
        self.bomb.update_position(floor_y)
        self.bomb.apply_constraint(self.constraint[0], self.constraint[1], self.constraint[2], fix_points)
        if not self.bomb.thrown:
            self.bomb.position_current = self.head.position_current

    # unused
    def check_for_sword_hit(self, player, joysticks):
        joy = joysticks[self.head_type]

        if self.deflect_cooldown > 0:
            self.deflect_cooldown -= 1

        if player != None:
            axis = player.sword_point.position_current - self.head.position_current
            dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
            lb, rb = joy.get_button(4), joy.get_button(5)
            if not lb and not rb:
                self.deflect_started = False

            if not joy.get_button(1) and not self.dead and not self.bomb.thrown and self.deflect_cooldown <= 0:
                if lb and not self.deflect_started:
                    self.deflect_started = True

                    if dist < self.head.radius + player.sword_point.radius + 5:
                        if player.head.position_current.x < self.head.position_current.x or abs(player.head.position_current.x - self.head.position_current.x) < 3:
                            if player.head.position_current.y < self.head.position_current.y:
                                player.sword_point.accelerate(vector.Vector(-0.3, -0.3))
                            else:
                                player.sword_point.accelerate(vector.Vector(-0.3, 0.3))
                            player.sword_cooldown = 100
                            self.last_deflect_direction = -1
                            self.deflect_animation_start = True
                            self.sounds[2].play()
                    else:
                        self.deflect_cooldown = 50
                        self.sounds[3].play()

                elif rb and self.deflect_cooldown <= 0 and not self.deflect_started:
                    self.deflect_started = True

                    if dist < self.head.radius + player.sword_point.radius + 5:
                        if player.head.position_current.x > self.head.position_current.x or abs(player.head.position_current.x - self.head.position_current.x) < 3:
                            if player.head.position_current.y < self.head.position_current.y:
                                player.sword_point.accelerate(vector.Vector(0.3, -0.3))
                            else:
                                player.sword_point.accelerate(vector.Vector(0.3, 0.3))
                            player.sword_cooldown = 100
                            self.last_deflect_direction = -1
                            self.deflect_animation_start = True
                            self.sounds[2].play()
                    else:
                        self.deflect_cooldown = 50
                        self.sounds[3].play()

            if dist < self.head.radius + self.sword_point.radius:
                if not self.head_hit:
                    self.health -= 10
                self.head_hit = True
            else:
                self.head_hit = False

    def check_for_explosion(self, player):
        self.bomb.tick()
        if player != None:
            if player.bomb.ready and not player.bomb.opp_exploded and player.bomb.thrown:
                for joint in self.joints:
                    axis = joint.position_current - player.bomb.position_current
                    dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
                    n = axis / dist
                    if dist < 75:
                        joint.accelerate(n * (-dist + 75) * 0.0012)
                if dist <= 75:
                    self.health -= (-dist + 75) / 2
                player.bomb.opp_exploded = True

        if self.bomb.ready and not self.bomb.self_exploded and self.bomb.thrown:
            for joint in self.joints:
                axis = joint.position_current - self.bomb.position_current
                dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
                n = axis / dist
                if dist < 75:
                    joint.accelerate(n * (-dist + 75) * 0.0012)
            self.bomb.self_exploded = True

    def check_for_bomb_reload(self):
        if self.bomb.self_exploded and self.bomb.opp_exploded:
            if self.bomb_reload == 0:
                self.sounds[1].play()
                self.explosion_radius = 0
                self.last_explosion_pos = self.bomb.position_current.tup()
            self.bomb_reload += 1
            if self.bomb_reload >= 300:
                self.bomb = Bomb(self.head_pos, 3, self.bomb_color)
                self.bomb_reload = 0

    def render_explosions(self, win):
        if self.explosion_radius >= 0:
            self.explosion_radius += 1
            if self.explosion_radius > 25:
                self.explosion_radius = -1
                return
            pygame.draw.circle(win, self.bomb_color, self.last_explosion_pos, self.explosion_radius * 3, width=2)

    @staticmethod
    def step_dist(l, r, num, axis) -> bool:
        if axis >= 0:
            return l < r + num
        else:
            return l > r - num
        
    @staticmethod
    def step(l, r, axis) -> bool:
        if axis >= 0:
            return l < r
        else:
            return l > r
        
    def cor_upper_leg(self, main):
        if main == self.left_foot:
            return [self.left_upper_leg, self.right_upper_leg]
        else:
            return [self.right_upper_leg, self.left_upper_leg]
        
    def leg_switch(self):
        temp = self.rest_foot
        self.rest_foot = self.main_foot
        self.main_foot = temp

    def move(self, joysticks):
        joy = joysticks[self.head_type]
        self.gravity = vector.Vector(0, 0.0006)

        if joy.get_button(1) or self.dead:
            self.modifier = 0
        elif abs(joy.get_axis(0)) > 0.15 and not self.dead:
            if self.foot == "left":
                if (self.main_foot.position_current.tup()[0] > self.rest_foot.position_current.tup()[0]):
                    leg = self.cor_upper_leg(self.main_foot)
                    leg[0].target_vec.x = 2
                    leg[1].target_vec.x = -2
                    self.foot = "right"
            elif self.foot == "right":
                if self.main_foot.position_current.tup()[0] < self.rest_foot.position_current.tup()[0]:
                    leg = self.cor_upper_leg(self.main_foot)
                    leg[0].target_vec.x = -2
                    leg[1].target_vec.x = 2
                    self.foot = "left"

            if self.step_dist(self.main_foot.position_current.tup()[0], self.rest_foot.position_current.tup()[0], 9, joy.get_axis(0)):
                if not self.head.grab and (self.left_foot.standing or self.right_foot.standing):
                    self.rest_foot.position_old = self.rest_foot.position_current
                self.main_foot.position_current += vector.Vector(0.07 * joy.get_axis(0), 0)
            else:
                if self.left_foot.standing or self.right_foot.standing:
                    self.sounds[0].play()
                self.leg_switch()
                if self.foot == "left":
                    self.foot = "right"
                else:
                    self.foot = "left"

        # if self.sword_cooldown > 0:
        #     self.sword_cooldown -= 1

        # axis = vector.Vector(joy.get_axis(2), joy.get_axis(3))
        # dist = math.sqrt(axis.x * axis.x + axis.y * axis.y)
        # if dist > 0.2 and not joy.get_button(1) and not self.dead and self.sword_cooldown <= 0:
        #     dest = self.neck.position_current + axis * self.sword_link.target_dist
        #     self.sword_point.accelerate((dest - self.sword_point.position_current) * 0.00005)
                    
        if joy.get_button(0) and not joy.get_button(1) and not self.dead:
            if not self.jumped:
                self.jumped = True
                if (self.left_foot.standing or self.right_foot.standing):
                    self.left_knee.position_current += vector.Vector(0, -5.5)
                    self.right_knee.position_current += vector.Vector(0, -5.5)
        else:
            self.jumped = False

        if joy.get_button(2) and not self.bomb.thrown and self.bomb_reload == 0 and not self.dead and not joy.get_button(1):
            self.bomb.throw((joy.get_axis(0), joy.get_axis(1)))

    @staticmethod
    def reflection(pos, floor_y):
        x, y = pos
        return (x, floor_y * 2 - y)

    def render(self, win: pygame.Surface, floor_y):
        self.render_explosions(win)

        # pos = self.sword_link.object_2.position_current.tup()
        # ref_pos = self.reflection(pos, floor_y)

        # pygame.draw.line(win, (232, 98, 28), ref_pos, self.reflection(self.sword_link.object_1.position_current.tup(), floor_y), 1)
        # pygame.draw.line(win, (200, 200, 200), pos, self.sword_link.object_1.position_current.tup(), 1)

        # pygame.draw.circle(win, (236, 106, 39), ref_pos, self.sword_point.radius, width=1)
        # pygame.draw.circle(win, (236, 106, 39), ref_pos, 1)
        # pygame.draw.circle(win, self.bomb_color, pos, self.sword_point.radius, width=1)
        # pygame.draw.circle(win, self.bomb_color, pos, 1)

        for link in self.links:
            pygame.draw.line(win, (212, 78, 8), self.reflection(link.object_1.position_current.tup(), floor_y), self.reflection(link.object_2.position_current.tup(), floor_y), 1)
            pygame.draw.line(win, (40, 40, 40), link.object_1.position_current.tup(), link.object_2.position_current.tup(), 1)
        
        pos = self.main_foot.position_current.tup()
        win.set_at((int(pos[0]), int(pos[1])), (100, 100, 100))
        
        pos = self.head.position_current.tup()
        ref_pos = self.reflection(pos, floor_y)

        if self.head_type == 0:
            if not self.dead:
                if self.bomb.self_exploded and self.bomb.opp_exploded:
                    pygame.draw.rect(win, (236, 106, 39), (ref_pos[0] - 2, ref_pos[1] - int(self.bomb_reload / 100) + 1, 4, int(self.bomb_reload / 100) + 1))
                self.bomb.refrender(win, self.head_type, floor_y)

            pygame.draw.circle(win, (208, 74, 4), self.reflection(self.head.position_current.tup(), floor_y), self.head.radius + 2, width=1)
            
            if not self.dead:
                if self.bomb.self_exploded and self.bomb.opp_exploded:
                    pygame.draw.rect(win, self.bomb_color, (pos[0] - 2, pos[1] - 2, 4, int(self.bomb_reload / 100) + 1))
                self.bomb.render(win, self.head_type)

            pygame.draw.circle(win, (10, 10, 10), self.head.position_current.tup(), self.head.radius + 2, width=1)

        elif self.head_type == 1:
            if not self.dead:
                if self.bomb.self_exploded and self.bomb.opp_exploded:
                    pygame.draw.rect(win, (236, 106, 39), (ref_pos[0] - 2, ref_pos[1] - int(self.bomb_reload / 100) + 1, 4, int(self.bomb_reload / 100) + 1))
                self.bomb.refrender(win, self.head_type, floor_y)

            ref = self.reflection(self.head.position_current.tup(), floor_y)
            pygame.draw.rect(win, (208, 74, 4), (ref[0] - 2, ref[1] - 3, 5, 5), width=1)

            if not self.dead:
                if self.bomb.self_exploded and self.bomb.opp_exploded:
                    pygame.draw.rect(win, self.bomb_color, (pos[0] - 2, pos[1] - 2, 4, int(self.bomb_reload / 100) + 1))
                self.bomb.render(win, self.head_type)

            pygame.draw.rect(win, (10, 10, 10), (self.head.position_current.x - 2, self.head.position_current.y - 2, 5, 5), width=1)

        # if self.deflect_animation_start:
        #     if self.last_deflect_direction < 0:
        #         win.blit(Fighter.flipped_deflect_sprites[int(self.deflect_animation_index)], (self.head.position_current.x - 3, self.head.position_current.y - 6))
        #     elif self.last_deflect_direction > 0:
        #         win.blit(Fighter.deflect_sprites[int(self.deflect_animation_index)], (self.head.position_current.x - 2, self.head.position_current.y - 6))
        #     self.deflect_animation_index += 0.5
        #     if int(self.deflect_animation_index) > 6:
        #         self.deflect_animation_start = False
        #         self.deflect_animation_index = 0

        if self.health != 100 and not self.dead:
            pygame.draw.line(win, (100, 100, 100), (pos[0] - 4, pos[1] - 5), (pos[0] + 4, pos[1] - 5), 1)
            pygame.draw.line(win, (120, 200, 120), (pos[0] - 4, pos[1] - 5), (pos[0] - 5 + round(self.health / (100 / 9)) + 1, pos[1] - 5), 1)


class Ball:
    colors = [
        (180, 160, 200),
        (160, 180, 200),
        (180, 200, 160),
        (160, 200, 180),
        (200, 160, 180),
        (200, 180, 160),
    ]

    def __init__(self, pos, radius, slip):
        self.pos = pos
        self.r = radius
        self.slip = slip
        self.color = random.choice(Ball.colors)

    def render(self, win):
        pygame.draw.circle(win, (170, 170, 170), self.pos, self.r, width=1)
        pygame.draw.circle(win, (140, 140, 160), self.pos, self.r - 2, width=self.r - 6)
        pygame.draw.circle(win, (200, 200, 200), self.pos, 5, width=2)
        pygame.draw.circle(win, self.color, self.pos, self.r - 6, width=1)
        n = vector.Vector.new((-math.sin(math.radians(45)), -math.sin(math.radians(45))))
        pygame.draw.line(win, (200, 200, 200), (vector.Vector.new(self.pos) + n * 5).tup(), (vector.Vector.new(self.pos) + n * (self.r - 3)).tup(), 1)
        pygame.draw.line(win, (200, 200, 200), (vector.Vector.new(self.pos) + n * 5 + vector.Vector(2, -1)).tup(), (vector.Vector.new(self.pos) + n * (self.r - 3) + vector.Vector(2, -1)).tup(), 1)
        pygame.draw.line(win, (200, 200, 200), (vector.Vector.new(self.pos) + n * 5 + vector.Vector(-1, 2)).tup(), (vector.Vector.new(self.pos) + n * (self.r - 3) + vector.Vector(-1, 2)).tup(), 1)
        # (230, 0, 90)


class Bomb(Point):
    def __init__(self, pos, radius, color):
        super().__init__(pos, radius)
        self.life = 300
        self.blink = 20
        self.transparent = False
        self.thrown = False
        self.ready = False
        self.self_exploded = False
        self.opp_exploded = False
        self.bouncy = 1.3
        self.color = color

    def throw(self, n):
        self.accelerate(vector.Vector.new(n) * 0.05)
        self.thrown = True

    def tick(self):
        if self.thrown:
            self.life -= 1
        if self.life <= 0:
            self.ready = True
    
    def render(self, win, type):
        if self.life < 100:
            self.blink -= 1
            if self.blink <= 0:
                self.blink = (self.life + 100) / 10
                if not self.transparent:
                    self.transparent = True
                else:
                    self.transparent = False
        if self.thrown:
            if not self.transparent and not self.opp_exploded and not self.self_exploded:
                pygame.draw.circle(win, self.color, self.position_current.tup(), self.radius)
        elif type == 0:
            pygame.draw.circle(win, self.color, self.position_current.tup(), self.radius)
        else:
            pygame.draw.rect(win, self.color, (self.position_current.x - 1, self.position_current.y - 1, 3.5, 3.5))
    
    def refrender(self, win, type, floor_y):
        pos = Fighter.reflection(self.position_current.tup(), floor_y)
        color = (236, 106, 39)
        if self.thrown:
            if not self.transparent and not self.opp_exploded and not self.self_exploded:
                pygame.draw.circle(win, color, pos, self.radius)
        elif type == 0:
            pygame.draw.circle(win, color, pos, self.radius)
        else:
            pygame.draw.rect(win, color, (pos[0] - 1, pos[1] - 2, 3.5, 3.5))