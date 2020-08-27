import pygame

# Screen components
TILE_SIZE = 64
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = TILE_SIZE * 8
BOARD_X = 8
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (64, 64)

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [50, 50, 50]
LIGHT_BLUE = [51, 153, 255]
BROWN = [71, 40, 11]
BEIGE = [232, 216, 152]
GREEN = [20, 148, 20]
RED = [255, 0, 0]

# Create screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Converts grid locations to pixel coordinates
def to_coords(x, y):
    return BOARD_X + x * TILE_SIZE, BOARD_Y + y * TILE_SIZE
