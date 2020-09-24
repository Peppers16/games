import pygame as pg
import sys
from numpy import array
from collections import deque
from random import shuffle

pg.init()

snake_color = (0, 255, 0)
bg_color = (0, 0, 0)
deadzone_color = (255, 0, 0)
food_color = (0, 0, 255)

screen_width = 500
block_width = 10
screen = pg.display.set_mode((screen_width, screen_width))
clock = pg.time.Clock()


class Snake:
    def __init__(self, start_len: int = 3):
        mid = screen_width // 2
        start_head = pg.Rect(mid, mid, block_width, block_width)
        self.body = deque([start_head])
        self.alive = True
        self.in_motion = False
        self.body_len = start_len
        self.board = Board(self)
        self._direction = array([0, 0])
        self.key_dir_map = {
            pg.K_UP: array([0, -1])
            , pg.K_DOWN: array([0, 1])
            , pg.K_RIGHT: array([1, 0])
            , pg.K_LEFT: array([-1, 0])
        }

    def receive_key(self, key):
        if key in self.key_dir_map:
            new_dir = self.key_dir_map[key]*block_width
            if any(new_dir + self._direction):  # ignore direct reversal
                self._direction = new_dir
                self.in_motion = True

    def move(self):
        if self.in_motion:
            new_head = self.head.move(self._direction)
            new_head.x = new_head.x % screen_width
            new_head.y = new_head.y % screen_width
            self.body.append(new_head)
        if self.board.try_eating(self.head):
            print('yum')
            self.body_len += 1
            print(len(self.body))
        # TODO: Currently snake ignores food which it eats whilst it is growing to start_len
        elif len(self.body) > self.body_len:
            old_tail = self.body.popleft()
            screen.fill(bg_color, old_tail)
        screen.fill(snake_color, self.head)  # fill new cell with snake color
        if self.collides_with(self.head):
            self.alive = False

    def collides_with(self, rect: pg.Rect):
        i = rect.collidelist(self.body)
        if -1 < i < len(self.body) - 1:
            return True
        return False

    @property
    def head(self):
        return self.body[-1]


class Board:
    def __init__(self, snake: Snake):
        self.snake = snake
        self.food = []
        n_blocks = screen_width // block_width
        self.grid = [(i, j) for j in range(n_blocks) for i in range(n_blocks)]
        self.place_food()

    def place_food(self):
        """
        Place food at a random location on the grid. Method shuffles the grid and iterates through it until it finds an
        unoccupied location: this will help in late game when there are few available locations.
        :return:
        """
        shuffle(self.grid)
        for i, j in self.grid:
            try_rect = pg.Rect(i*block_width, j*block_width, block_width, block_width)
            if self.snake.collides_with(try_rect):
                continue
            else:
                self.food.append(try_rect)
                screen.fill(food_color, try_rect)
                return

    def try_eating(self, rect: pg.Rect):
        """
        Given a Rect, eat food if present and return True. Otherwise, return False.
        :param rect:
        :return:
        """
        i = rect.collidelist(self.food)
        if -1 < i:
            self.food.pop(i)
            self.place_food()
            return True
        return False


snake = Snake()
pg.event.set_blocked(pg.MOUSEMOTION)

# this loop is designed to avoid 'ignoring' player directions if two are given in one game cycle.
while snake.alive:
    event = pg.event.poll()  # check one event, leave other events on the queue
    while event.type != pg.NOEVENT:
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            else:
                snake.receive_key(event.key)
                break  # advance game cycle before polling event queue further
        event = pg.event.poll()  # keep polling event queue until empty or player directs snake
    snake.move()
    pg.display.update()
    clock.tick(30)
