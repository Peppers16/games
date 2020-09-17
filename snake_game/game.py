import pygame as pg
import sys
from numpy import array
from collections import deque

pg.init()

snake_color = (255, 0, 0)
bg_color = (0, 0, 0)
deadzone_color = (0, 255, 0)

screen_width = 500
cell_width = 5

screen = pg.display.set_mode((screen_width, screen_width))
clock = pg.time.Clock()


class Cell:
    def __init__(self, rect: pg.Rect, is_deadzone=False, draw_color=bg_color):
        self.contains_snake = False
        self.contains_food = False
        self.is_deadzone = is_deadzone
        self.draw_color = draw_color
        self.rect = rect

    def draw(self):
        screen.fill(self.draw_color, self.rect)


class Grid:
    def __init__(self):
        self.grid = []
        self.grid_width = screen_width // cell_width
        for r in range(self.grid_width):
            row = []
            for c in range(self.grid_width):
                if r in [0, self.grid_width - 1] or c in [0, self.grid_width - 1]:
                    deadzone = True
                    color = deadzone_color
                else:
                    deadzone = False
                    color = bg_color
                row.append(
                    Cell(
                        rect=pg.Rect(c*cell_width, r*cell_width, cell_width, cell_width)
                        , is_deadzone=deadzone
                        , draw_color=color
                    ))
            self.grid.append(row)
        self._draw_screen()

    def _draw_screen(self):
        for cell in self:
            cell.draw()

    def __getitem__(self, item):
        return self.grid[item]

    def __iter__(self):
        return (c for r in self.grid for c in r)


class Player:
    def __init__(self, rect: pg.Rect):
        self.rect = rect
        self._direction = array([0, 0])
        self.key_dir_map = {
            pg.K_UP: array([0, -1])
            , pg.K_DOWN: array([0, 1])
            , pg.K_RIGHT: array([1, 0])
            , pg.K_LEFT: array([-1, 0])
        }

    def receive_key(self, key):
        if key in self.key_dir_map:
            new_dir = self.key_dir_map[key]
            if any(new_dir + self._direction):  # ignore direct reversal
                self._direction = new_dir

    def move(self):
        velocity = self._direction * cell_width
        self.rect = self.rect.move(tuple(velocity))


player = Player(pg.Rect(screen_width / 2, screen_width / 2, cell_width, cell_width))
grid = Grid()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            else:
                player.receive_key(event.key)
    screen.fill(bg_color, player.rect)
    player.move()
    screen.fill(snake_color, player.rect)
    pg.display.update()
    clock.tick(30)
