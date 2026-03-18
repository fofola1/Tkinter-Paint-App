from enum import Enum


class LineStyle(Enum):
    SOLID = "solid"
    DOTTED = "dotted"
    DASHED = "dashed"

class Shape:
    def __init__(
        self,
        color: str = "#000000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID
    ):
        self.color = color
        self.line_width = line_width
        self.line_style = line_style
        self.points: list = []
        self.erased_pixels: set = set()

    def move(self, dx: int, dy: int):
        for point in self.points:
            point.x += dx
            point.y += dy
        self.erased_pixels = {(px + dx, py + dy) for px, py in self.erased_pixels}

    def get_type(self) -> str:
        return self.__class__.__name__