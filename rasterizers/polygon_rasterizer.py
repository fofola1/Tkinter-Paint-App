from models import Polygon, Line
from rasterizers import Rasterizer, LineRasterizer
from rasters import Raster


class PolygonRasterizer(Rasterizer[Polygon]):
    def __init__(self, raster: Raster) -> None:
        super().__init__(raster)

    def rasterize(self, polygon: Polygon) -> list:
        drawn: list = []
        n = len(polygon.points)
        if n < 2:
            return drawn

        edges = n if polygon.closed else n - 1
        for i in range(edges):
            p1 = polygon.points[i]
            p2 = polygon.points[(i + 1) % n]
            edge = Line(p1, p2, polygon.color,
                        polygon.line_width, polygon.line_style)
            edge.erased_pixels = polygon.erased_pixels
            drawn.extend(LineRasterizer(self.raster).rasterize(edge))
        return drawn
