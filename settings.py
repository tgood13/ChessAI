import pygame

# Screen components
TILE_SIZE = 64
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = TILE_SIZE * 8
BOARD_X = 8
BOARD_X = (SCREEN_WIDTH-BOARD_SIZE)//2
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (TILE_SIZE, TILE_SIZE)

# Basic Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
LIGHT_BLUE = (51, 153, 255)
BROWN = (71, 40, 11)
BEIGE = (232, 216, 152)
GREEN = (20, 148, 20)
RED = (255, 0, 0)

# Game Colors
A = (230, 57, 70)
B = (255, 230, 167)
C = (67, 40, 24)
D = (158, 42, 43)
E = (84, 11, 14)

SMALL_TEXT_COLOR = (241, 250, 238)
LARGE_TEXT_COLOR = (230, 57, 70)

BG_COLOR = (29, 53, 87)
BG_COLOR_LIGHT = (70, 70, 70)

ICE_TILE_LIGHT = 241, 250, 238
ICE_TILE_DARK = 69, 123, 157
TILE_COLOR_LIGHT = 255, 230, 167
TILE_COLOR_DARK = 67, 40, 24

TILE_COLOR_LIGHT = ICE_TILE_LIGHT
TILE_COLOR_DARK = ICE_TILE_DARK

# Create screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Converts 8x8 grid locations to pixel coordinates
def to_coords(x, y):
    return BOARD_X + x * TILE_SIZE, BOARD_Y + y * TILE_SIZE
