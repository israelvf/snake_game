from dataclasses import dataclass
from pygame import Surface


@dataclass
class Apple:
    position: tuple
    skin: Surface = Surface((10, 10))
    color: tuple = (255, 0, 0)

    def __post_init__(self):
        self.skin.fill(self.color)
