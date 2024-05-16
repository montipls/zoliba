import vector

class Object:
    objects = []
    score = 0

    def __init__(self, pos: vector.Vector, type = 0) -> None:
        self.position_current = pos
        self.position_old = self.position_current
        self.acceleration = vector.Vector(0, 0)
        self.type = type
        self.invincible = True
        self.radius = self.init_type(self.type)

    def init_type(self, type):
        return (type + 1) * 15 + 5

    def update_position(self, dt = float):
        velocity = self.position_current - self.position_old
        self.position_old = self.position_current
        self.position_current = self.position_current + vector.Vector(
            velocity()[0] * 0.995, velocity()[1] * 0.5 if velocity()[1] < 0 else velocity()[1]
        ) / 1.006 + self.acceleration * dt * dt
        self.acceleration = vector.Vector(0, 0)

    def accelerate(self, acc):
        self.acceleration += acc

    def level_up(self):
        self.type += 1
        self.radius = self.init_type(self.type)
            
    @classmethod
    def append_object(cls, obj, count: int = 1):
        for _ in range(count):
            cls.objects.append(obj)

    @classmethod
    def remove_object(cls, obj):
        cls.objects.remove(obj)

    @classmethod
    def reset(cls):
        cls.objects = []
        cls.score = 0


def get_sprite(type: int) -> str:
   return f'img/{min(400, (type + 1) * 30 + 10)}.png' 
