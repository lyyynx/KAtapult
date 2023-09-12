import math
from functools import cached_property
from typing import Literal, Generator

import cv2
import numpy as np

GRAVITATIONAL_CONSTANT = 9.81
HIT_RADIUS = 5


class Tank:
    def __init__(self, x_position: int, y_position: int) -> None:
        self.x_position = x_position
        self.y_position = y_position

    def shoot(self, angle: int, velocity: int) -> Generator[None, None, None]:
        angle_ = self.direction * angle * math.pi / 180
        for i in range(HIT_RADIUS + 5, 1000):
            x_i = velocity * math.cos(angle_) * i + self.x_position  # todo: correct velocity * i ??
            y_i = (
                    -0.5 * GRAVITATIONAL_CONSTANT * i**2
                    + velocity * math.sin(angle_) * i
                    + self.y_position
            )

            yield x_i, y_i

    def draw(self, screen: np.array) -> np.array:
        screen = cv2.circle(screen, (self.x_position, self.y_position), 7, [0.5], -1)
        return screen

    def is_hit(self, x: int, y: int) -> bool:
        if abs(x - self.x_position) + abs(y - self.y_position) < HIT_RADIUS:
            return True

        return False

    @cached_property
    def direction(self) -> Literal[1, -1]:
        if self.x_position < 10:
            return 1
        else:
            return -1
