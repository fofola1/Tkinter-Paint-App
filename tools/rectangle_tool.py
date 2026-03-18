from tools import Tool
from models import Rectangle, Point, LineStyle


class RectangleTool(Tool):
    NAME = "Rectangle"

    def __init__(self, app):
        super().__init__(app)
        self.start_point = None
        self.current_rectangle = None
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

    def _calc(self, start: Point, end: Point) -> Point:
        if self.shift_held:
            dx = end.x - start.x
            dy = end.y - start.y
            side = max(abs(dx), abs(dy))
            return Point(
                start.x + (side if dx >= 0 else -side),
                start.y + (side if dy >= 0 else -side),
            )
        return end

    def on_press(self, event):
        self.start_point = Point(event.x, event.y)
        self.current_rectangle = Rectangle(
            self.start_point.copy(), self.start_point.copy(),
            self.app.current_color, self.app.current_size,
            self._line_style(),
        )
        self.app.canvas_rasterizer.add_shape(self.current_rectangle)

    def _apply_to_rect(self, end: Point):
        if not self.current_rectangle or not self.start_point:
            return
        end = self._calc(self.start_point, end)
        self.current_rectangle.p2 = end
        self.current_rectangle.points = [
            self.current_rectangle.p1,
            self.current_rectangle.p2
        ]
        self.current_rectangle.line_style = self._line_style()
        self.app.canvas_rasterizer.mark_dirty(self.current_rectangle)

    def on_drag(self, event):
        if not self.current_rectangle or not self.start_point:
            return
        self._last_end = Point(event.x, event.y)
        self._apply_to_rect(self._last_end)
        self.app.render()

    def on_release(self, event):
        if not self.current_rectangle or self.start_point is None:
            return
        self._last_end = None
        self._apply_to_rect(Point(event.x, event.y))
        self.current_rectangle = None
        self.start_point = None
        self.app.render()

    def on_key_press(self, event):
        changed = False
        match event.keysym:
            case "Shift_L" | "Shift_R":
                self.shift_held = True
                changed = True
            case "Control_L" | "Control_R":
                self.ctrl_held = True
                changed = True
            case "Alt_L" | "Alt_R":
                self.alt_held = True
                changed = True
        if changed and self.current_rectangle and self._last_end:
            self._apply_to_rect(self._last_end)
            self.app.render()

    def on_key_release(self, event):
        changed = False
        match event.keysym:
            case "Shift_L" | "Shift_R":
                self.shift_held = False
                changed = True
            case "Control_L" | "Control_R":
                self.ctrl_held = False
                changed = True
            case "Alt_L" | "Alt_R":
                self.alt_held = False
                changed = True
        if changed and self.current_rectangle and self._last_end:
            self._apply_to_rect(self._last_end)
            self.app.render()