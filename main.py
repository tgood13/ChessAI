import pygame
import piece
from settings import *
from board import *
from timer import Timer

import datetime

import pygame_menu

pygame.init()

# Title and Icon
pygame.display.set_caption("Chess")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Game:

    def __init__(self):
        self.board = Board()
        self.board.initialize_tiles()
        self.board.reset_pieces()
        #self.menu_screen()
        self.start_game()

    def menu_screen(self):
        t1 = Timer(600, "top")
        t2 = Timer(600, "bot")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            SCREEN.fill(BLACK)

            # draw top name
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y - 36, TILE_SIZE*2, 28])
            p1name = pygame.font.SysFont('menlottc', 18).render("???", True, GREEN)
            SCREEN.blit(p1name, (BOARD_X+4, BOARD_Y - 32))

            # draw top captured pieces
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y - 36, TILE_SIZE*5-16, 28])
            # count number of pieces of a type in player.captured_pieces --> [pawn-img] x 0

            # draw top ready button
            # if p1.ready
            pygame.draw.rect(SCREEN, GREEN, [BOARD_X+BOARD_SIZE+8, BOARD_Y-8-28, TILE_SIZE*4+8, 28])
            txt = pygame.font.SysFont('menlottc', 18).render("READY", True, BLACK)
            # else
            #pygame.draw.rect(SCREEN, RED, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*4+8, 28])
            #txt = pygame.font.SysFont('menlottc', 18).render("NOT READY", True, BLACK)
            SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.6), BOARD_Y-4-28))

            # draw bottom name
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*2, 28])
            p2name = pygame.font.SysFont('menlottc', 18).render("Troy", True, GREEN)
            SCREEN.blit(p2name, (BOARD_X+4, BOARD_Y+BOARD_SIZE+12))

            # draw bottom captured pieces
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*5-16, 28])

            # draw bottom READY button
            pygame.draw.rect(SCREEN, RED, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*4+8, 28])
            txt = pygame.font.SysFont('menlottc', 18).render("NOT READY", True, BLACK)
            SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.8), BOARD_Y+BOARD_SIZE+12))

            # draw clocks
            t1.draw()
            t2.draw()

            # draw settings area
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            self.board.update()
            pygame.display.flip()
        pygame.quit()

    def set_difficulty(self, value, difficulty):
        pass

    def start_game(self):

        # Game Loop
        clock = pygame.time.Clock()
        playing = True

        t1 = Timer(600, "top")
        t2 = Timer(600, "bot")
        dt = 0

        while playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.select()

            SCREEN.fill(BLACK)

            if self.board.human == WHITE:
                t2.tick(dt)
            else:
                t1.tick(dt)

            t1.draw()
            t2.draw()

            # draw top name
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y - 36, TILE_SIZE*2, 28])
            p1name = pygame.font.SysFont('menlottc', 18).render("Opponent", True, GREEN)
            SCREEN.blit(p1name, (BOARD_X+4, BOARD_Y - 32))

            # draw top captured pieces
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y - 36, TILE_SIZE*5-16, 28])
            # count number of pieces of a type in player.captured_pieces --> [pawn-img] x 0

            # draw bottom name
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*2, 28])
            p2name = pygame.font.SysFont('menlottc', 18).render("Troy", True, GREEN)
            SCREEN.blit(p2name, (BOARD_X+4, BOARD_Y+BOARD_SIZE+12))

            # draw bottom captured pieces
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*5-16, 28])

            # draw clocks
            t1.draw()
            t2.draw()

            # draw settings area
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            # Timout occurred
            if t1.time <= 0 or t2.time <= 0:
                # TIMEOUT
                print("TIMEOUT!")
                t1.time = 999
                t2.time = 999
                pass

            dt = clock.tick(30) / 1000

            self.board.update()

            pygame.display.flip()
        pygame.quit()

g = Game()


# def game_screen(screen, board, p1_time, p2_time, color, ready):
#     board.update()

# menu = pygame_menu.Menu(600, 800, 'Chess', theme=pygame_menu.themes.THEME_DEFAULT)
# menu.add_selector('Select color: ', [('White', 1), ('Black', 2)])
# menu.add_selector('Select Opponent: ', [('Mini-max', 1), ('DeepLearning', 2)], onchange=Game.set_difficulty)
# menu.add_button('Start Game', Game.__init__)
# menu.add_button('Quit', pygame_menu.events.EXIT)
# menu.mainloop(SCREEN)
