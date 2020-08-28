import pygame
import pygame_menu

from board import *
from timer import Timer
from math import inf

import AI

pygame.init()

FONT = pygame.font.Font(pygame.font.get_default_font(), 18)
BIG_FONT = pygame.font.Font(pygame.font.get_default_font(), 26)

# Title and Icon
pygame.display.set_caption("Chess")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Game:

    def __init__(self):
        self.p1_name = "Player 1"
        self.p2_name = "Minimax"

        self.p1_ready = False
        self.p2_ready = True

        self.p1_timer = Timer(600, "bot")
        self.p2_timer = Timer(600, "top")

        self.p1_color = WHITE
        self.p2_color = BLACK

        self.board = Board()
        self.board.initialize_pieces()

        #self.pregame_screen()
        #self.game_screen()
        self.menu_screen()

    def reset(self):
        self.p1_ready = False
        self.p2_ready = True
        self.p1_timer.reset()
        self.p2_timer.reset()
        self.p1_color = WHITE
        self.p2_color = BLACK
        self.board = Board()
        self.board.initialize_pieces()

    def set_ai(self, tup, value):
        self.p2_name = tup[0]
        # self.p2_ready = True

    def set_name(self, name):
        self.p1_name = name

    def menu_screen(self):
        theme = pygame_menu.themes.Theme(title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE)
        theme.widget_font = pygame_menu.font.FONT_NEVIS
        menu = pygame_menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH, 'Welcome', theme=theme)

        menu.add_text_input('Name : ', default=self.p1_name, onchange=self.set_name)
        menu.add_selector('AI : ', [('Minimax', 1), ('Random', 2)], onchange=self.set_ai)
        menu.add_button('Play', self.pregame_screen)
        menu.add_button('Quit', pygame_menu.events.EXIT)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            menu.mainloop(SCREEN)

            #self.board.update()
            pygame.display.flip()

    def pregame_screen(self):

        # create ready buttons
        p1_ready_button = pygame.Rect(BOARD_X+TILE_SIZE*3, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*3, 28)
        p2_ready_button = pygame.Rect(BOARD_X+TILE_SIZE*3, BOARD_Y-8-28, TILE_SIZE*3, 28)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if p1_ready_button.collidepoint(mouse_pos):
                        self.p1_ready = not self.p1_ready
                    # if p2_ready_button.collidepoint(mouse_pos):
                    #     self.p2_ready = not self.p2_ready

            SCREEN.fill(BLACK)

            # draw names
            self.draw_names()

            # draw ready buttons
            self.draw_ready_buttons()

            # draw clocks
            self.p1_timer.draw()
            self.p2_timer.draw()

            # draw disconnect button


            # draw settings area
            # pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            # draw board
            self.board.update()

            # start game if both players ready
            if self.p1_ready and self.p2_ready:
                running = False
                self.game_screen()

            pygame.display.flip()

    def game_screen(self):

        clock = pygame.time.Clock()
        playing = True

        p1_draw_offered = False
        p2_draw_offered = False

        p1_resigned = False
        p2_resigned = False

        # create buttons
        # draw_button = pygame.Rect(BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28)
        resign_button = pygame.Rect(BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28)
        # resign_button = pygame.Rect(int(BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+4), BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28)

        dt = 0

        # Game Loop
        while playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.select()
                    mouse_pos = event.pos
                    # if draw_button.collidepoint(mouse_pos):
                    #     p1_draw_offered = not p1_draw_offered
                    if resign_button.collidepoint(mouse_pos):
                        p1_resigned = True

            SCREEN.fill(BLACK)

            # decrement timer for player of current turn
            if self.board.turn == self.p2_color:
                self.p2_timer.tick(dt)
            else:
                self.p1_timer.tick(dt)

            # draw names
            self.draw_names()

            # draw turn indicator
            # if self.board.turn == self.p1_color:
            #     txt = FONT.render("YOUR TURN", True, RED)
            #     SCREEN.blit(txt, (BOARD_X+TILE_SIZE*2+8, BOARD_Y+BOARD_SIZE+12))
            # else:
            #     txt = FONT.render("THEIR TURN", True, RED)
            #     SCREEN.blit(txt, (BOARD_X+TILE_SIZE*2+8, BOARD_Y+BOARD_SIZE+12))

            # draw clocks
            self.p1_timer.draw()
            self.p2_timer.draw()

            # draw settings area
            # pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y, TILE_SIZE*4+8, TILE_SIZE*8])

            # # draw 'draw' button
            # if p1_draw_offered:
            #     pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28])
            #     txt = FONT.render("Offered", True, GREEN)
            #     SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+32, BOARD_Y+BOARD_SIZE+12))
            # else:
            #     pygame.draw.rect(SCREEN, GREY, [BOARD_X+BOARD_SIZE+8, BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28])
            #     txt = FONT.render("Offer Draw", True, GREEN)
            #     SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+16, BOARD_Y+BOARD_SIZE+12))

            # # draw 'resign' button
            # pygame.draw.rect(SCREEN, GREY, [int(BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+4), BOARD_Y+BOARD_SIZE+8, int((TILE_SIZE*4+8)/2-4), 28])
            # txt = FONT.render("Resign", True, GREEN)
            # SCREEN.blit(txt, (int(BOARD_X+BOARD_SIZE+8+(TILE_SIZE*4+8)/2+36), BOARD_Y+BOARD_SIZE+12))

            pygame.draw.rect(SCREEN, GREY, [BOARD_X + BOARD_SIZE + 8, BOARD_Y + BOARD_SIZE + 8, int((TILE_SIZE * 4 + 8) / 2 - 4), 28])
            txt = FONT.render("Resign", True, GREEN)
            SCREEN.blit(txt, (BOARD_X+BOARD_SIZE+16, BOARD_Y+BOARD_SIZE+12))

            if self.board.gameover:
                playing = False
                print("GAME OVER")
                if self.board.gameover[1] == self.board.player:
                    self.end_screen(self.board.gameover[0], self.p1_name)
                else:
                    self.end_screen(self.board.gameover[0], self.p2_name)

            # Game over: Timeout
            if self.p1_timer.time <= 0:
                playing = False
                print("GAME OVER: Timeout")
                self.end_screen("Timeout", self.p2_name)

            # Game over: Timeout
            if self.p2_timer.time <= 0:
                playing = False
                print("GAME OVER: Timeout")
                self.end_screen("Timeout", self.p1_name)

            # Game over: Draw
            if p1_draw_offered or p2_draw_offered:
                playing = False
                print("GAME OVER: Draw")
                self.end_screen("Draw")

            # Game over: Resignation
            if p1_resigned:
                playing = False
                print("GAME OVER: Resignation")
                self.end_screen("Resignation", self.p2_name)

            # Game over: Resignation
            if p2_resigned:
                playing = False
                print("GAME OVER: Resignation")
                self.end_screen("Resignation", self.p1_name)

            dt = clock.tick(30) / 1000

            # AI makes its move
            if self.board.turn == self.p2_color:
                move = None
                if self.p2_name == "Minimax":
                    move = AI.minimax(self.board, 1, -inf, inf, False)[0]
                else:
                    move = AI.random_move(self.board)
                self.board.move_piece(move[0], move[1])
                self.board.next_turn()
            else:
                #move = AI.minimax(self.board, 1, -inf, inf, False)[0]
                move = AI.random_move(self.board)
                self.board.move_piece(move[0], move[1])
                self.board.next_turn()

            self.board.update()

            pygame.display.flip()
        pygame.quit()

    def end_screen(self, condition, winner=None):

        bg = pygame.Rect(int(BOARD_X+TILE_SIZE*2.5), int(BOARD_Y+TILE_SIZE*2.5), TILE_SIZE*3, TILE_SIZE*2)
        rematch_button = pygame.Rect(bg.left, bg.bottom-28, bg.centerx-bg.left-2, 28)
        leave_button = pygame.Rect(bg.centerx+2, bg.bottom-28, bg.centerx-bg.left-2, 28)

        def fade(width, height):
            fade = pygame.Surface((width, height))
            fade.fill((0, 0, 0))
            for alpha in range(0, 175):
                fade.set_alpha(alpha)
                self.board.update()
                SCREEN.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(1)

        running = True
        fading = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if rematch_button.collidepoint(mouse_pos):
                        running = False
                        self.board.initialize_pieces()
                        self.board.gameover = None
                        self.p1_timer.reset()
                        self.p2_timer.reset()
                        self.game_screen()
                    if leave_button.collidepoint(mouse_pos):
                        running = False
                        self.reset()
                        self.menu_screen()
            if fading:
                fade(SCREEN_WIDTH, SCREEN_HEIGHT)
                fading = False

            # draw Game Over
            bg = pygame.draw.rect(SCREEN, GREY, [int(BOARD_X+TILE_SIZE*2.5), int(BOARD_Y+TILE_SIZE*2.5), TILE_SIZE*3, TILE_SIZE*2])
            pygame.draw.rect(SCREEN, BLACK, [int(BOARD_X+TILE_SIZE*2.5), int(BOARD_Y+TILE_SIZE*2.5), TILE_SIZE*3, TILE_SIZE*2], 1)
            txt = BIG_FONT.render("Game Over", True, RED)
            SCREEN.blit(txt, (BOARD_X+TILE_SIZE*3-8, int(BOARD_Y+TILE_SIZE*2.5+4)))

            # draw win condition and winner (if applicable)
            if winner:
                txt = FONT.render(winner + " won", True, GREEN)
                SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, BOARD_Y + TILE_SIZE * 3+4))
                txt = FONT.render(f"by {condition}", True, GREEN)
                SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, int(BOARD_Y + TILE_SIZE * 3.4)))
            else:
                txt = FONT.render(f"{condition}", True, GREEN)
                SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3+32, BOARD_Y + TILE_SIZE * 3))

            # draw Rematch button
            pygame.draw.rect(SCREEN, BLACK, [bg.left, bg.bottom-28, bg.centerx-bg.left+3, 28], 1)
            txt = FONT.render("Rematch", True, GREEN)
            SCREEN.blit(txt, (bg.left+8, bg.bottom-28+4))

            # draw Leave button
            pygame.draw.rect(SCREEN, BLACK, [bg.centerx+2, bg.bottom-28, bg.centerx-bg.left+3, 28], 1)
            txt = FONT.render("Leave", True, GREEN)
            SCREEN.blit(txt, (bg.centerx+20, bg.bottom-28+4))

            pygame.display.flip()

    def draw_names(self):
        # draw top name (player 2)
        pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y - 36, TILE_SIZE*2, 28])
        p1name = FONT.render(self.p2_name, True, GREEN)
        SCREEN.blit(p1name, (BOARD_X+4, BOARD_Y - 32))
        # draw bottom name (player 1)
        pygame.draw.rect(SCREEN, GREY, [BOARD_X, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*2, 28])
        p2name = FONT.render(self.p1_name, True, GREEN)
        SCREEN.blit(p2name, (BOARD_X+4, BOARD_Y+BOARD_SIZE+12))

    def draw_ready_buttons(self):
        if self.p2_ready:
            pygame.draw.rect(SCREEN, GREEN, [BOARD_X+TILE_SIZE*3, BOARD_Y-8-28, TILE_SIZE*3, 28])
            txt = FONT.render("READY", True, BLACK)
            SCREEN.blit(txt, (BOARD_X+TILE_SIZE*4, BOARD_Y-4-28))
        else:
            pygame.draw.rect(SCREEN, RED, [BOARD_X+TILE_SIZE*3, BOARD_Y-8-28, TILE_SIZE*3, 28])
            txt = FONT.render("NOT READY", True, BLACK)
            SCREEN.blit(txt, (int(BOARD_X+TILE_SIZE*3.7), BOARD_Y-4-28))
        if self.p1_ready:
            pygame.draw.rect(SCREEN, GREEN, [BOARD_X+TILE_SIZE*3, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*3, 28])
            txt = FONT.render("READY", True, BLACK)
            SCREEN.blit(txt, (BOARD_X+TILE_SIZE*4, BOARD_Y+BOARD_SIZE+12))
        else:
            pygame.draw.rect(SCREEN, RED, [BOARD_X+TILE_SIZE*3, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*3, 28])
            txt = FONT.render("NOT READY", True, BLACK)
            SCREEN.blit(txt, (int(BOARD_X+TILE_SIZE*3.7), BOARD_Y+BOARD_SIZE+12))

            #pygame.draw.rect(SCREEN, WHITE, [BOARD_X+TILE_SIZE*3, BOARD_Y+BOARD_SIZE+8, TILE_SIZE*3, 28])
            #SCREEN.blit(pygame.transform.scale(K_b, (32, 32)), (BOARD_X+TILE_SIZE*4, BOARD_Y+BOARD_SIZE+8))

    def draw_draw(self):
        pass

    def draw_resign(self):
        pass

Game()
