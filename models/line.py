from models import Point, Shape, LineStyle

class Line(Shape):
    def __init__(
        self,
        start: Point | None = None,
        end: Point | None = None,
        color: str = "#000000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID
    ):
        super().__init__(color, line_width, line_style)
        self.start = start or Point()
        self.end = end or Point()
        self.points = [self.start, self.end]

    def copy(self):
        new = Line(
            self.start.copy(),
            self.end.copy(),
            self.color,
            self.line_width,
            self.line_style
        )
        new.erased_pixels = set(self.erased_pixels)
        return new