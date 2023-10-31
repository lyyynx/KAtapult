import cv2
import numpy as np

from tank import BLAST_RADIUS


class Building:
    def __init__(self, x_position: int, height: int, width: int = 30) -> None:
        self.x_position = x_position
        self.height = height
        self.width = width

        self.hits = []

    def draw(self, screen: np.array) -> np.array:
        screen = cv2.line(
            screen,
            (self.x_position - self.width // 2, 0),
            (self.x_position - self.width // 2, self.height),
            [0],
            2,
        )
        screen = cv2.line(
            screen,
            (self.x_position - self.width // 2, self.height),
            (self.x_position + self.width // 2, self.height),
            [0],
            2,
        )
        screen = cv2.line(
            screen,
            (self.x_position + self.width // 2, 0),
            (self.x_position + self.width // 2, self.height),
            [0],
            2,
        )

        for hit in self.hits:
            screen = cv2.circle(screen, hit, BLAST_RADIUS, [0], 2)

        return screen

    def is_hit(self, x: int, y: int) -> bool:
        if self.x_position - self.width // 2 <= x <= self.x_position + self.width // 2 and self.height > y:
            for hit in self.hits:
                if (x - hit[0])**2 + (y-hit[1])**2 < BLAST_RADIUS**2:
                    return False

            self.hits.append((x, y))
            return True

        return False
