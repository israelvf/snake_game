from dataclasses import dataclass, field
from pygame import Surface


@dataclass
class Snake:
    position: tuple[int, int]
    initial_size: int
    skin: Surface = Surface((10, 10))
    color: tuple[int, int, int] = (255, 255, 255)
    body: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.skin.fill(self.color)

    def create_body(self, segment_size: int) -> None:
        self.body = list()

        for segment in range(0, self.initial_size):
            x = self.position[0] + segment * segment_size
            y = self.position[1]
            self.body.append((x, y))

    def grow(self) -> None:
        self.body.append(self.body[-1])

    def move(self, vector: tuple) -> None:
        if vector == (0, 0):
            return

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i-1][0], self.body[i-1][1])

        new_x, new_y = map(sum, zip(self.body[0], vector))
        self.body[0] = (new_x, new_y)
        self.position = self.body[0]
