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
        top_left_ = (top_left[0] * PX_TO_INCH, top_left[1] * PX_TO_INCH)
        bottom_right_ = (bottom_right[0] * PX_TO_INCH, bottom_right[1] * PX_TO_INCH)

        self.output.goto(*top_left_)
        self.output.pendown()
        self.output.lineto(top_left_[0], bottom_right_[1])
        self.output.lineto(*bottom_right_)
        self.output.lineto(bottom_right_[0], top_left_[1])
        self.output.lineto(*top_left_)
        self.output.penup()
        self.output.goto(0, 0)

    def draw_circle(self, center: tuple[int, int], radius: int) -> None:
        circle_points = []
        for phi in range(0, 360, 20):
            x, y = (
                radius * math.sin(phi * ANGLE_TO_RADIANS) + center[0],
                radius * math.cos(phi * ANGLE_TO_RADIANS) + center[1],
            )
            if 0 < x < self.width and 0 < y < self.height:
                circle_points.append((x * PX_TO_INCH, y * PX_TO_INCH))

        self.output.goto(*circle_points[0])
        self.output.pendown()

        for point in circle_points:
            self.output.lineto(*point)

        self.output.penup()
        self.output.goto(0, 0)

    def draw_path(self, path: list[tuple[int, int]]) -> None:
        path_ = [(point[0] * PX_TO_INCH, point[1] * PX_TO_INCH) for point in path]

        for i in range(0, len(path_), 20):
            try:
                self.output.goto(*path_[i])
                self.output.pendown()

                self.output.goto(*path_[i+10])
                self.output.pendown()
            except IndexError:
                break

        self.output.penup()
        self.output.goto(0, 0)