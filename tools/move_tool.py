from tools import Tool
from models import Point, Polygon, Line, Rectangle, Oval
from math import hypot, atan2, cos, sin, pi

POINT_SNAP_RADIUS = 10


class MoveTool(Tool):
    NAME = "Move"
    ctrl_held = False
    shift_held = False

    def __init__(self, app):
        super().__init__(app)
        self.selected_shape = None
        self._selected_point = None
        self._modification_mode = None
        self._selected_rect_corner = None
        self._last_x = 0
        self._last_y = 0

    def _get_modifiable_points(self, shape):
        if isinstance(shape, Polygon):
            return shape.points
        elif isinstance(shape, Line):
            return [shape.start, shape.end]
        return []

    def _get_rectangle_corners(self, rect: Rectangle):
        x1, y1 = rect.p1.x, rect.p1.y
        x2, y2 = rect.p2.x, rect.p2.y
        return [
            ("p1", Point(x1, y1)),
            ("p2", Point(x2, y2)),
            ("p1x_p2y", Point(x1, y2)),
            ("p2x_p1y", Point(x2, y1)),
        ]

    def _apply_line_snap(self, start: Point, end: Point) -> Point:
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

    def _apply_rectangle_snap(self, anchor: Point, dragged: Point) -> Point:
        if not self.shift_held:
            return dragged
        dx = dragged.x - anchor.x
        dy = dragged.y - anchor.y
        side = max(abs(dx), abs(dy))
        return Point(
            anchor.x + (side if dx >= 0 else -side),
            anchor.y + (side if dy >= 0 else -side),
        )

    def on_press(self, event):
        self.selected_shape = self.app.canvas_rasterizer.hit_test(
            event.x, event.y,
        )
        self._selected_point = None
        self._modification_mode = None
        self._selected_rect_corner = None

        if self.ctrl_held and self.selected_shape:
            cursor = Point(event.x, event.y)

            if isinstance(self.selected_shape, Oval):
                if self.selected_shape.center and self.selected_shape.center.distance(cursor) <= POINT_SNAP_RADIUS:
                    self._selected_point = self.selected_shape.center
                    self._modification_mode = "oval_center"
                else:
                    self._modification_mode = "oval_resize"
            elif isinstance(self.selected_shape, Rectangle):
                corners = self._get_rectangle_corners(self.selected_shape)
                corner_id, corner_point = min(
                    corners,
                    key=lambda c: c[1].distance(cursor),
                    default=(None, None),
                )
                if corner_point is not None and corner_point.distance(cursor) <= POINT_SNAP_RADIUS:
                    self._selected_rect_corner = corner_id
                    self._modification_mode = "rect_corner"
            else:
                points = self._get_modifiable_points(self.selected_shape)
                if points:
                    closest = min(
                        points,
                        key=lambda p: p.distance(cursor),
                        default=None,
                    )
                    if closest is not None and closest.distance(cursor) <= POINT_SNAP_RADIUS:
                        self._selected_point = closest
                        self._modification_mode = "point"

        self._last_x = event.x
        self._last_y = event.y

    def on_drag(self, event):
        if not self.selected_shape:
            return

        dx = event.x - self._last_x
        dy = event.y - self._last_y

        if self._modification_mode == "point":
            if self._selected_point is not None:
                if isinstance(self.selected_shape, Line):
                    if self._selected_point is self.selected_shape.start:
                        other_point = self.selected_shape.end
                    else:
                        other_point = self.selected_shape.start
                    snapped_end = self._apply_line_snap(other_point, Point(event.x, event.y))
                    self._selected_point.x = snapped_end.x
                    self._selected_point.y = snapped_end.y
                else:
                    self._selected_point.x += dx
                    self._selected_point.y += dy
        elif self._modification_mode == "rect_corner":
            if isinstance(self.selected_shape, Rectangle) and self._selected_rect_corner is not None:
                r = self.selected_shape
                raw = Point(event.x, event.y)
                if self._selected_rect_corner == "p1":
                    snapped = self._apply_rectangle_snap(r.p2, raw)
                    r.p1.x = snapped.x
                    r.p1.y = snapped.y
                elif self._selected_rect_corner == "p2":
                    snapped = self._apply_rectangle_snap(r.p1, raw)
                    r.p2.x = snapped.x
                    r.p2.y = snapped.y
                elif self._selected_rect_corner == "p1x_p2y":
                    anchor = Point(r.p2.x, r.p1.y)
                    snapped = self._apply_rectangle_snap(anchor, raw)
                    r.p1.x = snapped.x
                    r.p2.y = snapped.y
                elif self._selected_rect_corner == "p2x_p1y":
                    anchor = Point(r.p1.x, r.p2.y)
                    snapped = self._apply_rectangle_snap(anchor, raw)
                    r.p2.x = snapped.x
                    r.p1.y = snapped.y

        elif self._modification_mode == "oval_center":
            if self._selected_point is not None:
                self._selected_point.x += dx
                self._selected_point.y += dy

        elif self._modification_mode == "oval_resize":
            if isinstance(self.selected_shape, Oval) and self.selected_shape.center:
                new_rx = abs(event.x - self.selected_shape.center.x)
                new_ry = abs(event.y - self.selected_shape.center.y)

                if self.shift_held:
                    size = max(new_rx, new_ry)
                    new_rx = size
                    new_ry = size

                self.selected_shape.rx = new_rx
                self.selected_shape.ry = new_ry
        else:
            self.selected_shape.move(dx, dy)

        self._last_x = event.x
        self._last_y = event.y
        self.app.canvas_rasterizer.mark_dirty(self.selected_shape)
        self.app.render()

    def on_release(self, event):
        self.selected_shape = None
        self._selected_point = None
        self._modification_mode = None
        self._selected_rect_corner = None

    def on_key_press(self, event):
        if event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = True
        elif event.keysym in ("Shift_L", "Shift_R"):
            self.shift_held = True

    def on_key_release(self, event):
        if event.keysym in ("Control_L", "Control_R"):
            self.ctrl_held = False
        elif event.keysym in ("Shift_L", "Shift_R"):
            self.shift_held = False