from models import Shape
from rasters import Raster

from typing import TypeVar, Generic


T = TypeVar('T', bound=Shape)

class Rasterizer(Generic[T]):
    def __init__(
        self,
        raster: Raster,
    ) -> None:
        self.raster = raster

    def rasterize(
        self,
        shape: T
    ) -> list:
        pass
