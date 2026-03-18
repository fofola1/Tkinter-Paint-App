import os
import tempfile
import tkinter as tk

class Raster:
    def __init__(
        self,
        width: int,
        height: int,
        background: tuple[int, int, int] = (255, 255, 255),
    ):
        self.width = width
        self.height = height
        self.BACKGROUND = background
        self.buffer = bytearray(b"\xff" * (width * height * 3))
        self._image: tk.PhotoImage | None = None
        fd, self._tmp_path = tempfile.mkstemp(suffix=".ppm")
        os.close(fd)

    def set_pixel(self, x: int, y: int, color: tuple[int, int, int] | str) -> None:
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            r, g, b = self.parse_color(color)
            self.buffer[idx] = r
            self.buffer[idx + 1] = g
            self.buffer[idx + 2] = b

    def get_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            return (self.buffer[idx], self.buffer[idx + 1], self.buffer[idx + 2])
        return self.BACKGROUND

    def clear(self) -> None:
        self.buffer[:] = b"\xff" * (self.width * self.height * 3)

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.buffer = bytearray(b"\xff" * (width * height * 3))

    def to_photo_image(self) -> tk.PhotoImage:
        header = f"P6\n{self.width} {self.height}\n255\n".encode("ascii")
        with open(self._tmp_path, "wb") as f:
            f.write(header)
            f.write(self.buffer)
        self._image = tk.PhotoImage(file=self._tmp_path)
        return self._image

    def cleanup(self):
        try:
            os.unlink(self._tmp_path)
        except OSError:
            pass

    @staticmethod
    def parse_color(color) -> tuple:
        if isinstance(color, (tuple, list)):
            return (color[0], color[1], color[2])
        if isinstance(color, str):
            h = color.lstrip("#")
            if len(h) == 6:
                return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            if len(h) == 3:
                return (int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16))
        return (0, 0, 0)