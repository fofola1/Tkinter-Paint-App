import math
from models import LineStyle, Oval
from rasters import Raster
from rasterizers import Rasterizer


class OvalRasterizer(Rasterizer[Oval]):
    def __init__(self, raster: Raster) -> None:
        super().__init__(raster)

    def rasterize(self, oval: Oval) -> list:
        cx, cy = oval.center.x, oval.center.y
        rx, ry = abs(oval.rx), abs(oval.ry)
        if rx == 0 or ry == 0:
            return []

        drawn: list = []

        if oval.filled and oval.fill_color:
            for px, py in OvalRasterizer._fill_ellipse(cx, cy, rx, ry):
                if (px, py) not in oval.erased_pixels:
                    self.raster.set_pixel(px, py, oval.fill_color)
                    drawn.append((px, py))

        outline = OvalRasterizer._midpoint_ellipse(cx, cy, rx, ry)
        styled = OvalRasterizer._apply_style(
            outline,
            oval.line_style,
            oval.line_width
        )
        for px, py in styled:
            for wx, wy in OvalRasterizer._apply_width(px, py, oval.line_width):
                if (wx, wy) not in oval.erased_pixels:
                    self.raster.set_pixel(wx, wy, oval.color)
                    drawn.append((wx, wy))
        return drawn

    @staticmethod
    def _midpoint_ellipse(cx, cy, rx, ry) -> list:
        pixels: list = []
        x, y = 0, ry
        rx2, ry2 = rx * rx, ry * ry

        p1 = ry2 - rx2 * ry + 0.25 * rx2
        dx = 2 * ry2 * x
        dy = 2 * rx2 * y
        while dx < dy:
            pixels.extend(OvalRasterizer._sym4(cx, cy, x, y))
            x += 1
            dx += 2 * ry2
            if p1 < 0:
                p1 += dx + ry2
            else:
                y -= 1
                dy -= 2 * rx2
                p1 += dx - dy + ry2

        p2 = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
        while y >= 0:
            pixels.extend(OvalRasterizer._sym4(cx, cy, x, y))
            y -= 1
            dy -= 2 * rx2
            if p2 > 0:
                p2 += rx2 - dy
            else:
                x += 1
                dx += 2 * ry2
                p2 += dx - dy + rx2
        return pixels

    @staticmethod
    def _sym4(cx, cy, x, y):
        return [(cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y)]

    @staticmethod
    def _fill_ellipse(cx, cy, rx, ry) -> list:
        pixels: list = []
        for y in range(-ry, ry + 1):
            if ry == 0:
                continue
            xr = int(rx * math.sqrt(max(0, 1 - (y / ry) ** 2)))
            for x in range(-xr, xr + 1):
                pixels.append((cx + x, cy + y))
        return pixels

    @staticmethod
    def _apply_style(pixels, style, width: int = 1):
        if style == LineStyle.SOLID:
            return pixels
        out: list = []
        if style == LineStyle.DOTTED:
            period = max(3, width * 2)
            for i, p in enumerate(pixels):
                if (i % period) == 0:
                    out.append(p)
        elif style == LineStyle.DASHED:
            on = max(8, width * 3)
            gap = max(4, width * 2)
            period = on + gap
            for i, p in enumerate(pixels):
                if (i % period) < on:
                    out.append(p)
        return out

    @staticmethod
    def _apply_width(x, y, width):
        if width <= 1:
            return [(x, y)]
        half = width // 2
        pts: list = []
        for dx in range(-half, half + 1):
            for dy in range(-half, half + 1):
                pts.append((x + dx, y + dy))
        return pts