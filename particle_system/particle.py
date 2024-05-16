import random
import math
import time


class Particle:
    def __init__(self,
        x: int, y: int,
        speed: float,
        max_lifetime: int
    ) -> None:
        self.x, self.y = x, y
        self.speed = speed
        self.delta_lifetime = 0
        self.lifetime = random.randrange(0, max_lifetime)

    def update_position(self, delta_time) -> None:
        self.y += self.speed * (delta_time / 1000)
        self.delta_lifetime += delta_time
    
    def reset(self, x: float, y: float, speed: float) -> None:
        self.y = 0
        self.x, self.y = x, y
        self.speed = speed
        self.delta_lifetime: int = 0


class ParticleSystem:
    def __init__(self,
        X: int, Y: int,
        max_speed: float,
        max_lifetime: int,
        spread: float = 1.0
    ) -> None:
        self.X, self.Y = X, Y
        self.mean = self.X / 2
        self.max_speed = max_speed
        self.max_lifetime = max_lifetime
        self.spread = spread
        self.last_time = time.time()
        self.matrix: dict[tuple[int, int], int] = {}
        self.particles: list[Particle] = []

    def append_to_matrix(self, pos: tuple[int, int]) -> None:
        if pos in self.matrix.keys():
            self.matrix[pos] += 1
            return
        self.matrix[pos] = 1

    def remove_from_matrix(self, pos: tuple[int, int]) -> None:
        if self.matrix.get(pos):
            if self.matrix[pos] > 1:
                self.matrix[pos] -= 1
                return
            del self.matrix[pos]

    def add_particles(self, particle_count: int) -> None:
        particles: list[Particle] = []
        for _ in range(particle_count):
            x = max(0, min(self.X - 0.01, random.normalvariate(self.mean, self.spread)))
            particles.append(Particle(x, 0.0, random.uniform(0, self.max_speed), self.max_lifetime))
            self.append_to_matrix((0, math.floor(x)))

        self.particles.extend(particles)
    
    def update(self) -> None:
        now = time.time()
        delta_time = (now - self.last_time) * 1000
        self.last_time = now

        for particle in self.particles:
            old_row = math.floor(particle.y)
            old_col = math.floor(particle.x)

            particle.update_position(delta_time)
            if particle.y > self.Y \
            or particle.y < 0 \
            or particle.x > self.X \
            or particle.x < 0 \
            or particle.delta_lifetime > particle.lifetime:
                self.reset_particle(particle)

            row = math.floor(particle.y)
            col = math.floor(particle.x)

            if old_row != row or old_col != col:
                self.remove_from_matrix((old_row, old_col))
                self.append_to_matrix((row, col))
    
    def reset_particle(self, particle: Particle) -> None:
        x = max(0, min(self.X - 0.01, random.normalvariate(self.mean, self.spread)))
        particle.reset(x, 0.0, random.uniform(0, self.max_speed))