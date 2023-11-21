from output.drawable import Drawable, Rectangle, Circle


class Building(Drawable):
    def __init__(self, x_position: int, height: int, width: int = 30, health: int = 2) -> None:
        self.x_position = x_position
        self.height = height
        self.width = width
        self.health = health

    def is_hit(self, x: int, y: int) -> bool:
        if self.health == 0:
            return False

        if (
            self.x_position - self.width // 2 <= x <= self.x_position + self.width // 2
            and self.height > y
        ):
            self.demolish()
            return True

        return False

    @property
    def sprite(self) -> list[Rectangle | Circle]:
        return [
            Rectangle(
                top_left=(self.x_position - self.width // 2, self.height),
                bottom_right=(self.x_position + self.width // 2, 0),
            )
        ]

    def demolish(self):
        self.health -= 1

