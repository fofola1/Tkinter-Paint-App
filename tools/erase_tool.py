from tools import Tool
from models import Line


class EraseTool(Tool):
    NAME = "Eraser"

    def __init__(self, app):
        super().__init__(app)
        self.ctrl_held = False
        self._erasing = False
        self._last_x: int | None = None
        self._last_y: int | None = None

    def on_press(self, event):
        self._last_x = event.x
        self._last_y = event.y
        if self.ctrl_held:
            self._erasing = True
            self._erase_pixels(event.x, event.y)
        else:
            shape = self.app.canvas_rasterizer.hit_test(event.x, event.y)
            if shape:
                self.app.canvas_rasterizer.remove_shape(shape)
                self.app.render()

    def on_drag(self, event):
        if self.ctrl_held:
            self._erasing = True
            self._erase(event.x, event.y)
        else:
            shape = self.app.canvas_rasterizer.hit_test(event.x, event.y)
            if shape:
                self.app.canvas_rasterizer.remove_shape(shape)
                self.app.render()
        self._last_x = event.x
        self._last_y = event.y

    def on_release(self, event):
        if self._erasing:
            self._check_splits()
            self._erasing = False
            self.app.render()
        self._last_x = None
        self._last_y = None

    def on_key_press(self, event):
        if event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = True

    def on_key_release(self, event):
        if event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = False

    def _erase(self, x: int, y: int):
        lx, ly = self._last_x, self._last_y
        if lx is None or ly is None:
            self._erase_pixels(x, y)
            return
        dx = abs(x - lx)
        dy = abs(y - ly)
        sx = 1 if lx < x else -1
        sy = 1 if ly < y else -1
        err = dx - dy
        while True:
            self._erase_pixels(lx, ly)
            if lx == x and ly == y:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                lx += sx
            if e2 < dx:
                err += dx
                ly += sy

    def _erase_pixels(self, x: int, y: int):
        size = self.app.current_size
        half = max(size // 2, 1)
        brush: set = set()
        for dx in range(-half, half + 1):
            for dy in range(-half, half + 1):
                if dx * dx + dy * dy <= half * half + half:
                    brush.add((x + dx, y + dy))

        cr = self.app.canvas_rasterizer
        for shape in list(cr.shapes):
            pixels = cr.shape_pixels.get(shape, set())
            overlap = brush & pixels
            if overlap:
                cr.erase_pixels(shape, overlap)
        self.app.render()

    def _check_splits(self):
        cr = self.app.canvas_rasterizer
        to_remove: list = []
        to_add: list = []

        for shape in cr.shapes:
            if isinstance(shape, Line) and shape.erased_pixels:
                parts = cr.check_line_split(shape)
                if len(parts) > 1:
                    to_remove.append(shape)
                    to_add.extend(parts)

        for s in to_remove:
            cr.remove_shape(s)
        for s in to_add:
            cr.add_shape(s)