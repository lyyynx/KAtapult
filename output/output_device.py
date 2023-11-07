from abc import ABCMeta, abstractmethod

from output.drawable import Rectangle, Circle


class OutputDevice(metaclass=ABCMeta):
    @abstractmethod
    def draw_rectangle(
        self, top_left: tuple[int, int], bottom_right: tuple[int, int]
    ) -> None:
        ...

    @abstractmethod
    def draw_circle(self, center: tuple[int, int], radius: int) -> None:
        ...

    @abstractmethod
    def draw_path(self, path: list[tuple[int, int]]) -> None:
        ...

    def draw_sprite(self, sprite: list[Rectangle | Circle]) -> None:
        for shape in sprite:
            if isinstance(shape, Rectangle):
                self.draw_rectangle(shape.top_left, shape.bottom_right)
            elif isinstance(shape, Circle):
                self.draw_circle(shape.center, shape.radius)
            else:
                raise ValueError(f"Unknown shape {shape}")
