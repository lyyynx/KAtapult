from output.drawable import Drawable, Rectangle, Circle
from utils.constants import BLAST_RADIUS


class Explosion(Drawable):
    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    def is_hit(self, x: int, y: int) -> bool:
        if (x - self.x) ** 2 + (y - self.y) ** 2 < BLAST_RADIUS**2:
            return True

        return False

    @property
    def sprite(self) -> list[Rectangle | Circle]:
        return [Circle(center=(self.x, self.y), radius=BLAST_RADIUS)]
