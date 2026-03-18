from models import Point, Shape, LineStyle

class Rectangle(Shape):
    def __init__(
        self,
        p1: Point | None = None,
        p2: Point | None = None,
        color: str = "#000000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID,
        filled: bool = False,
        fill_color: str | None = None
    ):
        super().__init__(color, line_width, line_style)
        self.p1 = p1 or Point()
        self.p2 = p2 or Point()
        self.filled = filled
        self.fill_color = fill_color
        self.points = [self.p1, self.p2]

    def copy(self):
        new = Rectangle(
            self.p1.copy(),
            self.p2.copy(),
            self.color,
            self.line_width,
            self.line_style,
            self.filled,
            self.fill_color
        )
        new.erased_pixels = set(self.erased_pixels)
        return new