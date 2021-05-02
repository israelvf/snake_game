from pygame import Surface
from models import Apple, Snake
from game import Engine


if __name__ == "__main__":
    apple = Apple(position=(250, 250))
    snake = Snake(position=(200, 200), initial_size=3)

    game = Engine(apple=apple, snake=snake)

    while True:
        game.run()
