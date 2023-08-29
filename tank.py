import math
from functools import cached_property
from typing import Literal, Generator

import cv2
import numpy as np

GRAVITATIONAL_CONSTANT = 9.81


class Tank:
    def __init__(self, x_position: int, height: int) -> None:
        self.x_position = x_position
        self.height = height

        self.hit = False

    def shoot(self, angle: int, velocity: int) -> Generator[None, None, None]:
        angle_ = angle * math.pi / 180
        for i in range(1000):
            x_i = velocity * math.cos(angle_) * i + self.x_position,
            y_i = -0.5 * GRAVITATIONAL_CONSTANT * i ** 2 + velocity * math.sin(angle_) * i + self.height,

            yield x_i, y_i

    def draw(self, screen: np.array) -> np.array:
        screen = cv2.circle(screen, (self.x_position, self.height), 4, [255, 0, 0], -1)
        return screen

    @cached_property
    def direction(self) -> Literal[1, -1]:
        if self.x_position < 10:
            return 1
        else:
            return -1
