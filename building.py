import cv2
import numpy as np


class Building:
    def __init__(self, x_position: int, height: int) -> None:
        self.x_position = x_position
        self.height = height

        self.width = 30

    def draw(self, screen: np.array) -> np.array:
        screen = cv2.line(
            screen,
            (self.x_position - self.width // 2, 0),
            (self.x_position - self.width // 2, self.height),
            [0, 0, 0],
            2,
        )
        screen = cv2.line(
            screen,
            (self.x_position - self.width // 2, self.height),
            (self.x_position + self.width // 2, self.height),
            [0, 0, 0],
            2,
        )
        screen = cv2.line(
            screen,
            (self.x_position + self.width // 2, 0),
            (self.x_position + self.width // 2, self.height),
            [0, 0, 0],
            2,
        )

        return screen