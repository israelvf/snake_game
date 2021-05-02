import sys
import pygame
from pygame.locals import *
from random import randint


class SnakeGame:

    def __init__(self):
        pygame.display.set_caption("Snake")
        pygame.init()
        self.up_direction = 0
        self.right_direction = 1
        self.down_direction = 2
        self.left_direction = 3
        self.base_speed = 10
        self.high_score = 0
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.initial_conditions()

    def initial_conditions(self):
        self.snake = [(200, 200), (210, 200), (220, 200)]
        self.snake_skin = pygame.Surface((10, 10))
        self.snake_skin.fill((255, 255, 255))

        self.apple_pos = self.on_grid_random()
        self.apple = pygame.Surface((10, 10))
        self.apple.fill((255, 0, 0))

        self.my_direction = self.left_direction
        self.speed = self.base_speed

        self.score = 0

    def update_clock_tick(self):
        self.clock.tick(self.speed)

    def increase_snake_speed(self):
        speed_increase_factor = len(self.snake) - 3
        self.speed = self.base_speed + speed_increase_factor

    def on_grid_random(self):
        x = randint(0, 590)
        y = randint(0, 590)

        return (x//10 * 10, y//10 * 10)

    def collision(self, c1, c2, x=None, y=None):
        if x is not None:
            return (c1[0] == c2[0])
        if y is not None:
            return (c1[1] == c2[1])
        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def check_apple_collision(self):
        self.update_score()
        return self.collision(self.snake[0], self.apple_pos)

    def check_snake_body_collision(self):
        snake_head = self.snake[0]

        for i in range(len(self.snake) - 1):
            if i == 0:
                continue
            snake_body_segment = self.snake[i]
            if self.collision(snake_head, snake_body_segment):
                return True

        return False

    def check_wall_collision(self):
        up_wall_collision = self.collision(self.snake[0], (0, 0), y=True)
        down_wall_collision = self.collision(self.snake[0], (600, 600), y=True)
        right_wall_collision = self.collision(
            self.snake[0], (600, 600), x=True)
        left_wall_collision = self.collision(self.snake[0], (0, 0), x=True)

        return up_wall_collision or down_wall_collision or right_wall_collision or left_wall_collision

    def check_death(self):
        wall_collision = self.check_wall_collision()
        snake_body_collision = self.check_snake_body_collision()
        return wall_collision or snake_body_collision

    def move_snake(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = (self.snake[i-1][0], self.snake[i-1][1])
        if self.my_direction == self.up_direction:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - 10)
        if self.my_direction == self.down_direction:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + 10)
        if self.my_direction == self.right_direction:
            self.snake[0] = (self.snake[0][0] + 10, self.snake[0][1])
        if self.my_direction == self.left_direction:
            self.snake[0] = (self.snake[0][0] - 10, self.snake[0][1])

    def calculate_apple_position(self):
        self.apple_pos = self.on_grid_random()

    def grow_snake(self):
        self.snake.append((0, 0))

    def render_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.apple, self.apple_pos)
        for pos in self.snake:
            self.screen.blit(self.snake_skin, pos)

        pygame.display.update()

    def process_game_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    self.change_snake_direction(event)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def change_snake_direction(self, event):
        new_direction = self.my_direction

        if event.key == K_UP:
            new_direction = self.up_direction
        if event.key == K_DOWN:
            new_direction = self.down_direction
        if event.key == K_RIGHT:
            new_direction = self.right_direction
        if event.key == K_LEFT:
            new_direction = self.left_direction

        prohibited_direction = abs(self.my_direction - new_direction) == 2

        if not prohibited_direction:
            self.my_direction = new_direction

    def update_score(self):
        bonus_snake_length = (len(self.snake) - 3)//10 * (len(self.snake) - 3)
        self.score = (len(self.snake) - 3) + bonus_snake_length

    def run(self):
        self.increase_snake_speed()
        self.update_clock_tick()
        self.process_game_events()

        death = self.check_death()

        if death:
            self.initial_conditions()

        apple_collision = self.check_apple_collision()

        if apple_collision:
            self.calculate_apple_position()
            self.grow_snake()

        self.move_snake()

        self.render_screen()


if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game.run()
