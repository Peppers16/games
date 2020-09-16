import pygame as pg
import sys

pg.init()

red = (255, 0, 0)
black = (0, 0, 0)
screensize = (640, 480)

screen = pg.display.set_mode(screensize)
clock = pg.time.Clock()


class Player:
    def __init__(self, rect: pg.Rect):
        self.rect = rect
        self._direction = (0, 0)

    def dir_up(self):
        self._direction = (0, -1)

    def dir_down(self):
        self._direction = (0, 1)

    def dir_right(self):
        self._direction = (1, 0)

    def dir_left(self):
        self._direction = (-1, 0)

    def move(self):
        self.rect = self.rect.move(self._direction)


player = Player(pg.Rect(320, 200, 5, 5))  # this Rect object stores info about the area the player occupies


def keypress_response(key: pg.key):
    if key == pg.K_ESCAPE:
        sys.exit()
    elif key == pg.K_UP:
        player.dir_up()
    elif key == pg.K_DOWN:
        player.dir_down()
    elif key == pg.K_LEFT:
        player.dir_left()
    elif key == pg.K_RIGHT:
        player.dir_right()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            keypress_response(event.key)
    screen.fill(black, player.rect)
    player.move()
    screen.fill(red, player.rect)
    pg.display.update()
    clock.tick(120)
