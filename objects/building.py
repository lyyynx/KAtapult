from output.drawable import Drawable, Rectangle, Circle


class Building(Drawable):
    def __init__(self, x_position: int, height: int, width: int = 30) -> None:
        self.x_position = x_position
        self.height = height
        self.width = width

    def is_hit(self, x: int, y: int) -> bool:
        if (
            self.x_position - self.width // 2 <= x <= self.x_position + self.width // 2
            and self.height > y
        ):
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
