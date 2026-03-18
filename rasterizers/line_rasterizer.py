from models import LineStyle, Line
from rasterizers import Rasterizer
from rasters import Raster


class LineRasterizer(Rasterizer[Line]):
    def __init__(self, raster: Raster) -> None:
        super().__init__(raster)

    def rasterize(self, line: Line) -> list:
        x1, y1 = line.start.x, line.start.y
        x2, y2 = line.end.x, line.end.y
        color = line.color
        width = line.line_width
        style = line.line_style

        spine: list = []
        cx, cy = x1, y1
        dx = abs(x2 - cx)
        dy = abs(y2 - cy)
        sx = 1 if cx < x2 else -1
        sy = 1 if cy < y2 else -1
        err = dx - dy
        while True:
            spine.append((cx, cy))
            if cx == x2 and cy == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                cx += sx
            if e2 < dx:
                err += dx
                cy += sy

        if style == LineStyle.SOLID:
            visible = spine
        else:
            on  = max(1, width)     if style == LineStyle.DOTTED else max(4, width * 4)
            off = max(2, width * 2) if style == LineStyle.DOTTED else max(2, width * 2)
            period = on + off
            visible = [p for i, p in enumerate(spine) if i % period < on]

        drawn: list = []
        erased = line.erased_pixels
        set_px = self.raster.set_pixel
        dx_tot = abs(x2 - x1)
        dy_tot = abs(y2 - y1)
        for px, py in visible:
            for w in range(-(width // 2), (width + 1) // 2):
                wx = px + w * (0 if dx_tot >= dy_tot else 1)
                wy = py + w * (0 if dx_tot < dy_tot else 1)
                if (wx, wy) not in erased:
                    set_px(wx, wy, color)
                    drawn.append((wx, wy))
        return drawn