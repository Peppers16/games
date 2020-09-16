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
        self.key_dir_map = {
            pg.K_UP: (0, -1)
            , pg.K_DOWN: (0, 1)
            , pg.K_RIGHT: (1, 0)
            , pg.K_LEFT: (-1, 0)
        }

    def receive_key(self, key):
        if key in self.key_dir_map:
            self._direction = self.key_dir_map[key]

    def move(self):
        self.rect = self.rect.move(self._direction)


player = Player(pg.Rect(320, 200, 5, 5))  # this Rect object stores info about the area the player occupies


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
    clock.tick(120)
