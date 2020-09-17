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


class Player:
    def __init__(self, grid: Grid):
        self.grid = grid
        mid_ix = grid.grid_width // 2
        self.cell = grid[mid_ix][mid_ix]
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

    def move(self):
        new_r, new_c = self.cell.vector + self._direction
        new_r, new_c = new_r % self.grid.grid_width, new_c % self.grid.grid_width  # wrap screen if travelling off grid
        new_cell = self.grid[new_r][new_c]
        self.cell.draw()  # restore old cell to its former color
        self.cell = new_cell
        screen.fill(snake_color, self.cell.rect)  # fill new cell with snake color


grid = Grid()
player = Player(grid)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            else:
                player.receive_key(event.key)
    player.move()
    pg.display.update()
    clock.tick(30)
