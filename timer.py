import pygame
from settings import *


class Timer:
    def __init__(self, time, pos):
        self.time = time
        self.pos = pos
        self.font = pygame.font.SysFont('menlottc', 18)

    def tick(self, dt):
        self.time -= dt

    def draw(self):
        mins, secs = divmod(self.time, 60)
        ms = divmod(self.time, 1000)[1]
        s = ''
        if self.time <= 10:
            s = f'{ms:.02f}'
        else:
            s = f'{int(mins):02}:{int(secs):02}'
        txt = self.font.render(s, True, GREEN)
        if self.pos == "top":
            pygame.draw.rect(SCREEN, GREY, [BOARD_X + BOARD_SIZE - TILE_SIZE, BOARD_Y - 36, TILE_SIZE, 28])
            SCREEN.blit(txt, (BOARD_X + BOARD_SIZE - TILE_SIZE + 4, BOARD_Y - 32))
        else:
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE-TILE_SIZE, BOARD_Y+BOARD_SIZE+8, TILE_SIZE, 28])
            SCREEN.blit(txt, (BOARD_X+BOARD_SIZE-TILE_SIZE+4, BOARD_Y+BOARD_SIZE+12))