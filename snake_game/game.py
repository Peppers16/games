import pygame as pg
import sys
from numpy import array

pg.init()

red = (255, 0, 0)
black = (0, 0, 0)
screen_width = 500
cell_width = 5

screen = pg.display.set_mode((screen_width, screen_width))
clock = pg.time.Clock()


class Player:
    def __init__(self, rect: pg.Rect):
        self.rect = rect
        self._direction = array([0, 0])
        self.speed = 1
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
        velocity = self._direction * self.speed * cell_width
        self.rect = self.rect.move(tuple(velocity))


player = Player(pg.Rect(screen_width/2, screen_width/2, cell_width, cell_width))  # this Rect object stores info about the area the player occupies


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            else:
                player.receive_key(event.key)

    screen.fill(black, player.rect)
    player.move()
    screen.fill(red, player.rect)
    pg.display.update()
    clock.tick(30)
