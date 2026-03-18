from rasterizers import Rasterizer
from rasters import Raster
from models import Fill

class FillRasterizer(Rasterizer[Fill]):
    def __init__(self, raster: Raster) -> None:
        super().__init__(raster)

    def rasterize(self, fill: Fill) -> list:
        for px, py in fill.filled_pixels:
            if (px, py) not in fill.erased_pixels:
                self.raster.set_pixel(px, py, fill.color)
        return fill.filled_pixels