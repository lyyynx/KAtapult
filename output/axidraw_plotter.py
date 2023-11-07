import math

from pyaxidraw.axidraw import AxiDraw

from output.output_device import OutputDevice
from utils.units import PX_TO_INCH, ANGLE_TO_RADIANS


class AxidrawPlotter(OutputDevice):
    def __init__(self, output: AxiDraw, width: int, height: int) -> None:
        self.output = output
        self.width = width
        self.height = height

    def draw_rectangle(
        self, top_left: tuple[int, int], bottom_right: tuple[int, int]
    ) -> None:
        # todo: draw rectangle
        ...

    def draw_circle(self, center: tuple[int, int], radius: int) -> None:
        # todo: draw circle
        ...

    def draw_path(self, path: list[tuple[int, int]]) -> None:
        # todo: draw path
        ...

