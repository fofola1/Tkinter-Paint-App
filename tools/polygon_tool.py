from tools import Tool
from models import Polygon, Line, Point, LineStyle

CLOSE_DISTANCE = 15

class PolygonTool(Tool):
    NAME = "Polygon"

    def __init__(self, app):
        super().__init__(app)
        self.current_polygon = None
        self.ctrl_held = False
        self.alt_held = False

    def _line_style(self) -> LineStyle:
        if self.ctrl_held:
            return LineStyle.DOTTED
        if self.alt_held:
            return LineStyle.DASHED
        return LineStyle.SOLID

    def on_press(self, event):
        point = Point(event.x, event.y)

        if self.current_polygon is None:
            self.current_polygon = Polygon(
                [point],
                self.app.current_color,
                self.app.current_size,
                self._line_style(),
                closed=False,
            )
            self.app.canvas_rasterizer.add_shape(self.current_polygon)
        else:
            if len(self.current_polygon.points) >= 3:
                if point.distance(self.current_polygon.points[0]) < CLOSE_DISTANCE:
                    self._close_polygon()
                    self.app.render()
                    return
            self.current_polygon.add_point(point)
            self.current_polygon.line_style = self._line_style()
            self.app.canvas_rasterizer.mark_dirty(self.current_polygon)
        self.app.render()

    def on_motion(self, event):
        if self.current_polygon and len(self.current_polygon.points) >= 1:
            last = self.current_polygon.points[-1]
            guide = Line(
                Point(last.x, last.y), Point(event.x, event.y),
                self.app.current_color, 1, LineStyle.DOTTED,
            )
            self.app.canvas_rasterizer.preview_shapes = [guide]
            self.app.render()

    def on_right_click(self, event):
        if self.current_polygon and len(self.current_polygon.points) >= 3:
            self._close_polygon()
            self.app.render()

    def on_key_press(self, event):
        match event.keysym:
            case "Control_L" | "Control_R":
                self.ctrl_held = True
            case "Alt_L" | "Alt_R":
                self.alt_held = True
            case "Return":
                if self.current_polygon:
                    self.app.canvas_rasterizer.remove_shape(self.current_polygon)
                    self.current_polygon = None
                    self.app.canvas_rasterizer.preview_shapes = []
                    self.app.render()

    def on_key_release(self, event):
        match event.keysym:
            case "Control_L" | "Control_R":
                self.ctrl_held = False
            case "Alt_L" | "Alt_R":
                self.alt_held = False

    def _close_polygon(self):
        if self.current_polygon is not None:
            self.current_polygon.closed = True
            self.current_polygon.line_style = self._line_style()
            self.app.canvas_rasterizer.mark_dirty(self.current_polygon)
            self.current_polygon = None
        self.app.canvas_rasterizer.preview_shapes = []

    def cleanup(self):
        if self.current_polygon:
            if len(self.current_polygon.points) >= 3:
                self._close_polygon()
            else:
                self.app.canvas_rasterizer.remove_shape(self.current_polygon)
                self.current_polygon = None
        self.app.canvas_rasterizer.preview_shapes = []