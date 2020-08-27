import random
from math import inf
from piece import *

def random_move(board):
    return random.choice(board.get_moves())

def evaluate(board):

    # materialScore = 900 * (board.count(WHITE, King)-board.count(BLACK, King)) \
    #                 + 90 * (board.count(WHITE, Queen)-board.count(BLACK, Queen)) \
    #                 + 50 * (board.count(WHITE, Rook)-board.count(BLACK, Rook)) \
    #                 + 30 * (board.count(WHITE, Bishop)-board.count(BLACK, Bishop)) \
    #                 + 30 * (board.count(WHITE, Knight)-board.count(BLACK, Knight)) \
    #                 + 10 * (board.count(WHITE, Pawn)-board.count(BLACK, Pawn))


    return board.whiteScore - board.blackScore


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.checkmate():
        return None, evaluate(board)
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board_copy = board.copy()
            board_copy.move_piece(move[0], move[1])
            current_eval = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        for move in moves:
            board_copy = board.copy()
            board_copy.move_piece(move[0], move[1])
            current_eval = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval