from models import (
    Line,
    Polygon,
    Oval,
    Rectangle,
    Fill,
)
from rasterizers import (
    LineRasterizer,
    PolygonRasterizer,
    OvalRasterizer,
    RectangleRasterizer,
    FillRasterizer,
)


def _build_segments(idx_rgb: list) -> list:
    segments = []
    n = len(idx_rgb)
    i = 0
    while i < n:
        idx0, r, g, b = idx_rgb[i]
        j = i + 1
        while (j < n
                and idx_rgb[j][0] == idx0 + (j - i) * 3
                and idx_rgb[j][1] == r
                and idx_rgb[j][2] == g
                and idx_rgb[j][3] == b):
            j += 1
        segments.append((idx0, bytes([r, g, b]) * (j - i)))
        i = j
    return segments


class CanvasRasterizer:
    def __init__(self, raster):
        self.raster = raster
        self.shapes: list = []
        self.shape_pixels: dict = {}
        self._pixel_color_cache: dict = {}
        self._dirty: set = set()
        self.preview_shapes: list = []
        self.line_rasterizer = LineRasterizer(raster)
        self.polygon_rasterizer = PolygonRasterizer(raster)
        self.oval_rasterizer = OvalRasterizer(raster)
        self.rectangle_rasterizer = RectangleRasterizer(raster)
        self.fill_rasterizer = FillRasterizer(raster)

    def add_shape(self, shape):
        self.shapes.append(shape)
        self._dirty.add(shape)

    def remove_shape(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)
        self.shape_pixels.pop(shape, None)
        self._pixel_color_cache.pop(shape, None)
        self._dirty.discard(shape)

    def clear_all(self):
        self.shapes.clear()
        self.shape_pixels.clear()
        self._pixel_color_cache.clear()
        self._dirty.clear()
        self.preview_shapes.clear()
        self.raster.clear()

    def mark_dirty(self, shape):
        self._dirty.add(shape)

    def hit_test(self, x: int, y: int, radius: int = 5):
        for shape in reversed(self.shapes):
            pixels = self.shape_pixels.get(shape, set())
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if (x + dx, y + dy) in pixels:
                        return shape
        return None

    def erase_pixels(self, shape, pixels: set):
        shape.erased_pixels |= pixels
        self.shape_pixels[shape] = self.shape_pixels.get(shape, set()) - pixels
        self._dirty.add(shape)

    def fill(self, x: int, y: int, color: str):
        target = self.raster.get_pixel(x, y)
        fill_rgb = self.raster.parse_color(color)
        if target == fill_rgb:
            return
        width, height = self.raster.width, self.raster.height
        visited: set = set()
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            if not (0 <= cx < width and 0 <= cy < height):
                continue
            if self.raster.get_pixel(cx, cy) != target:
                continue
            visited.add((cx, cy))
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        if not visited:
            return
        fill_shape = Fill(color)
        fill_shape.filled_pixels = visited
        self.add_shape(fill_shape)

    def render_all(self):
        for shape in list(self._dirty):
            if shape in self.shapes:
                self._rasterize_to_cache(shape)
        self._dirty.clear()

        self.raster.clear()
        buf = self.raster.buffer
        for shape in self.shapes:
            for idx, data in self._pixel_color_cache.get(shape, ()):
                buf[idx:idx + len(data)] = data

        for shape in self.preview_shapes:
            self._rasterize_shape(shape)

    def _rasterize_to_cache(self, shape):
        if isinstance(shape, Fill):
            self._cache_fill(shape)
            return

        recorded: list = []
        original_set_pixel = self.raster.set_pixel
        parse = self.raster.parse_color
        w, h = self.raster.width, self.raster.height

        def _recording_set_pixel(x, y, color):
            xi, yi = int(x), int(y)
            if 0 <= xi < w and 0 <= yi < h:
                r, g, b = parse(color)
                recorded.append((xi, yi, r, g, b))

        self.raster.set_pixel = _recording_set_pixel
        try:
            self._rasterize_shape(shape)
        finally:
            self.raster.set_pixel = original_set_pixel

        self.shape_pixels[shape] = {(x, y) for x, y, *_ in recorded}
        idx_rgb = sorted(((yi * w + xi) * 3, r, g, b) for xi, yi, r, g, b in recorded)
        self._pixel_color_cache[shape] = _build_segments(idx_rgb)

    def _cache_fill(self, fill: Fill):
        r, g, b = self.raster.parse_color(fill.color)
        w, h = self.raster.width, self.raster.height
        erased = fill.erased_pixels
        hit_set = set()
        indices = []
        for px, py in fill.filled_pixels:
            if (px, py) not in erased and 0 <= px < w and 0 <= py < h:
                hit_set.add((px, py))
                indices.append((py * w + px) * 3)
        self.shape_pixels[fill] = hit_set
        indices.sort()
        n = len(indices)
        rgb_unit = bytes([r, g, b])
        segments = []
        i = 0
        while i < n:
            idx0 = indices[i]
            j = i + 1
            while j < n and indices[j] == idx0 + (j - i) * 3:
                j += 1
            segments.append((idx0, rgb_unit * (j - i)))
            i = j
        self._pixel_color_cache[fill] = segments

    def _rasterize_shape(self, shape) -> list:
        if isinstance(shape, Fill):
            return self.fill_rasterizer.rasterize(shape)
        if isinstance(shape, Line):
            return self.line_rasterizer.rasterize(shape)
        if isinstance(shape, Polygon):
            return self.polygon_rasterizer.rasterize(shape)
        if isinstance(shape, Oval):
            return self.oval_rasterizer.rasterize(shape)
        if isinstance(shape, Rectangle):
            return self.rectangle_rasterizer.rasterize(shape)
        return []