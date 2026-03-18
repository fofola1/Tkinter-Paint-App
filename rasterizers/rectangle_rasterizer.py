from models import Rectangle, Point, Line
from rasterizers import Rasterizer, LineRasterizer
from rasters import Raster


class RectangleRasterizer(Rasterizer[Rectangle]):
    def __init__(self, raster: Raster) -> None:
        super().__init__(raster)

    def rasterize(self, Rectangle: Rectangle) -> list:
        x1, y1 = Rectangle.p1.x, Rectangle.p1.y
        x2, y2 = Rectangle.p2.x, Rectangle.p2.y
        left, right = min(x1, x2), max(x1, x2)
        top, bottom = min(y1, y2), max(y1, y2)

        drawn: list = []

        corners = [
            Point(left, top), Point(right, top),
            Point(right, bottom), Point(left, bottom),
        ]
        for i in range(4):
            edge = Line(corners[i], corners[(i + 1) % 4],
                        Rectangle.color, Rectangle.line_width, Rectangle.line_style)
            edge.erased_pixels = Rectangle.erased_pixels
            drawn.extend(LineRasterizer(self.raster).rasterize(edge))
        return drawn