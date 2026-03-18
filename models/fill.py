from models import Shape

class Fill(Shape):
    def __init__(self, color: str = "#000000"):
        super().__init__(color)
        self.filled_pixels: set = set()

    def move(self, dx: int, dy: int):
        self.filled_pixels = {(x + dx, y + dy) for x, y in self.filled_pixels}
        self.erased_pixels = {(x + dx, y + dy) for x, y in self.erased_pixels}

    def copy(self):
        new = Fill(self.color)
        new.filled_pixels = set(self.filled_pixels)
        return new