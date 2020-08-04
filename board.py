from piece import *

import pygame

import copy

from settings import *
from tile import *


class Board:

    def __init__(self):
        self.tilemap = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_tiles()
        self.selected = None
        self.blackKingCoords = None
        self.whiteKingCoords = None
        self.turn = WHITE
        self.playerpos = "bot"
        self.player = WHITE

    def initialize_pieces(self) -> None:
        """
        places all tiles in the correct starting position
        """

        # remove all pieces from board
        for x in range(8):
            for y in range(8):
                self.tilemap[x][y].piece = None

        # pawns
        for i in range(8):
            self.tilemap[i][1].piece = Pawn(i, 1, BLACK)
            self.tilemap[i][6].piece = Pawn(i, 6, WHITE)

        # rooks
        self.tilemap[0][0].piece = Rook(0, 0, BLACK)
        self.tilemap[7][0].piece = Rook(7, 0, BLACK)
        self.tilemap[0][7].piece = Rook(0, 7, WHITE)
        self.tilemap[7][7].piece = Rook(7, 7, WHITE)

        # knights
        self.tilemap[1][0].piece = Knight(1, 0, BLACK)
        self.tilemap[6][0].piece = Knight(6, 0, BLACK)
        self.tilemap[1][7].piece = Knight(1, 7, WHITE)
        self.tilemap[6][7].piece = Knight(6, 7, WHITE)

        # bishops
        self.tilemap[2][0].piece = Bishop(2, 0, BLACK)
        self.tilemap[5][0].piece = Bishop(5, 0, BLACK)
        self.tilemap[2][7].piece = Bishop(2, 7, WHITE)
        self.tilemap[5][7].piece = Bishop(5, 7, WHITE)

        # queens
        self.tilemap[3][0].piece = Queen(3, 0, BLACK)
        self.tilemap[3][7].piece = Queen(3, 7, WHITE)

        # kings
        self.tilemap[4][0].piece = King(4, 0, BLACK)
        self.tilemap[4][7].piece = King(4, 7, WHITE)

        # store coords of both kings
        self.blackKingCoords = (4, 0)
        self.whiteKingCoords = (4, 7)

        if self.player == BLACK:
            self.blackKingCoords = (4, 7)
            self.whiteKingCoords = (4, 0)
            for x in range(8):
                for y in range(8):
                    if self.piece_at_coords((x, y)):
                        if self.tilemap[x][y].piece.color == BLACK:
                            self.tilemap[x][y].piece.color = WHITE
                        else:
                            self.tilemap[x][y].piece.color = BLACK

    def initialize_tiles(self) -> None:
        """
        draws tile grid for the chess board
        """
        cnt = 0
        for x in range(8):
            for y in range(8):
                tile = Tile(None, x, y)
                if cnt % 2 == 0:
                    tile.color = BEIGE
                    tile.fill(BEIGE)
                else:
                    tile.color = BROWN
                    tile.fill(BROWN)
                self.tilemap[x][y] = tile
                cnt += 1
            cnt += 1

    def update(self) -> None:
        """
        draws all components of the board
        """

        # draw tiles and pieces
        for row in self.tilemap:
            for tile in row:
                tile.draw()

        # draw circles to indicate valid move locations
        if self.selected:
            moves = self.selected.piece.valid_moves(self) + self.can_castle(self.selected.piece.color)
            for move in moves:
                if not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y),
                                                move, self.selected.piece.color):
                    tup = to_coords(move[0], move[1])
                    x = tup[0] + int(TILE_SIZE / 2)
                    y = tup[1] + int(TILE_SIZE / 2)
                    tup2 = x, y
                    pygame.draw.circle(SCREEN, GREEN, tup2, 10)
        # if self.in_check(BLACK):
        #     print("Black is in check!")
        # if self.in_check(WHITE):
        #     print("White is in check!")

    def select(self) -> None:
        """
        selects tile that contains the mouse pointer if tile is valid
        """

        # get position of mouse
        pos = pygame.mouse.get_pos()

        # get coordinates of top left corner of selected tile
        x = (pos[0] - BOARD_X) // TILE_SIZE
        y = (pos[1] - BOARD_Y) // TILE_SIZE
        coords = x, y

        # if mouse position is out of bounds, de-select current tile (if applicable) and restore its color
        if not self.in_bounds(coords):
            print("Out of bounds selection.")
            if self.selected:
                self.selected.fill(self.selected.color)
                self.selected = None
            return

        # handle castling case
        if self.selected and type(self.selected.piece) is King and self.can_castle(self.selected.piece.color):
            print("Castling!")
            if (x, y) == (2, 7):
                self.move_piece((4, 7), (2, 7))
                self.move_piece((0, 7), (3, 7))
            elif (x, y) == (6, 7):
                self.move_piece((4, 7), (6, 7))
                self.move_piece((7, 7), (5, 7))
            elif (x, y) == (2, 0):
                self.move_piece((4, 0), (2, 0))
                self.move_piece((0, 0), (3, 0))
            elif (x, y) == (6, 0):
                self.move_piece((4, 0), (6, 0))
                self.move_piece((7, 0), (5, 0))
            self.selected = None
            self.next_turn()
            return

        # if a piece is already selected, make move to selected tile
        if self.selected and coords in self.selected.piece.valid_moves(self) \
                and not self.in_check_after_move((self.selected.piece.x, self.selected.piece.y), coords,
                                                 self.selected.piece.color):
            print("Moving Piece!")
            self.move_piece((self.selected.x, self.selected.y), (x, y))
            self.selected = None
            self.next_turn()
            return

        # restore color and de-select previously selected tile before selecting new tile
        if self.selected:
            print("De-selecting old tile.")
            self.selected.fill(self.selected.color)
            self.selected = None

        # select tile at coordinates and remember tile
        if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
            print("Selected Tile.")
            self.tilemap[x][y].select()
            self.selected = self.tilemap[x][y]

    def piece_at_coords(self, coords) -> bool:
        """
        returns True if tile at coords contains a piece of any kind
        """
        if self.tilemap[coords[0]][coords[1]].piece is None:
            return False
        return True

    def move_piece(self, source, dest) -> None:
        """
        moves piece from source coords to dest coords and makes necessary updates to game state
        """

        # get shorthand for source and destination tiles
        sourceTile = self.tilemap[source[0]][source[1]]
        destTile = self.tilemap[dest[0]][dest[1]]

        # promote piece if it meets requirements
        if type(sourceTile.piece) is Pawn:
            if sourceTile.piece.color == WHITE and destTile.y == 0 \
                    or sourceTile.piece.color == BLACK and destTile.y == 7:
                sourceTile.piece = Queen(sourceTile.piece.x, sourceTile.piece.y, sourceTile.piece.color)

        # move piece from source tile to dest tile
        destTile.piece = sourceTile.piece
        destTile.piece.move(destTile.x, destTile.y)
        destTile.piece.firstMove = False

        # update king coords if necessary
        if type(sourceTile.piece) is King:
            if sourceTile.piece.color == BLACK:
                self.blackKingCoords = destTile.x, destTile.y
            else:
                self.whiteKingCoords = destTile.x, destTile.y

        # remove piece from source tile
        sourceTile.piece = None  # ADD PIECE TO LIST OF TAKEN
        sourceTile.fill(sourceTile.color)

        self.checkmate()

    @staticmethod
    def in_bounds(coords) -> bool:
        """
        returns True if given coords are within the bounds of the board
        """
        if coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8:
            return False
        return True

    def enemy_at_coords(self, coords, color) -> bool:
        """
        returns True if color of the piece at coords is not same as specified color
        """
        if self.piece_at_coords(coords):
            return self.tilemap[coords[0]][coords[1]].piece.color != color

    def valid_move(self, dest, color) -> bool:
        """
        returns True if move to dest coords is within board's bounds and not obstructed
        """
        if self.in_bounds(dest) \
                and (not self.piece_at_coords(dest) or self.enemy_at_coords(dest, color)):
            return True
        return False

    def in_check(self, color) -> bool:
        """
        returns True if player of specified color is in check
        """
        kingCoords = None
        if color == BLACK:
            kingCoords = self.blackKingCoords
        else:
            kingCoords = self.whiteKingCoords

        # check if position of King is in any of the valid moves for opposite player
        for x in range(8):
            for y in range(8):
                if self.enemy_at_coords((x, y), color):
                    for move in self.tilemap[x][y].piece.valid_moves(self):
                        if move[0] == kingCoords[0] and move[1] == kingCoords[1]:
                            return True
        return False

    def in_check_after_move(self, source, dest, color) -> bool:
        """
        returns True if player of specified color is in check after a move from source to dest
        """
        in_check = False

        # get shorthand for source and destination tiles and pieces
        sourceTile = self.tilemap[source[0]][source[1]]
        destTile = self.tilemap[dest[0]][dest[1]]
        destPiece = destTile.piece
        sourcePiece = sourceTile.piece

        # preserve king coords
        kingCoords = None
        if type(sourcePiece) is King:
            if color == BLACK:
                kingCoords = self.blackKingCoords
            else:
                kingCoords = self.whiteKingCoords

        # move piece from source tile to dest tile
        destTile.piece = sourcePiece
        destTile.piece.move(destTile.x, destTile.y)
        sourceTile.piece = None

        # set king coords
        if type(sourcePiece) is King:
            if color == BLACK:
                self.blackKingCoords = (destTile.piece.x, destTile.piece.y)
            else:
                self.whiteKingCoords = (destTile.piece.x, destTile.piece.y)

        # set playerpos
        if self.playerpos == "bot":
            self.playerpos = "top"
        else:
            self.playerpos = "bot"

        # see if in check state after move
        if self.in_check(color):
            in_check = True

        # restore king coords
        if type(sourcePiece) is King:
            if color == BLACK:
                self.blackKingCoords = kingCoords
            else:
                self.whiteKingCoords = kingCoords

        # restore playerpos
        if self.playerpos == "bot":
            self.playerpos = "top"
        else:
            self.playerpos = "bot"

        # move piece back
        sourceTile.piece = sourcePiece
        destTile.piece = destPiece
        sourceTile.piece.move(sourceTile.x, sourceTile.y)

        return in_check

    def can_castle(self, color) -> bool:
        """
        returns list of castling moves if player of specified color can castle
        """
        moves = []
        if color == WHITE:
            if type(self.tilemap[0][7].piece) is Rook and self.tilemap[0][7].piece.firstMove \
                    and type(self.tilemap[7][7].piece) is Rook and self.tilemap[7][7].piece.firstMove \
                    and type(self.tilemap[4][7].piece) is King \
                    and self.tilemap[4][7].piece.firstMove:
                # castle left
                if self.tilemap[1][7].piece == self.tilemap[2][7].piece == self.tilemap[3][7].piece is None:
                    moves.append((2, 7))
                # castle right
                if self.tilemap[5][7].piece == self.tilemap[6][7].piece is None:
                    moves.append((6, 7))
        else:
            if type(self.tilemap[0][0].piece) is Rook and self.tilemap[0][0].piece.firstMove \
                    and type(self.tilemap[7][0].piece) is Rook and self.tilemap[7][0].piece.firstMove \
                    and type(self.tilemap[4][0].piece) is King \
                    and self.tilemap[4][0].piece.firstMove:
                # castle left
                if self.tilemap[1][0].piece == self.tilemap[2][0].piece == self.tilemap[3][0].piece is None:
                    moves.append((2, 0))
                # castle right
                if self.tilemap[5][0].piece == self.tilemap[6][0].piece is None:
                    moves.append((6, 0))
        return moves

    def next_turn(self) -> None:
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

        if self.playerpos == "bot":
            self.playerpos = "top"
        else:
            self.playerpos = "bot"

    def checkmate(self) -> bool:
        legal_moves = 0
        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color != self.turn:
                    moves = self.tilemap[x][y].piece.valid_moves(self) + self.can_castle(self.tilemap[x][y].piece.color)
                    for move in moves:
                        if not self.in_check_after_move((self.tilemap[x][y].piece.x, self.tilemap[x][y].piece.y), move, self.tilemap[x][y].piece.color):
                            legal_moves += 1
        if legal_moves == 0 and not self.in_check(BLACK):           # CHANGE TO OPPONENT's COLOR
            print("GAME OVER: Stalemate")
        elif legal_moves == 0:
            print("GAME OVER: Checkmate")
        return legal_moves == 0

    # def check_win_conditions(self):
    #
    #     # checkmate
    #     self.checkmate()
    #
    #     # DRAW CONDITIONS #
    #     # stalemate
    #
    #     # insufficient material
    #     piece_counts = {"minor": 0, "king": 0, "knight": 0}
    #     for x in range(8):
    #         for y in range(8):
    #             piece = self.tilemap[x][y].piece
    #             if type(piece) is King:
    #                 piece_counts["king"] += 1