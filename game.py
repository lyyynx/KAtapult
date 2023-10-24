import math
import random
from abc import ABCMeta, abstractmethod

import cv2
import numpy as np
from pyaxidraw.axidraw import AxiDraw

from building import Building
from explosion import Explosion
from tank import Tank, BLAST_RADIUS

PX_TO_INCH = 1 / 96
ANGLE_TO_RADIANS = math.pi / 180


class TankGame(metaclass=ABCMeta):
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width

        self.buildings: list[Building] = []
        self.tanks: dict[int:Tank] = {}
        self.explosions: list[Explosion] = []
        self.screen = np.zeros((height, width))
        self.game_over = False

    @abstractmethod
    def create_buildings(self, number_of_buildings: int) -> None:
        ...

    @abstractmethod
    def place_tanks(self) -> None:
        ...

    @abstractmethod
    def start_game(self) -> None:
        ...


class TwoPlayerTankGame(TankGame):
    def __init__(self, output: AxiDraw | None = None) -> None:
        super().__init__(595, 375)
        self.output = output

        self.active_player = 1

    def create_buildings(self, number_of_buildings: int) -> None:
        for _ in range(number_of_buildings):
            self.buildings.append(
                Building(random.randint(0, self.width), random.randint(10, self.height))
            )
            # todo: buildings go over right edge
            # todo: when distance to edge too short, widen building to fit to edge

    def place_tanks(self) -> None:
        buildings_on_left = [
            building.height
            for building in self.buildings
            if building.x_position - building.width < 5
        ]
        max_left_height = max(buildings_on_left) if len(buildings_on_left) > 0 else 0
        self.tanks[1] = Tank(5, max_left_height)

        buildings_on_right = [
            building.height
            for building in self.buildings
            if building.x_position + building.width > self.width - 5
        ]
        max_right_height = max(buildings_on_right) if len(buildings_on_right) > 0 else 0
        self.tanks[-1] = Tank(self.width - 5, max_right_height)

    def start_game(self) -> None:
        self.create_buildings(3)
        self.place_tanks()
        self.screen.fill(255)
        self.draw_canvas()
        self.draw_playground()

        while not self.game_over:
            projectile_path = []
            angle, force = self._get_command()
            for i, (projectile_x, projectile_y) in enumerate(
                self.tanks[self.active_player].shoot(angle, force * 10)
            ):
                x_, y_ = int(projectile_x), int(projectile_y)
                if (
                    i % 10 in [0, 9]  # first and last dash point
                    and i // 10 % 2 == 0  # each dash has width 10
                    and 0 < x_ < self.width
                    and 0 < y_ < self.height
                ):
                    projectile_path.append((x_, self.height - y_))

                self.screen = cv2.circle(self.screen, (x_, y_), 2, [0.2], 2)
                if self._check_hit(x_, y_):
                    if isinstance(self.output, AxiDraw):
                        self.draw_path(projectile_path)
                        self.draw_circle((x_, self.height - y_), BLAST_RADIUS)
                    print("hit")
                    break

                if projectile_x < 0 or projectile_x > self.width or projectile_y < 0:
                    self.draw_path(projectile_path)
                    print("out")
                    break

            self.active_player *= -1

    def _check_hit(self, x: int, y: int) -> bool:
        for tank in self.tanks.values():
            if tank.is_hit(x, y):
                self.game_over = True
                return True

        for building in self.buildings:
            if building.is_hit(x, y):
                return True

        return False

    def _get_command(self) -> tuple[int, int]:
        angle, force = input(
            f"Player {self.active_player}: Enter angle and velocity (i.e. 50 160) "
        ).split()
        # todo: validate input
        return int(angle), int(force)

    def draw_canvas(self) -> None:
        if self.output is None:
            self.screen = cv2.line(self.screen, (0, 0), (0, self.height), [0], 4)
            self.screen = cv2.line(
                self.screen, (0, self.height), (self.width, self.height), [0], 4
            )
            self.screen = cv2.line(
                self.screen, (self.width, 0), (self.width, self.height), [0], 4
            )
            self.screen = cv2.line(self.screen, (0, 0), (self.width, 0), [0], 4)
        elif isinstance(self.output, AxiDraw):
            self.draw_rectangle((0, 0), (self.width, self.height))
        else:
            raise NotImplemented(f"Output device {self.output} not implemented")

    def draw_playground(self) -> None:
        if self.output is None:
            for building in self.buildings:
                self.screen = building.draw(self.screen)

            for tank in self.tanks.values():
                self.screen = tank.draw(self.screen)

            cv2.imshow("battlefield", cv2.flip(self.screen, 0))
            cv2.waitKey(10)
        elif isinstance(self.output, AxiDraw):
            for building in self.buildings:
                self.draw_rectangle(
                    (
                        building.x_position - building.width // 2,
                        self.height - building.height,
                    ),
                    (building.x_position + building.width // 2, self.height),
                )

            for tank in self.tanks.values():
                self.draw_rectangle(
                    (tank.x_position - 5, self.height - tank.y_position + 5),
                    (tank.x_position + 5, self.height - tank.y_position - 5),
                )

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

        self.output.goto(*path_[0])
        self.output.pendown()

        for i, point in enumerate(path_):
            if i % 2 == 0:
                self.output.pendown()
            else:
                self.output.penup()

            self.output.goto(*point)

        self.output.penup()
        self.output.goto(0, 0)
