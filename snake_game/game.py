import pygame
import sys

pygame.init()

red = (255, 0, 0)
black = (0, 0, 0)

screensize = (640, 480)

screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()

player = pygame.Rect(320, 200, 5, 5)  # this Rect object stores info about the area the player occupies
pygame.time.delay(500)

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()
        screen.fill(black, player)
        player = player.move(1, 0)
        screen.fill(red, player)
        pygame.display.update()
        clock.tick(60)
