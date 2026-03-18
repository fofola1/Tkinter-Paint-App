from tools import Tool


class FillTool(Tool):
    NAME = "Fill"

    def on_press(self, event):
        self.app.canvas_rasterizer.fill(
            event.x, event.y, self.app.current_color,
        )
        self.app.render()