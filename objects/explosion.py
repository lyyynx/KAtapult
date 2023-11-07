from output.drawable import Drawable, Rectangle, Circle
from utils.constants import BLAST_RADIUS


class Explosion(Drawable):
    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    def is_hit(self, x: int, y: int) -> bool:
        # todo: define hit detection

        return False

    @property
    def sprite(self) -> list[Rectangle | Circle]:
        return []  # todo: define sprite
