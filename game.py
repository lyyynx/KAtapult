import random
from abc import ABCMeta, abstractmethod
from functools import cached_property

import numpy as np
from pyaxidraw.axidraw import AxiDraw

from objects.building import Building
from objects.explosion import Explosion
from output.axidraw_plotter import AxidrawPlotter
from output.output_device import OutputDevice
from output.screen_plotter import ScreenPlotter
from objects.tank import Tank
from utils.constants import BLAST_RADIUS


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

    @abstractmethod
    def output_device(self) -> OutputDevice:
        ...


class TwoPlayerTankGame(TankGame):
    def __init__(self, output: AxiDraw | None = None) -> None:
        super().__init__(595, 375)
        self.output = output

        self.active_player = 1

    def create_buildings(self, number_of_buildings: int) -> None:
        for _ in range(number_of_buildings):
            building_x = random.randint(10, self.width-10)
            distance_to_edge = min(building_x - 20, self.width - building_x + 20)

            if abs(building_x < 10):
                self.buildings.append(
                    Building(building_x, random.randint(10, self.height - 10), width=20 + distance_to_edge)
                )

            self.buildings.append(
                Building(building_x, random.randint(10, self.height-10))
            )

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
        self.draw_playground()

        while not self.game_over:
            angle, force = self._get_command()
            self.shoot(angle, force)
            self.active_player *= -1

    def shoot(self, angle: int, force: int) -> None:
        projectile_path: list[tuple[int, int]] = []
        for i, (projectile_x, projectile_y) in enumerate(
                self.tanks[self.active_player].shoot(angle, force * 10)
        ):
            x_, y_ = int(projectile_x), int(projectile_y)
            projectile_path.append((x_, self.height - y_))

            if self._check_and_hit(x_, y_):
                self.output_device.draw_path(projectile_path)
                self.output_device.draw_circle((x_, self.height - y_), BLAST_RADIUS)
                break

            if projectile_x < 0 or projectile_x > self.width or projectile_y < 0:
                self.output_device.draw_path(projectile_path)
                break

    def _check_and_hit(self, x: int, y: int) -> bool:
        for tank in self.tanks.values():
            if tank.is_hit(x, y):
                self.game_over = True
                return True

        for explosion in self.explosions:
            if explosion.is_hit(x, y):
                return False

        for building in self.buildings:
            if building.is_hit(x, y):
                self.explosions.append(Explosion(x, y, BLAST_RADIUS))
                return True

        return False

    def _get_command(self) -> tuple[int, int]:
        angle_, force_ = None, None

        while angle_ is None:
            try:
                angle, force = input(
                    f"Player {self.active_player}: Enter angle and velocity (i.e. 50 160) "
                ).split()
                angle_, force_ = int(angle), int(force)
            except ValueError:
                print("Expected two integers (e.g. 50 500)")

        return angle_, force_

    def draw_playground(self) -> None:
        self.output_device.draw_rectangle((0, 0), (self.width, self.height))

        for building in self.buildings:
            self.output_device.draw_rectangle(
                (
                    building.x_position - building.width // 2,
                    self.height - building.height,
                ),
                (building.x_position + building.width // 2, self.height),
            )

        for tank in self.tanks.values():
            self.output_device.draw_rectangle(
                (tank.x_position - 5, self.height - tank.y_position + 5),
                (tank.x_position + 5, self.height - tank.y_position - 5),
            )

    @cached_property
    def output_device(self) -> OutputDevice:
        if self.output is None:
            return ScreenPlotter(self.screen, self.width, self.height)
        elif isinstance(self.output, AxiDraw):
            return AxidrawPlotter(self.output, self.width, self.height)
        else:
            raise ValueError(f"Unknown output type {self.output}")