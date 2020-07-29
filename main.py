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
        self.p1_name = "Player 1"
        self.p2_name = "Player 2"

        self.p1_ready = False
        self.p2_ready = False

        self.p1_timer = Timer(600, "bot")
        self.p2_timer = Timer(600, "top")

        self.p1_color = WHITE
        self.p2_color = BLACK

        self.board = Board()
        self.board.initialize_tiles()
        self.board.reset_pieces()

        self.menu_screen()
        #self.start_game()

    def menu_screen(self):
        p1_ready_button = pygame.Rect(BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*4+8, 28)
        p2_ready_button = pygame.Rect(BOARD_X+BOARD_SIZE+8, BOARD_Y-8-28, TILE_SIZE*4+8, 28)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if p1_ready_button.collidepoint(mouse_pos):
                        self.p1_ready = not self.p1_ready
                    if p2_ready_button.collidepoint(mouse_pos):
                        self.p2_ready = not self.p2_ready

            SCREEN.fill(BLACK)

            # draw names
            self.draw_name("top")
            self.draw_name("bot")

            # draw clocks
            self.p1_timer.draw()
            self.p2_timer.draw()

            # draw ready buttons
            self.draw_ready("top")
            self.draw_ready("bot")

            # draw settings area
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            # draw board
            self.board.update()

            # start game if both players ready
            if self.p1_ready and self.p2_ready:
                self.start_game()

            pygame.display.flip()
        pygame.quit()

    def draw_name(self, pos):

        # draw top name
        if pos == "top":
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y - 36, TILE_SIZE*2, 28])
            p1name = pygame.font.SysFont('menlottc', 18).render(self.p2_name, True, GREEN)
            SCREEN.blit(p1name, (BOARD_X+4, BOARD_Y - 32))
        else:
            pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*2, 28])
            p2name = pygame.font.SysFont('menlottc', 18).render(self.p1_name, True, GREEN)
            SCREEN.blit(p2name, (BOARD_X+4, BOARD_Y+BOARD_SIZE+12))

    def draw_ready(self, pos):
        if pos == "top":
            if self.p2_ready:
                pygame.draw.rect(SCREEN, GREEN, [BOARD_X+BOARD_SIZE+8, BOARD_Y-8-28, TILE_SIZE*4+8, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("READY", True, BLACK)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.6), BOARD_Y-4-28))
            else:
                pygame.draw.rect(SCREEN, RED, [BOARD_X+BOARD_SIZE+8, BOARD_Y-8-28, TILE_SIZE*4+8, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("NOT READY", True, BLACK)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.8), BOARD_Y-4-28))
        else:
            if self.p1_ready:
                pygame.draw.rect(SCREEN, GREEN, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*4+8, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("READY", True, BLACK)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.6), BOARD_Y+BOARD_SIZE+12))
            else:
                pygame.draw.rect(SCREEN, RED, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*4+8, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("NOT READY", True, BLACK)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*7+4 + ((TILE_SIZE*4+8)/1.8), BOARD_Y+BOARD_SIZE+12))

    def draw_draw(self):
        pass

    def draw_resign(self):
        pass

    def set_difficulty(self, value, difficulty):
        pass

    def start_game(self):

        # Game Loop
        clock = pygame.time.Clock()
        playing = True

        # initialize draw variables
        p1_draw_offered = False
        p2_draw_offered = False

        p1_resigned = False

        # create buttons
        draw_button = pygame.Rect(BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, (TILE_SIZE*4+8)/2-4, 28)
        resign_button = pygame.Rect(BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+4, BOARD_Y+BOARD_SIZE+8, (TILE_SIZE*4+8)/2-4, 28)

        dt = 0

        while playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.select()
                    mouse_pos = event.pos
                    if draw_button.collidepoint(mouse_pos):
                        p1_draw_offered = not p1_draw_offered
                    if resign_button.collidepoint(mouse_pos):
                        p1_resigned = True


            SCREEN.fill(BLACK)

            # decrement timer for player of current turn
            if self.board.human == WHITE:
                self.p2_timer.tick(dt)
            else:
                self.p1_timer.tick(dt)

            # draw names
            self.draw_name("top")
            self.draw_name("bot")

            # # draw captured pieces
            # pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y - 36, TILE_SIZE*5-16, 28])
            # pygame.draw.rect(SCREEN, GREY, [BOARD_X+TILE_SIZE*2+8, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*5-16, 28])
            # # count number of pieces of a type in player.captured_pieces --> [pawn-img] x 0

            # draw turn indicator
            if self.board.turn == self.p1_color:
                txt = pygame.font.SysFont('menlottc', 18).render("YOUR TURN", True, RED)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*3+8, BOARD_Y+BOARD_SIZE+12))
            else:
                txt = pygame.font.SysFont('menlottc', 18).render("THEIR TURN", True, RED)
                SCREEN.blit(txt, (BOARD_X+TILE_SIZE*3+8, BOARD_Y+BOARD_SIZE+12))

            # draw clocks
            self.p1_timer.draw()
            self.p2_timer.draw()

            # draw settings area
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            # draw 'draw' button
            if p1_draw_offered:
                pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, (TILE_SIZE*4+8)/2-4, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("Offered", True, GREEN)
                SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+32, BOARD_Y+BOARD_SIZE+12))
            else:
                pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, (TILE_SIZE*4+8)/2-4, 28])
                txt = pygame.font.SysFont('menlottc', 18).render("Offer Draw", True, GREEN)
                SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+16, BOARD_Y+BOARD_SIZE+12))

            # draw 'resign' button
            pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+4, BOARD_Y+BOARD_SIZE+8, (TILE_SIZE*4+8)/2-4, 28])
            txt = pygame.font.SysFont('menlottc', 18).render("Resign", True, GREEN)
            SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+36, BOARD_Y+BOARD_SIZE+12))

            # Game end: Timout
            if self.p1_timer.time <= 0 or self.p2_timer.time <= 0:
                # TIMEOUT
                print("GAME OVER: Timeout")
                self.p1_timer.time = 999
                self.p2_timer.time = 999

            # Game over: Draw
            if p1_draw_offered and p2_draw_offered:
                print("GAME OVER: Draw")
                pass

            # Game over: Resignation
            if p1_resigned:
                print("GAME OVER: Resignation")
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
