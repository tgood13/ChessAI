import random
from math import inf
from piece import *


def random_move(board):
    """
    Selects a random move from the valid moves for the current players turn
    :param board: the current board being used for the game (Board)
    :return: tuple representing move ((sourceX, sourceY), (destX, destY))
    """
    moves = board.get_moves()
    if moves:
        return random.choice(moves)


def evaluate(board, maximizing_color):
    """
    Provides a number representing the value of the board at a given state
    :param board: the current board being used for the game (Board)
    :param maximizing_color: color associated with maximizing player (tuple)
    :return: integer representing boards value
    """
    if maximizing_color == WHITE:
        return board.whiteScore - board.blackScore
    else:
        return board.blackScore - board.whiteScore


def minimax(board, depth, alpha, beta, maximizing_player, maximizing_color):
    """
    Minimax algorithm used to find best move for the AI
    :param board: the current board being used for the game (Board)
    :param depth: controls how deep to search the tree of possible moves (int)
    :param alpha: the best value that the maximizer currently can guarantee at that level or above (int)
    :param beta: the best value that the minimizer currently can guarantee at that level or above (int)
    :param maximizing_player: True if current player is maximizing player (bool)
    :param maximizing_color: color of the AI using this function to determine a move (tuple)
    :return: tuple representing move and eval; format: (move, eval)
    """
    if depth == 0 or board.gameover:
        return None, evaluate(board, maximizing_color)
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board_copy = board.copy()
            board_copy.make_move(move[0], move[1])
            current_eval = minimax(board_copy, depth - 1, alpha, beta, False, maximizing_color)[1]
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
            board_copy.make_move(move[0], move[1])
            current_eval = minimax(board_copy, depth - 1, alpha, beta, True, maximizing_color)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval


def minimax2(board, depth, alpha, beta, maximizing_player, maximizing_color):
    """
    Minimax algorithm used to find best move for the AI
    :param board: the current board being used for the game (Board)
    :param depth: controls how deep to search the tree of possible moves (int)
    :param alpha: the best value that the maximizer currently can guarantee at that level or above (int)
    :param beta: the best value that the minimizer currently can guarantee at that level or above (int)
    :param maximizing_player: True if current player is maximizing player (bool)
    :return: tuple representing move and eval (move, eval)
    """
    if depth == 0 or board.gameover:
        return None, evaluate(board, maximizing_color)
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximizing_player:
        max_eval = -inf
        for move in moves:
            board.make_move(move[0], move[1])
            current_eval = minimax2(board, depth - 1, alpha, beta, False, maximizing_color)[1]
            board.unmake_move()
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
            board.make_move(move[0], move[1])
            current_eval = minimax2(board, depth - 1, alpha, beta, True, maximizing_color)[1]
            board.unmake_move()
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
