from pygame import Surface
from models import Apple, Snake
from game import Engine


if __name__ == "__main__":
    apple = Apple(position=(450, 450))
    snake = Snake(position=(300, 300), initial_size=3)

    game = Engine(apple=apple, snake=snake)

    while True:
        game.run()
