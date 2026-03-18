from math import sqrt

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = int(x)
        self.y = int(y)

    def copy(self):
        return Point(self.x, self.y)

    def distance(self, other: "Point") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)