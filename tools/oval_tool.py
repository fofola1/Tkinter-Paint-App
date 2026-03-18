from tools import Tool
from models import Oval, Point, LineStyle


class OvalTool(Tool):
    NAME = "Oval"

    def __init__(self, app):
        super().__init__(app)
        self.start_point = None
        self.current_oval = None
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

    def _calc(self, start: Point, end: Point):
        dx = end.x - start.x
        dy = end.y - start.y
        if self.shift_held:
            side = min(abs(dx), abs(dy))
            dx = side if dx >= 0 else -side
            dy = side if dy >= 0 else -side
        cx = start.x + dx // 2
        cy = start.y + dy // 2
        rx = abs(dx) // 2
        ry = abs(dy) // 2
        return cx, cy, rx, ry

    def on_press(self, event):
        self.start_point = Point(event.x, event.y)
        self.current_oval = Oval(
            Point(event.x, event.y), 0, 0,
            self.app.current_color, self.app.current_size,
            self._line_style(),
        )
        self.app.canvas_rasterizer.add_shape(self.current_oval)

    def _apply_to_oval(self, end: Point):
        cx, cy, rx, ry = self._calc(self.start_point, end)
        self.current_oval.center = Point(cx, cy)
        self.current_oval.rx = rx
        self.current_oval.ry = ry
        self.current_oval.points = [self.current_oval.center]
        self.current_oval.line_style = self._line_style()
        self.app.canvas_rasterizer.mark_dirty(self.current_oval)

    def on_drag(self, event):
        if not self.current_oval or not self.start_point:
            return
        self._last_end = Point(event.x, event.y)
        self._apply_to_oval(self._last_end)
        self.app.render()

    def on_release(self, event):
        if not self.current_oval or not self.start_point:
            return
        self._last_end = None
        self._apply_to_oval(Point(event.x, event.y))
        self.current_oval = None
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
        if changed and self.current_oval and self._last_end:
            self._apply_to_oval(self._last_end)
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
        if changed and self.current_oval and self._last_end:
            self._apply_to_oval(self._last_end)
            self.app.render()