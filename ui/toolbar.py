import tkinter as tk
from tkinter import colorchooser


class Toolbar(tk.Frame):
    PREDEFINED_COLORS = [
        "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
        "#FFFF00", "#FF00FF", "#00FFFF", "#808080"
    ]

    TOOLS = ["Line", "Rectangle", "Oval", "Polygon", "Fill", "Erase", "Move"]
    
    def __init__(self, parent, app):
        super().__init__(parent, bd=1, relief=tk.RAISED, bg="#e8e8e8",)
        self.app = app
        self.last_custom_color: str | None = None
        self._build()

    def _build(self):
        tf = tk.LabelFrame(
            self,
            text="Tools",
            padx=4,
            pady=2,
            bg="#e8e8e8",
            font=("Arial", 9),
        )
        tf.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.Y)

        self.tool_var = tk.StringVar(value="Line")
        for name in self.TOOLS:
            tk.Radiobutton(
                tf,
                text=name,
                variable=self.tool_var,
                value=name,
                command=self._on_tool,
                bg="#e8e8e8",
                indicatoron=False,
                width=8,
                padx=2,
                pady=2,
                font=("Arial", 9),
                selectcolor="#b0c4de",
            ).pack(side=tk.LEFT, padx=1)

        sf = tk.LabelFrame(
            self,
            text="Size",
            padx=4,
            pady=2,
            bg="#e8e8e8",
            font=("Arial", 9),
        )
        sf.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.Y)

        self.size_var = tk.IntVar(value=2)
        self.size_scale = tk.Scale(
            sf,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            command=self._on_size,
            length=110,
            bg="#e8e8e8",
            highlightthickness=0,
        )
        self.size_scale.pack()

        cf = tk.LabelFrame(
            self,
            text="Color",
            padx=4,
            pady=2,
            bg="#e8e8e8",
            font=("Arial", 9),
        )
        cf.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.Y)

        self.color_display = tk.Canvas(
            cf,
            width=28,
            height=28,
            bg="#000000",
            bd=2,
            relief=tk.SUNKEN,
            highlightthickness=0,
        )
        self.color_display.pack(side=tk.LEFT, padx=4)

        grid = tk.Frame(cf, bg="#e8e8e8")
        grid.pack(side=tk.LEFT, padx=4)
        for i, c in enumerate(self.PREDEFINED_COLORS):
            row, col = divmod(i, 10)
            btn = tk.Button(
                grid,
                bg=c,
                width=2,
                height=1,
                bd=1,
                relief=tk.RAISED,
                command=lambda clr=c: self._set_color(clr),
            )
            btn.grid(row=row, column=col, padx=0, pady=0)

        self._last_btn = tk.Button(
            cf,
            text="Last\nCustom",
            command=self._use_last_custom,
            width=5,
            height=2,
            bg="#e8e8e8",
            state=tk.DISABLED,
            font=("Arial", 8),
        )
        self._last_btn.pack(side=tk.LEFT, padx=4)

        tk.Button(
            cf,
            text="Pick\nColor",
            command=self._pick_color,
            width=5,
            height=2,
            bg="#e8e8e8",
            font=("Arial", 8),
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            self,
            text="Clear",
            command=self.app.clear_canvas_and_cache,
            width=8,
            bg="#f2dede",
            activebackground="#ebcccc",
            font=("Arial", 9, "bold"),
        ).pack(side=tk.RIGHT, padx=6, pady=2)

    def _on_tool(self):
        self.app.set_tool(self.tool_var.get())

    def _on_size(self, _val):
        self.app.current_size = self.size_var.get()

    def _set_color(self, color: str):
        self.app.current_color = color
        self.color_display.configure(bg=color)

    def _use_last_custom(self):
        if self.last_custom_color:
            self._set_color(self.last_custom_color)

    def _pick_color(self):
        result = colorchooser.askcolor(
            initialcolor=self.app.current_color, title="Choose Color",
        )
        if result[1]:
            self.last_custom_color = result[1]
            self._last_btn.configure(state=tk.NORMAL, bg=result[1])
            self._set_color(result[1])