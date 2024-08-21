import pygame
import random
from collections import deque
from enum import Enum


"""
Game functionality

Snake Game
---------------
* The goal of the game is to get the longest snake.
** The snake gets longer with each food the snake eats.
* The player can move the snake with arrow keys 
* The player loses if:
** Hits the edge of the board
** Bites own body
* Scored by # of food eaten
* Every time food is eaten, a new one is created. (Does it avoid snake?)
* Eat:
** If food coordinate overlaps snake 
"""

class Coordinate():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Direction(Enum):
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3


class Game:
    # Add any game variables here
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BG_COLOR = pygame.Color('Light Slate Gray')
    BOARD_COLOR = pygame.Color('chartreuse2')
    SNAKE_COLOR = pygame.Color('darkgreen')
    FOOD_COLOR = pygame.Color('red')

    MOVE_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        self.screen = None
        self.running = False
        self.init_screen()
        
        self.grid_height = 20
        self.grid_length = 30
        self.scale = 25
        # List of coordinate tuples
        self.snake = deque()
        self.snake.append(Coordinate(self.grid_length / 2, self.grid_height / 2))
        self.snake_direction = Direction.RIGHT
        self.food_location = self.get_random_food()
        self.move_timer = 50 # ms
        pygame.time.set_timer(self.MOVE_EVENT, self.move_timer)
    
    def init_screen(self):
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def get_random_food(self):
        x = random.randint(0, self.grid_length - 1)
        y = random.randint(0, self.grid_height - 1)

        return Coordinate(x, y)
    
    def draw_board(self):
        board = pygame.Surface((self.scale * self.grid_length, self.scale * self.grid_height))
        board.fill(self.BOARD_COLOR)

        board_center = (
            (self.WINDOW_WIDTH - board.get_width()) / 2,
            (self.WINDOW_HEIGHT - board.get_height()) / 2
        )
        self.screen.blit(board, board_center)

    def draw_snake(self):
        for snake_tile in self.snake:
            surf = pygame.Surface((self.scale,self.scale))
            surf.fill(self.SNAKE_COLOR)

            x = self.scale * snake_tile.x
            y = self.scale * snake_tile.y

            x += (self.WINDOW_WIDTH - (self.grid_length * self.scale)) / 2
            y += (self.WINDOW_HEIGHT - (self.grid_height * self.scale)) / 2
            self.screen.blit(surf, (x, y))

    def draw_food(self):
        x = (0.5 + self.food_location.x) * self.scale
        y = (0.5 + self.food_location.y) * self.scale
        x += (self.WINDOW_WIDTH - (self.grid_length * self.scale)) / 2
        y += (self.WINDOW_HEIGHT - (self.grid_height * self.scale)) / 2
        pygame.draw.circle(self.screen, self.FOOD_COLOR, (x, y), 8)


    def draw_all(self):
        self.screen.fill(self.BG_COLOR)

        self.draw_board()
        self.draw_snake()
        self.draw_food()
        pygame.display.flip()



    def collision(self):
        head = self.snake[0]


        if head.x >= self.grid_length or head.x < 0 \
            or head.y >= self.grid_height or head.y < 0:
            print(f"Collided: {head.x}, {head.y}")

            return True

    def move_snake(self):
        head = self.snake[0]
        rear = self.snake.pop()

        dir = self.snake_direction
        if dir == Direction.RIGHT:
            rear.x = head.x + 1
            rear.y = head.y
        elif dir == Direction.LEFT:
            rear.x = head.x - 1
            rear.y = head.y
        elif dir == Direction.DOWN:
            rear.x = head.x
            rear.y = head.y + 1
        elif dir == Direction.UP:
            rear.x = head.x
            rear.y = head.y - 1
        self.snake.appendleft(rear)

    def process_events(self):
        if self.collision():
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == self.MOVE_EVENT:
                self.move_snake()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.snake_direction = Direction.DOWN
                   # self.move_snake()
                elif event.key == pygame.K_UP:
                    self.snake_direction = Direction.UP
                    #self.move_snake()
                elif event.key == pygame.K_RIGHT:
                    self.snake_direction = Direction.RIGHT
                    #self.move_snake()
                elif event.key == pygame.K_LEFT:
                    self.snake_direction = Direction.LEFT
                    #self.move_snake()

    def check_food(self):
        found = False
        for s in self.snake:
            if s.x == self.food_location.x and s.y == self.food_location.y:
                found = True
                break
        if found:
            self.food_location = self.get_random_food()
            tail = self.snake[-1]
            self.snake.append(Coordinate(tail.x, tail.y))


    
    def start_main_loop(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(30)

            self.process_events()
            self.check_food()
            self.draw_all()


def run():
    pygame.init()
    pygame.display.set_caption("Duk's Snake Game")
    game = Game()
    game.start_main_loop()

