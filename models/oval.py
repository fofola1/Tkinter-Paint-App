from models import Point, Shape, LineStyle

class Oval(Shape):
    def __init__(
        self,
        center: Point | None = None,
        rx: int = 0,
        ry: int = 0,
        color: str = "#000000",
        line_width: int = 1,
        line_style: LineStyle = LineStyle.SOLID,
        filled: bool = False,
        fill_color: str | None = None
    ):
        super().__init__(color, line_width, line_style)
        self.center = center
        self.rx = rx
        self.ry = ry
        self.filled = filled
        self.fill_color = fill_color
        # Initialize points for move() to work
        if self.center:
            self.points = [self.center]
        else:
            self.points = []

    def copy(self):
        new = Oval(
            self.center.copy() if self.center else None,
            self.rx,
            self.ry,
            self.color,
            self.line_width,
            self.line_style,
            self.filled,
            self.fill_color
        )
        new.erased_pixels = set(self.erased_pixels)
        return new