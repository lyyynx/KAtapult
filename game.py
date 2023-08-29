import random
from abc import ABCMeta, abstractmethod

from building import Building
from explosion import Explosion
from tank import Tank


class TankGame(metaclass=ABCMeta):
    def __init__(self, width: int, height: int) -> None:
        self.height = height
        self.width = width

        self.buildings: list[Building] = []
        self.tanks: list[Tank] = []
        self.explosions: list[Explosion] = []

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
    def __init__(self) -> None:
        super().__init__(300, 50)

        self.active_player = 1

    def create_buildings(self, number_of_buildings: int) -> None:
        for _ in range(number_of_buildings):
            self.buildings.append(
                Building(random.randint(0, self.width), random.randint(10, self.height))
            )

    def place_tanks(self) -> None:
        buildings_on_left = [
            building.height
            for building in self.buildings
            if building.x_position - building.width < 10
        ]
        max_left_height = max(buildings_on_left) if len(buildings_on_left) > 0 else 0
        self.tanks.append(Tank(5, max_left_height))

        buildings_on_right = [
            building.height
            for building in self.buildings
            if building.x_position + building.width > self.width - 10
        ]
        max_right_height = max(buildings_on_right) if len(buildings_on_right) > 0 else 0
        self.tanks.append(Tank(self.width - 5, max_right_height))

    def start_game(self) -> None:
        self.create_buildings(3)
        self.place_tanks()

        while not self._check_hit():
            angle, force = self._get_command()
            self.tanks[(self.active_player + 1) // 2].shoot(angle, force)
            self.active_player *= -1

    def _check_hit(self) -> bool:
        for tank in self.tanks:
            if tank.hit:
                return True

        return False

    def _get_command(self) -> tuple[int, int]:
        angle, force = input(f"Player {self.active_player}: Enter angle and force (i.e. 50 160) ").split()
        return angle, force
