import pygame
import os

from settings import *

K_b = pygame.image.load(os.path.join("img", "king-black.png"))
Q_b = pygame.image.load(os.path.join("img", "queen-black.png"))
B_b = pygame.image.load(os.path.join("img", "bishop-black.png"))
H_b = pygame.image.load(os.path.join("img", "knight-black.png"))
R_b = pygame.image.load(os.path.join("img", "rook-black.png"))
P_b = pygame.image.load(os.path.join("img", "pawn-black.png"))

K_w = pygame.image.load(os.path.join("img", "king-white.png"))
Q_w = pygame.image.load(os.path.join("img", "queen-white.png"))
B_w = pygame.image.load(os.path.join("img", "bishop-white.png"))
H_w = pygame.image.load(os.path.join("img", "knight-white.png"))
R_w = pygame.image.load(os.path.join("img", "rook-white.png"))
P_w = pygame.image.load(os.path.join("img", "pawn-white.png"))


class Piece:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.images = None
        self.firstMove = True

    def draw(self):
        if self.color == WHITE:
            SCREEN.blit(self.images[0], to_coords(self.x, self.y))
        else:
            SCREEN.blit(self.images[1], to_coords(self.x, self.y))

    def move(self, x, y):
        self.x = x
        self.y = y


class King(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(K_w, (64, 64)), pygame.transform.scale(K_b, (64, 64)))

    def valid_moves(self, board):

        moves = []

        # move 1 in each direction
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if board.valid_move((x, y), self.color):
                    moves.append((x, y))
        return moves


class Queen(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(Q_w, (64, 64)), pygame.transform.scale(Q_b, (64, 64)))

    def valid_moves(self, board):

        # Queen's move set is simply Rook and Bishop combined
        moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)

        return moves


class Bishop(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(B_w, (64, 64)), pygame.transform.scale(B_b, (64, 64)))

    def valid_moves(self, board):

        moves = []

        # up left
        x, y = self.x, self.y
        while board.valid_move((x-1, y-1), self.color):
            moves.append((x-1, y-1))
            if board.piece_at_coords((x-1, y-1)):
                break
            x -= 1
            y -= 1

        # up right
        x, y = self.x, self.y
        while board.valid_move((x+1, y-1), self.color):
            moves.append((x+1, y-1))
            if board.piece_at_coords((x+1, y-1)):
                break
            x += 1
            y -= 1

        # down left
        x, y = self.x, self.y
        while board.valid_move((x-1, y+1), self.color):
            moves.append((x-1, y+1))
            if board.piece_at_coords((x-1, y+1)):
                break
            x -= 1
            y += 1

        # down right
        x, y = self.x, self.y
        while board.valid_move((x+1, y+1), self.color):
            moves.append((x+1, y+1))
            if board.piece_at_coords((x+1, y+1)):
                break
            x += 1
            y += 1

        return moves


class Knight(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(H_w, (64, 64)), pygame.transform.scale(H_b, (64, 64)))

    def valid_moves(self, board):

        moves = []

        for x in range(self.x-2, self.x+3):
            for y in range(self.y-2, self.y+3):
                if abs(self.x - x) == 2 and abs(self.y - y) == 1 or abs(self.x - x) == 1 and abs(self.y - y) == 2:
                    if board.valid_move((x, y), self.color):
                        moves.append((x, y))
        return moves


class Rook(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(R_w, (64, 64)), pygame.transform.scale(R_b, (64, 64)))

    def valid_moves(self, board):

        moves = []

        # up
        for y in range(self.y-1, -1, -1):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        # down
        for y in range(self.y+1, 8, 1):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        # left
        for x in range(self.x-1, -1, -1):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        # right
        for x in range(self.x+1, 8, 1):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        return moves


class Pawn(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.images = (pygame.transform.scale(P_w, (64, 64)), pygame.transform.scale(P_b, (64, 64)))

    def valid_moves(self, board):

        moves = []
        if board.human == WHITE:
            # move forward 1
            if board.valid_move((self.x, self.y-1), self.color) \
                    and not board.piece_at_coords((self.x, self.y-1)):
                moves.append((self.x, self.y-1))

                # move forward 2 on first move
                if board.valid_move((self.x, self.y-2), self.color) \
                        and not board.piece_at_coords((self.x, self.y-2)) \
                        and self.firstMove:
                    moves.append((self.x, self.y-2))

            # attack diagonal left
            if board.valid_move((self.x-1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y-1), self.color):
                moves.append((self.x-1, self.y-1))

            # attack diagonal right
            if board.valid_move((self.x+1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y-1), self.color):
                moves.append((self.x+1, self.y-1))
        else:
            # move forward 1
            if board.valid_move((self.x, self.y+1), self.color) \
                    and not board.piece_at_coords((self.x, self.y+1)):
                moves.append((self.x, self.y+1))

                # move forward 2 on first move
                if board.valid_move((self.x, self.y+2), self.color) \
                        and not board.piece_at_coords((self.x, self.y+2)) \
                        and self.firstMove:
                    moves.append((self.x, self.y+2))

            # attack diagonal left
            if board.valid_move((self.x-1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y+1), self.color):
                moves.append((self.x-1, self.y+1))

            # attack diagonal right
            if board.valid_move((self.x+1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y+1), self.color):
                moves.append((self.x+1, self.y+1))

        return moves
