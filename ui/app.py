import tkinter as tk

from rasters import Raster
from rasterizers import CanvasRasterizer
from ui import Toolbar
from tools import (
    LineTool,
    PolygonTool,
    OvalTool,
    RectangleTool,
    FillTool,
    EraseTool,
    MoveTool
)


class PaintApp:
    CANVAS_W = 1300
    CANVAS_H = 800

    TOOL_CURSORS = {
        "Line": "crosshair",
        "Rectangle": "crosshair",
        "Oval": "crosshair",
        "Polygon": "crosshair",
        "Fill": "tcross",
        "Erase": "X_cursor",
        "Move": "fleur"
    }

    TOOL_SHORTCUTS = {
        "l": "Line",
        "r": "Rectangle",
        "o": "Oval",
        "p": "Polygon",
        "f": "Fill",
        "e": "Erase",
        "m": "Move"
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint App")
        self.root.geometry(f"{self.CANVAS_W}x{self.CANVAS_H + 70}")
        self.root.resizable(False, False)

        self.current_color: str = "#000000"
        self.current_size: int = 2

        self.raster = Raster(self.CANVAS_W, self.CANVAS_H)
        self.canvas_rasterizer = CanvasRasterizer(self.raster)

        self.toolbar = Toolbar(self.root, self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(
            self.root,
            width=self.CANVAS_W,
            height=self.CANVAS_H,
            bg="white",
            cursor="crosshair",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._image_id = None

        self.tools = {
            "Line": LineTool(self),
            "Rectangle": RectangleTool(self),
            "Oval": OvalTool(self),
            "Polygon": PolygonTool(self),
            "Fill": FillTool(self),
            "Erase": EraseTool(self),
            "Move": MoveTool(self),
        }

        self.current_tool = self.tools["Line"]

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<ButtonPress-3>", self._on_right_click)
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)

        self._render_pending = False
        self.render()

    def set_tool(self, name: str):
        self.current_tool.cleanup()
        self.current_tool = self.tools.get(name, self.tools["Line"])
        self.canvas.configure(cursor=self.TOOL_CURSORS.get(name, "crosshair"))
        self.render()

    def render(self):
        if not self._render_pending:
            self._render_pending = True
            self.root.after_idle(self._do_render)

    def _do_render(self):
        self._render_pending = False
        self.canvas_rasterizer.render_all()
        photo = self.raster.to_photo_image()
        if self._image_id is not None:
            self.canvas.itemconfig(self._image_id, image=photo)
        else:
            self._image_id = self.canvas.create_image(
                0, 0, anchor=tk.NW, image=photo
            )
        self.canvas._photo = photo

    def _on_press(self, event):
        self.current_tool.on_press(event)

    def _on_drag(self, event):
        self.current_tool.on_drag(event)

    def _on_release(self, event):
        self.current_tool.on_release(event)

    def _on_motion(self, event):
        self.current_tool.on_motion(event)

    def _on_right_click(self, event):
        self.current_tool.on_right_click(event)

    def _on_key_press(self, event):
        if event.char in self.TOOL_SHORTCUTS:
            name = self.TOOL_SHORTCUTS[event.char]
            self.set_tool(name)
            self.toolbar.tool_var.set(name)
            return
        self.current_tool.on_key_press(event)

    def _on_key_release(self, event):
        self.current_tool.on_key_release(event)

    def clear_canvas_and_cache(self):
        self.current_tool.cleanup()
        self.canvas_rasterizer.clear_all()
        self._render_pending = False
        self._do_render()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        self.raster.cleanup()
        self.root.destroy()