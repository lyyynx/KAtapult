from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class Circle:
    center: tuple[int, int]
    radius: int


@dataclass
class Rectangle:
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]


class Drawable:
    @property
    @abstractmethod
    def sprite(self) -> list[Rectangle | Circle]:
        ...
