import cv2
import numpy as np

from output.output_device import OutputDevice


class ScreenPlotter(OutputDevice):
    def __init__(self, screen: np.array, width: int, height: int) -> None:
        self.screen = screen
        self.width = width
        self.height = height

        self._init_screen()

    def draw_rectangle(
        self, top_left: tuple[int, int], bottom_right: tuple[int, int]
    ) -> None:
        self.screen = cv2.rectangle(
            self.screen,
            (top_left[0], self.height - top_left[1]),
            (bottom_right[0], self.height - bottom_right[1]),
            [0],
            4,
        )
        cv2.imshow("KAtapult", self.screen)
        cv2.waitKey(1)

    def draw_circle(self, center: tuple[int, int], radius: int) -> None:
        self.screen = cv2.circle(
            self.screen, (center[0], self.height - center[1]), radius, [0], 4
        )
        cv2.imshow("KAtapult", self.screen)
        cv2.waitKey(1)

    def draw_path(self, path: list[tuple[int, int]]) -> None:
        for i in range(0, len(path), 20):
            try:
                point_a = path[i]
                point_b = path[i + 10]
            except IndexError:
                break

            self.screen = cv2.line(
                self.screen,
                (point_a[0], self.height - point_a[1]),
                (point_b[0], self.height - point_b[1]),
                [0],
                4,
            )

        cv2.imshow("KAtapult", self.screen)
        cv2.waitKey(1)

    def _init_screen(self):
        self.screen.fill(255)
        cv2.imshow("KAtapult", self.screen)
        cv2.waitKey(1)
