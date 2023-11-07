import random
from abc import ABCMeta, abstractmethod
from functools import cached_property

import numpy as np
from pyaxidraw.axidraw import AxiDraw

from objects.building import Building
from objects.explosion import Explosion
from objects.tank import Tank
from output.axidraw_plotter import AxidrawPlotter
from output.output_device import OutputDevice
from output.screen_plotter import ScreenPlotter
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
        standard_width = 30
        # todo: create buildings

    def place_tanks(self) -> None:
        # todo: place tanks on left and right edge
        ...

    def start_game(self) -> None:
        self.create_buildings(5)
        self.place_tanks()
        self.draw_playground()

        while not self.game_over:
            angle, force = self._get_command()
            self.shoot(angle, force)
            self.active_player *= -1

    def shoot(self, angle: int, force: int) -> None:
        # todo: get shot from tank
        ...

    def _check_and_hit(self, x: int, y: int) -> bool:
        # todo: check if building or tank is hit
        # if building is hit, add explosion

        return False

    def _get_command(self) -> tuple[int, int]:
        angle_, force_ = None, None

        # todo: get input from console

        return angle_, force_

    def draw_playground(self) -> None:
        self.output_device.draw_rectangle((0, 0), (self.width, self.height))

        for building in self.buildings:
            self.output_device.draw_sprite(building.sprite)

        for tank in self.tanks.values():
            self.output_device.draw_sprite(tank.sprite)

    @cached_property
    def output_device(self) -> OutputDevice:
        if self.output is None:
            return ScreenPlotter(self.screen, self.width, self.height)
        elif isinstance(self.output, AxiDraw):
            return AxidrawPlotter(self.output, self.width, self.height)
        else:
            raise ValueError(f"Unknown output type {self.output}")
