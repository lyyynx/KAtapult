from abc import ABCMeta, abstractmethod


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
