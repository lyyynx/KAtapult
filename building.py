class Building:
    def __init__(self, x_position: int, height: int) -> None:
        self.x_position = x_position
        self.height = height

        self.width = 30

    def draw(self) -> None:
        ...