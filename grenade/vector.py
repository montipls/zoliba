class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector(self.x + other, self.y + other)
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Vector(self.x - other, self.y - other)
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other = float):
        return Vector(self.x * other, self.y * other)
    
    def __truediv__(self, other = float):
        return Vector(self.x / other, self.y / other)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def tup(self):
        return (self.x, self.y)
    
    @staticmethod
    def new(t: tuple):
        return Vector(t[0], t[1])