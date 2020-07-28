# settings.py

import pygame

TILE_SIZE = 64

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BOARD_SIZE = TILE_SIZE * 8

BOARD_X = int((SCREEN_WIDTH / 2) - (BOARD_SIZE / 2))
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))

BOARD_X = 8
#BOARD_X = 32

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [50, 50, 50]
LIGHT_BLUE = [51, 153, 255]

BROWN = [71, 40, 11]
BEIGE = [232, 216, 152]
GREEN = [20, 148, 20]
RED = [255, 0, 0]

#FONT = pygame.font.SysFont('menlottc', 18)


# Create screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def to_coords(x, y):
    return BOARD_X + x * 64, BOARD_Y + y * 64
