from tools import Tool
from models import Line, Point, LineStyle

from math import hypot, atan2, cos, sin, pi


class LineTool(Tool):
    NAME = "Line"

    def __init__(self, app):
        super().__init__(app)
        self.start_point = None
        self.current_line = None
        self._last_end = None
        self.shift_held = False
        self.ctrl_held = False
        self.alt_held = False

    def _line_style(self) -> LineStyle:
        if self.ctrl_held:
            return LineStyle.DOTTED
        if self.alt_held:
            return LineStyle.DASHED
        return LineStyle.SOLID

    def _align(self, start: Point, end: Point) -> Point:
        if not self.shift_held:
            return end
        dx = end.x - start.x
        dy = end.y - start.y
        length = hypot(dx, dy)
        if length == 0:
            return end
        angle = atan2(dy, dx)
        snapped = round(angle / (pi / 4)) * (pi / 4)
        return Point(start.x + int(length * cos(snapped)),
                     start.y + int(length * sin(snapped)))

    def on_press(self, event):
        self.start_point = Point(event.x, event.y)
        self.current_line = Line(
            self.start_point.copy(), self.start_point.copy(),
            self.app.current_color, self.app.current_size,
            self._line_style(),
        )
        self.app.canvas_rasterizer.add_shape(self.current_line)

    def _apply_to_line(self, raw_end: Point):
        if not self.current_line or not self.start_point:
            return
        end = self._align(self.start_point, raw_end)
        self.current_line.end = end
        self.current_line.points = [self.current_line.start, self.current_line.end]
        self.current_line.line_style = self._line_style()
        self.app.canvas_rasterizer.mark_dirty(self.current_line)

    def on_drag(self, event):
        if not self.current_line:
            return
        self._last_end = Point(event.x, event.y)
        self._apply_to_line(self._last_end)
        self.app.render()

    def on_release(self, event):
        if not self.current_line:
            return
        self._last_end = None
        self._apply_to_line(Point(event.x, event.y))
        self.current_line = None
        self.start_point = None
        self.app.render()

    def on_key_press(self, event):
        changed = False
        if event.keysym in ("Shift_L", "Shift_R"):
            self.shift_held = True; changed = True
        elif event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = True; changed = True
        elif event.keysym in ("Alt_L", "Alt_R"):
            self.alt_held = True; changed = True
        if changed and self.current_line and self._last_end:
            self._apply_to_line(self._last_end)
            self.app.render()

    def on_key_release(self, event):
        changed = False
        if event.keysym in ("Shift_L", "Shift_R"):
            self.shift_held = False; changed = True
        elif event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = False; changed = True
        elif event.keysym in ("Alt_L", "Alt_R"):
            self.alt_held = False; changed = True
        if changed and self.current_line and self._last_end:
            self._apply_to_line(self._last_end)
            self.app.render()