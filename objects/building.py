from output.drawable import Drawable, Rectangle, Circle


class Building(Drawable):
    def __init__(self, x_position: int, height: int, width: int = 30) -> None:
        self.x_position = x_position
        self.height = height
        self.width = width

    def is_hit(self, x: int, y: int) -> bool:
        # todo: define hit detection
        return False

    @property
    def sprite(self) -> list[Rectangle | Circle]:
        return []  # todo: define sprite
