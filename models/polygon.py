from models import Point, Shape, LineStyle

class Polygon(Shape):
    def __init__(
        self,
        points=None,
        color: str = "#000000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID,
        closed: bool = True,
        filled: bool = False,
        fill_color: str | None = None
    ):
        super().__init__(color, line_width, line_style)
        self.points = list(points) if points else []
        self.closed = closed
        self.filled = filled
        self.fill_color = fill_color

    def add_point(self, point: Point):
        self.points.append(point)

    def copy(self):
        new = Polygon(
            [p.copy() for p in self.points],
            self.color,
            self.line_width,
            self.line_style,
            self.closed,
            self.filled,
            self.fill_color
        )
        new.erased_pixels = set(self.erased_pixels)
        return new