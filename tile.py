from settings import *


class Tile:
    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y
        self.color = BLACK
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))

    def __repr__(self):
        return f"Tile ({self.x}, {self.y})"

    def fill(self, color):
        self.surface.fill(color)

    def select(self):
        if self.contains_piece():
            self.fill(LIGHT_BLUE)
            self.draw()

    def draw(self):
        SCREEN.blit(self.surface, to_coords(self.x, self.y))
        if self.piece:
            self.piece.draw()

    def contains_piece(self):
        if self.piece.images is None:
            return False
        return True
