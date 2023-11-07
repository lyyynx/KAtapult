import math
from functools import cached_property
from typing import Literal, Generator

from output.drawable import Drawable, Rectangle, Circle
from utils.constants import HIT_RADIUS
from utils.units import GRAVITATIONAL_CONSTANT


class Tank(Drawable):
    def __init__(self, x_position: int, y_position: int) -> None:
        self.x_position = x_position
        self.y_position = y_position

    def shoot(self, angle: int, velocity: int) -> Generator[None, None, None]:
        # todo implement shot
        ...

    def is_hit(self, x: int, y: int) -> bool:
        # todo: implement hit detection
        ...

    @cached_property
    def direction(self) -> Literal[1, -1]:
        # todo: implement direction tank is shooting to (1=right, -1=left)
        ...

    @property
    def sprite(self) -> list[Rectangle | Circle]:
        return []  # todo: define tank shape
