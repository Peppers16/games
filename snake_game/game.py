import pygame as pg
import sys
from numpy import array
from collections import deque
from random import choice

pg.init()

snake_color = (0, 255, 0)
bg_color = (0, 0, 0)
deadzone_color = (255, 0, 0)
food_color = (0, 0, 255)

screen_width = 600
cell_width = 10

screen = pg.display.set_mode((screen_width, screen_width))
clock = pg.time.Clock()


class Cell:
    def __init__(self, vector: array, is_deadzone=False, draw_color=bg_color):
        """
        a cell in the Grid. A cell can draw itself on the screen.

        :param vector: The location of the cell in the matrix representation of the grid [row, column] where [0,0]
            is top left and [0, n] is top right.
        :param is_deadzone: Is the cell a deadzone cell?
        :param draw_color: RGB tuple that the cell should draw itself with.
        """
        self.contains_snake = False
        self.contains_food = False
        self.is_deadzone = is_deadzone
        self.draw_color = draw_color
        # Note, screen coordinates are (x, y), so we take (column, row) from the vector.
        self.rect = pg.Rect(vector[1]*cell_width, vector[0]*cell_width, cell_width, cell_width)
        self.vector = vector

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
                        vector=array([r, c])
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

    def place_food(self):
        food_cell = choice([cell for cell in grid if not cell.is_deadzone and not cell.contains_snake])
        food_cell.contains_food = True
        screen.fill(food_color, food_cell.rect)


class Snake:
    def __init__(self, grid: Grid, start_len=20):
        self.grid = grid
        self.start_len = start_len
        # find initial cell in grid
        mid_ix = grid.grid_width // 2
        start_cell = grid[mid_ix][mid_ix]
        start_cell.contains_snake = True
        self.body = deque([start_cell])
        self.alive = True
        self.in_motion = False

        self._direction = array([0, 0])
        self.key_dir_map = {
            pg.K_UP: array([-1, 0])
            , pg.K_DOWN: array([1, 0])
            , pg.K_RIGHT: array([0, 1])
            , pg.K_LEFT: array([0, -1])
        }

    def receive_key(self, key):
        if key in self.key_dir_map:
            new_dir = self.key_dir_map[key]
            if any(new_dir + self._direction):  # ignore direct reversal
                self._direction = new_dir
                self.in_motion = True

    def move(self):
        if self.in_motion:
            # determine next cell in grid based on direction
            new_r, new_c = self.head.vector + self._direction
            new_r, new_c = new_r % self.grid.grid_width, new_c % self.grid.grid_width  # wrap screen if travelling off-grid
            new_cell = self.grid[new_r][new_c]
            if new_cell.contains_snake:
                if new_cell != self.body[0] and len(self.body) >= self.start_len:  # tail is exempt: it's about to leave this cell
                    self.alive = False
            if new_cell.is_deadzone:
                self.alive = False
            elif new_cell.contains_food:
                self.eat_food(new_cell)
            elif len(self.body) >= self.start_len and not new_cell.contains_food:
                old_tail = self.body.popleft()
                old_tail.contains_snake = False
                old_tail.draw()  # pop former tail cell from body and restore its former color
            self.body.append(new_cell)
            new_cell.contains_snake = True
        screen.fill(snake_color, self.head.rect)  # fill new cell with snake color
        # print("snake length:", len(self.body))

    def eat_food(self, food_cell: Cell):
        food_cell.contains_food = False
        self.grid.place_food()

    @property
    def head(self):
        return self.body[-1]


grid = Grid()
snake = Snake(grid)
grid.place_food()
pg.event.set_blocked(pg.MOUSEMOTION)  # else waving the mouse can make the snake lag by filling event queue

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
