class Building:
    def __init__(self, x_position: int, height: int, width: int = 30) -> None:
        self.x_position = x_position
        self.height = height
        self.width = width

        self.hits = []

    def is_hit(self, x: int, y: int) -> bool:
        if self.x_position - self.width // 2 <= x <= self.x_position + self.width // 2 and self.height > y:
            return True

        return False
