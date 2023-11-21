import random
from abc import ABCMeta, abstractmethod
from functools import cached_property

import numpy as np
# from pyaxidraw.axidraw import AxiDraw

from objects.building import Building
from objects.explosion import Explosion
from objects.tank import Tank
# from output.axidraw_plotter import AxidrawPlotter
from output.output_device import OutputDevice
from output.screen_plotter import ScreenPlotter
from utils.constants import BLAST_RADIUS


class TankGame(metaclass=ABCMeta):
    def __init__(self, width: int, height: int) -> None:
        self.window_height = height
        self.window_width = width

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
    def __init__(self, output: None = None) -> None:
        super().__init__(640, 360)
        self.output = output

        self.active_player = 1

    def create_buildings(self, number_of_buildings: int) -> None:
        standard_width = 30
        x_padding = 10 + standard_width
        possible_x_positions = np.arange(standard_width // 2, self.window_width - standard_width // 2)
        for _ in range(number_of_buildings):
            building_x = random.choice(possible_x_positions)

            # remove x positions of the building including x padding
            possible_x_positions = np.setdiff1d(
                possible_x_positions,
                np.arange(building_x - standard_width // 2 - x_padding, building_x + standard_width // 2 + x_padding),
            )

            distance_to_edge = min(building_x, self.window_width - building_x)
            height_multiplier = max((distance_to_edge / (self.window_width / 2)), 0.3)

            self.buildings.append(
                Building(building_x, int(random.randint(standard_width, self.window_height) * height_multiplier))
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
            if building.x_position + building.width // 2 > self.window_width - 5
        ]
        max_right_height = max(buildings_on_right) if len(buildings_on_right) > 0 else 0
        self.tanks[-1] = Tank(self.window_width - 5, max_right_height)

    def start_game(self) -> None:
        self.create_buildings(5)
        self.place_tanks()
        self.draw_playground()

        while not self.game_over:
            angle, force = self._get_command()
            self.shoot(angle, force)
            self.active_player *= -1

    def shoot(self, angle: int, force: int) -> None:
        projectile_path: list[tuple[int, int]] = []
        for (projectile_x, projectile_y) in self.tanks[self.active_player].shoot(angle, force * 10):
            x, y = int(projectile_x), int(projectile_y)
            previous_x, previous_y = projectile_path[-1] if len(projectile_path) > 0 else (self.tanks[self.active_player].x_position, self.tanks[self.active_player].y_position)
            projectile_path.append((x, y))

            y_difference = ((x - previous_x)**2 + (y - previous_y)**2)
            velocity = (y_difference * (force / 1000))**0.5

            if self._check_and_hit(x, y):
                self.output_device.draw_path(projectile_path)
                explosion = Explosion(x, y, int(BLAST_RADIUS * velocity))
                self.explosions.append(explosion)
                self.output_device.draw_sprite(explosion.sprite)
                break

            if projectile_x < 0 or projectile_x >= self.window_width or projectile_y < 0:
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
        self.output_device.draw_rectangle((0, 0), (self.window_width, self.window_height))

        for building in self.buildings:
            self.output_device.draw_sprite(building.sprite)

        for tank in self.tanks.values():
            self.output_device.draw_sprite(tank.sprite)

    @cached_property
    def output_device(self) -> OutputDevice:
        if self.output is None:
            return ScreenPlotter(self.screen, self.window_width, self.window_height)
        # elif isinstance(self.output, AxiDraw):
        #     return AxidrawPlotter(self.output, self.width, self.height)
        else:
            raise ValueError(f"Unknown output type {self.output}")
