import pygame
import vector
import game
import math

CONSTRAINT_RADIUS = 250
death = False

class Solver:
    gravity = vector.Vector(0, 0.5)

    def __init__(self, win):
        self.win = win

    def update(self, dt: float):
        sub_steps = 6
        sub_dt = dt / sub_steps

        for i in range(sub_steps):
            self.apply_gravity()
            self.update_positions(sub_dt)
            self.apply_constraint()
            self.solve_collisions()

    def update_positions(self, dt = float):
        for obj in game.Object.objects:
            obj.update_position(dt)
            if obj.position_current()[1] > self.win.get_size()[1] + obj.radius:
                game.Object.objects.remove(obj)
            elif obj.position_current()[0] > self.win.get_size()[0] + obj.radius or obj.position_current()[0] < -obj.radius:
                game.Object.objects.remove(obj)

    def apply_gravity(self):
        for obj in game.Object.objects:
            obj.accelerate(Solver.gravity)

    def apply_constraint(self):
        global death
        center = (self.win.get_size()[0] / 2, self.win.get_size()[1] / 2)
        for obj in game.Object.objects:
            if obj.position_current()[0] < center[0] - CONSTRAINT_RADIUS + obj.radius:
                obj.position_current = vector.Vector(center[0] - CONSTRAINT_RADIUS + obj.radius, obj.position_current()[1])
            if obj.position_current()[0] > center[0] + CONSTRAINT_RADIUS - obj.radius:
                obj.position_current = vector.Vector(center[0] + CONSTRAINT_RADIUS - obj.radius, obj.position_current()[1])
            if obj.position_current()[1] < center[1] - CONSTRAINT_RADIUS - 50:
                if not obj.invincible:
                    death = True
            else:
                obj.invincible = False
            if obj.position_current()[1] > center[1] + CONSTRAINT_RADIUS - obj.radius:
                obj.position_current = vector.Vector(obj.position_current()[0], center[1] + CONSTRAINT_RADIUS - obj.radius) 

    def fix_constraint(self, obj: game.Object):
        center = (self.win.get_size()[0] / 2, self.win.get_size()[1] / 2)
        if obj.position_current()[0] < center[0] - CONSTRAINT_RADIUS + obj.radius:
            obj.position_current = vector.Vector(center[0] - CONSTRAINT_RADIUS + obj.radius, obj.position_current()[1])
        if obj.position_current()[0] > center[0] + CONSTRAINT_RADIUS - obj.radius:
            obj.position_current = vector.Vector(center[0] + CONSTRAINT_RADIUS - obj.radius, obj.position_current()[1])
        if obj.position_current()[1] > center[1] + CONSTRAINT_RADIUS - obj.radius:
            obj.position_current = vector.Vector(obj.position_current()[0], center[1] + CONSTRAINT_RADIUS - obj.radius)
        obj.position_old = obj.position_current

    def solve_collisions(self):
        response_coef = 1
        objects_count = len(game.Object.objects)

        for i in range(objects_count):
            object_1 = game.Object.objects[i]

            for k in range(i + 1, objects_count):
                object_2 = game.Object.objects[k]
                v = object_1.position_current - object_2.position_current
                dist2 = v.x * v.x + v.y * v.y
                min_dist = object_1.radius + object_2.radius

                if dist2 < min_dist * min_dist:
                    dist = math.sqrt(dist2)
                    n = v / dist
                    mass_ratio_1 = object_1.radius / (object_1.radius + object_2.radius)
                    mass_ratio_2 = object_2.radius / (object_1.radius + object_2.radius)
                    delta = 0.5 * response_coef * (dist - min_dist)
                    if object_1.type == object_2.type:
                        object_1.position_current -= (object_1.position_current - object_2.position_current) / 2
                        game.Object.score += 4 ** object_1.type
                        game.Object.remove_object(object_2)
                        object_1.level_up()
                        self.fix_constraint(object_1)
                        return
                    object_1.position_current -= vector.Vector(n()[0] * (mass_ratio_1 * delta), n()[1] * (mass_ratio_1 * delta))
                    object_2.position_current += vector.Vector(n()[0] * (mass_ratio_2 * delta), n()[1] * (mass_ratio_2 * delta))


def restart():
    global death
    death = False
    game.Object.reset()
