import random
from math import inf
from piece import *


def random_move(board):
    '''
    selects a random move from the valid moves for the current players turn
    :param board: the current board being used for the game (Board)
    :return: tuple representing move ((sourceX, sourceY), (destX, destY))
    '''
    moves = board.get_moves()
    if moves:
        return random.choice(moves)


def evaluate(board):
    '''
    provides a number representing the value of the board at a given state
    :param board: the current board being used for the game (Board)
    :return: integer representing boards value
    '''
    return board.whiteScore - board.blackScore


def minimax(board, depth, alpha, beta, maximizing_player):
    '''
    minimax algorithm used to find best move for the AI
    :param board: the current board being used for the game (Board)
    :param depth: controls how deep to search the tree of possible moves (int)
    :param alpha: the best value that the maximizer currently can guarantee at that level or above (int)
    :param beta: the best value that the minimizer currently can guarantee at that level or above (int)
    :param maximizing_player: True if current player is maximizing player (bool)
    :return: tuple representing move and eval (move, eval)
    '''
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