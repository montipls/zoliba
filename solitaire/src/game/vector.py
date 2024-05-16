if __name__ == 'game.vector':
    class Vector:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __add__(self, other):
            if isinstance(other, (int, float)):
                return Vector(self.x + other, self.y + other)
            if isinstance(other, tuple):
                return Vector(self.x + other[0], self.y + other[1])
            return Vector(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
            if isinstance(other, (int, float)):
                return Vector(self.x - other, self.y - other)
            if isinstance(other, tuple):
                return Vector(self.x - other[0], self.y - other[1])
            return Vector(self.x - other.x, self.y - other.y)

        def __mul__(self, other: float):
            return Vector(self.x * other, self.y * other)

        def __truediv__(self, other: float):
            return Vector(self.x / other, self.y / other)
        
        def __getitem__(self, index: int) -> float:
            return self.true()[index]

        def true(self) -> tuple:
            return (self.x, self.y)
        
        def change(self, axis, new) -> None:
            if axis == 'x':
                self.x = new
            elif axis == 'y':
                self.y = new
            else:
                raise IndexError
