from timer import Timer
from settings import *


class Menu:

    def __init__(self):
        self.p1_color = WHITE
        self.p2_color = BLACK

        self.p1_name = "???"
        self.p2_name = "???"

        self.p1_captured_pieces = {"king": 0, "queen": 0, "rook": 0, "bishop": 0, "knight": 0, "pawn": 0}
        self.p2_captured_pieces = {"king": 0, "queen": 0, "rook": 0, "bishop": 0, "knight": 0, "pawn": 0}

        self.p1_time = 600
        self.p2_time = 600

        self.p1_timer = Timer(600, "bot")
        self.p2_timer = Timer(600, "top")

    def draw(self):
        pass