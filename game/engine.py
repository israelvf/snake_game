import sys
import pygame
from pygame.locals import *
from random import randint
from dataclasses import dataclass, field
from operator import add
from models import Apple, Snake


@dataclass
class Engine:
    apple: Apple
    snake: Snake
    apple_initial_position: tuple = field(init=False)
    snake_initial_position: tuple = field(init=False)
    screen_size: tuple = (600, 600)
    grid_size: int = 10
    base_speed: int = 10
    score: int = 0
    high_score: int = 0
    death_count: int = 0

    def __post_init__(self) -> None:
        self.apple_initial_position = self.apple.position
        self.snake_initial_position = self.snake.position
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake")
        pygame.init()
        self.initial_conditions()

    def initial_conditions(self) -> None:
        if self.death_count:
            pygame.time.delay(5000)

        self.direction_vector = (-self.base_speed, 0)
        self.speed = self.base_speed
        self.score = 0
        self.apple.position = self.apple_initial_position
        self.snake.position = self.snake_initial_position
        self.snake.create_body(self.grid_size)

    def get_random_position(self) -> tuple[int, int]:
        x = randint(0, self.screen_size[0] - self.grid_size)
        y = randint(0, self.screen_size[1] - self.grid_size)

        return (x//self.grid_size * self.grid_size, y//self.grid_size * self.grid_size)

    def collision(self, c1, c2) -> bool:
        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def check_apple_collision(self) -> bool:
        return self.collision(self.snake.position, self.apple.position)

    def check_snake_body_collision(self) -> bool:
        snake_head = self.snake.position

        for i in range(len(self.snake.body) - 1):
            if i == 0:
                continue
            snake_body_segment = self.snake.body[i]
            if self.collision(snake_head, snake_body_segment):
                return True

        return False

    def check_wall_collision(self) -> bool:
        up_wall_collision = self.snake.position[1] < 0
        down_wall_collision = self.snake.position[1] >= self.screen_size[1]
        right_wall_collision = self.snake.position[0] >= self.screen_size[0]
        left_wall_collision = self.snake.position[0] < 0

        return up_wall_collision or down_wall_collision or right_wall_collision or left_wall_collision

    def check_death(self) -> bool:
        wall_collision = self.check_wall_collision()
        snake_body_collision = self.check_snake_body_collision()
        return wall_collision or snake_body_collision

    def calculate_apple_position(self) -> None:
        self.apple.position = self.get_random_position()

    def render_screen(self) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.apple.skin, self.apple.position)
        for pos in self.snake.body:
            self.screen.blit(self.snake.skin, pos)

        pygame.display.update()

    def process_game_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    if not self.direction_lock:
                        self.update_direction_vector(event)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update_direction_vector(self, event) -> None:
        self.direction_lock = True

        v = self.grid_size
        new_direction = (-v, 0)

        if event.key == K_UP:
            new_direction = (0, -v)
        if event.key == K_DOWN:
            new_direction = (0, v)
        if event.key == K_RIGHT:
            new_direction = (v, 0)
        if event.key == K_LEFT:
            new_direction = (-v, 0)

        change_x, change_y = map(
            add, self.direction_vector, new_direction)

        prohibited_direction = (change_x, change_y) == (0, 0)

        if not prohibited_direction:
            self.direction_vector = new_direction

    def update_score(self) -> None:
        current_size = len(self.snake.body)
        initial_size = self.snake.initial_size
        bonus_snake_length = (current_size - initial_size)//10 * \
            (current_size - initial_size)
        self.score = (current_size - initial_size) + bonus_snake_length

    def run(self) -> None:
        self.direction_lock = False
        self.clock.tick(20)
        self.process_game_events()

        death = self.check_death()

        if death:
            self.death_count += 1
            self.initial_conditions()

        apple_collision = self.check_apple_collision()

        if apple_collision:
            self.calculate_apple_position()
            self.snake.grow()
            self.update_score()

        self.snake.move(self.direction_vector)

        self.render_screen()
