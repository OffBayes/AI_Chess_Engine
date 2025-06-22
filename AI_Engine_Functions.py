# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025

@author: Prior_Bayes

Purpose: Create a Chessbot
"""
# Imports
import chess
import chess.polyglot
import re
import numpy as np

# Functions
def legal_moves_list(board):
    legal_moves = [i.uci() for i in board.legal_moves]
    return legal_moves

# Classes
class ChessEngine:
    """
    A customizable chess engine.

    ChessEngine allows users to configure the engine's behavior by supplying
    different components at initialization time. ChessEngine requires a search
    engine and evaluation engine to create an object. These engines determine
    the logic used to determine what move to make.
    """

    def __init__(self, search, evaluation):
        """
        Initialize the engine with specific components.

        Arguments
        ---------
            search: The engine's search component.
            evaluation: The engine's board evaluation component.
        """
        self.searchEng = search
        self.evalEng = evaluation
        self.white = True
        self.black = False

    def evaluate(self, board):
        """Return the evaluation score of the given board."""
        return self.evalEng.score_pos(board)

    def find_best_move(self, board, depth=2):
        """Use the composed search engine to find the best move."""
        return self.searchEng.search(board, self.evaluate, depth)


class SearchEng:
    """
    A customizable search engine that allows different search approaches.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.
    """

    def minimax(self, board_node, eval_func):
        """
        Minimax finds the maximum value move for one full turn cycle (two ply).
        It assumes the opponent plays optimally (according to the evaluation
        function. It returns the maximum value move and the value for the
        current player.

        Arguments
        ---------
        board_node: a hypothetical board state that could be reached.

        It returns:
        A tuple where the best move is first and the score is second.
        """
        hyp_board = board_node.copy()
        legal_moves = legal_moves_list(board_node)

        scores = []

        # This layer of for loop scores all of the current player's moves - MAX
        for move in legal_moves:
            hyp_board.push_san(move)
            opp_legal_moves = legal_moves_list(hyp_board)

            # This is a list of the scores after the opponent makes each move
            response_scores = []

            # This layer of for loop scores all of the opponent's moves - MIN
            for opp_move in opp_legal_moves:
                hyp_board.push_san(opp_move)
                response_scores.append(eval_func(hyp_board))
                hyp_board.pop()
            # Assume opponent makes best move by minimizes the score
            scores.append(min(response_scores))
            hyp_board.pop()

        # Return the best move and associated maximum score value
        best_move = (legal_moves[scores.index(max(scores))], max(scores))

        return best_move

    def search(self, board, eval_func, depth=2):
        """
        This function evaluates the best score that can be achieved from the
        current position using a recursive minimax search up to a given depth.

        It takes three arguments:
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: how many ply deep the search goes.

        It returns:
        A tuple where the first element is the best move in UCI format, and the
        second element is the corresponding score.
        """
        hyp_board = board.copy()

        if depth == 0 or hyp_board.is_game_over():
            return (None, eval_func(hyp_board))

        legal_moves = legal_moves_list(hyp_board)

        if hyp_board.turn is True:
            best_value = -np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                _, value = self.search(hyp_board, eval_func, depth - 1)
                hyp_board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move

            return (best_move, best_value)

        else:
            best_value = np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                _, value = self.search(hyp_board, eval_func, depth - 1)
                hyp_board.pop()
                if value < best_value:
                    best_value = value
                    best_move = move

            return (best_move, best_value)

class AlphaBetaSearch(SearchEng):
    """
    A search engine with alpha beta pruning.
    """

    def search(self, board, eval_func, depth=4, alpha=-np.inf, beta=np.inf):
        """
        This function evaluates the best score that can be achieved from the
        current position using a recursive minimax search up to a given depth.

        It takes three arguments:
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: how many ply deep the search goes.

        It returns:
        A tuple where the first element is the best move in UCI format, and the
        second element is the corresponding score.
        """
        hyp_board = board.copy()

        if depth == 0 or hyp_board.is_game_over():
            return (None, eval_func(hyp_board))

        legal_moves = legal_moves_list(hyp_board)

        if hyp_board.turn is True:
            best_value = -np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                _, value = self.search(hyp_board, eval_func, depth - 1)
                hyp_board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return (best_move, best_value)

        else:
            best_value = np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                _, value = self.search(hyp_board, eval_func, depth - 1)
                hyp_board.pop()
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return (best_move, best_value)


class EvalEng:
    """
    EvalEng represents the chess engine evaluation capability.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.

    Methods
    -------
        score_pos: Checks whether subclass has implemented scoring function.
    """

    def score_pos(self, board):
        """
        score_pos scores a position to see which player has the advantage.
        
        It 
        
        """
        raise NotImplementedError("Subclasses must implement score_pos")

    def pawn_control_squares(self, board, color):
        """
        Returns a list of squares that are controlled by pawns of the given
        color, even if there are no pieces to capture (i.e., includes diagonal
        influence).

        Arguments:
        - board: a python-chess Board object.
        - color: chess.WHITE or chess.BLACK

        Returns:
        - A list of controlled square names (e.g., ["e4", "f5", "e4"])
        """
        controlled = []
        direction = 1 if color == chess.WHITE else -1

        for square in board.pieces(chess.PAWN, color):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            for df in [-1, 1]:
                f = file + df
                r = rank + direction
                if 0 <= f <= 7 and 0 <= r <= 7:
                    target_square = chess.square(f, r)
                    controlled.append(chess.square_name(target_square))
        return controlled


class HeuristicEval(EvalEng):
    """
    HeuristicEval attempts to evaluate the position using chess heuristics.

    Traditional heuristics include material count, squares controlled, piece
    development, pawn structure, king safety, etc.

    Methods
    -------
        current_material: calculatest the material score of the position.
        current_space: calculates the number of opponent's squares controlled.
        current_development: counts the number of pieces developed.
        current_pawnshain: counts the number of pawn-cahins.

    """

    def current_material(self, board):
        """
        This function calculates the current material score. It uses common
        scoring values — pawn: 1, knight: 3, bishop: 3.2, rook: 5, queen: 9.

        It takes one argument:
        board: the current board state.

        It returns:
        A tuple where the first position is the white material score and the
        second is the black material score.
        """
        state = board.board_fen()
        white_score = (state.count('P')
                       + 3*state.count('N')
                       + 3.2*state.count('B')
                       + 5*state.count('R')
                       + 9*state.count('Q'))

        black_score = (state.count('p')
                       + 3*state.count('n')
                       + 3.2*state.count('b')
                       + 5*state.count('r')
                       + 9*state.count('q'))
        scores = (white_score, black_score)
        return scores

    def current_space(self, board):
        """
        This function calculates the current space control. It scores space
        based on the number of opponent squares that can currently be moved to
        or a pawn could move to if a piece was there.

        It takes one argument:
        board: the current board state.

        It returns:
        A tuple where the first position is the white space score and the
        second is the black space score.
        """
        hyp_board = board.copy()
        score = []
        for color in ['white', 'black']:
            if color == 'white':
                hyp_board.turn = True
                opponent_rows = ["5", "6", "7", "8"]
            else:
                hyp_board.turn = False
                opponent_rows = ["1", "2", "3", "4"]

            # Generate pseudo-legal moves, excluding all pawn moves
            legal_moves = ''.join([
                move.uci()
                for move in hyp_board.generate_pseudo_legal_moves()
                if hyp_board.piece_type_at(move.from_square) != chess.PAWN
            ])

            result = ''

            # Removes the starting squares so that only the end squares remain
            for i in range(2, len(legal_moves), 4):
                result += legal_moves[i:i+2]  # take 2 characters, skip 2

            # Adds the squares pawns can control
            pawn_controls = self.pawn_control_squares(
                hyp_board, hyp_board.turn)
            result += ''.join(pawn_controls)

            score.append(sum(result.count(moves) for moves in opponent_rows))
        score = tuple(score)
        return score

    def current_development(self, board):
        """
        This function calculates the current piece development. It scores
        development based on whether the current square is the same as the
        starting square.

        Arguments
        ---------
        board: the current board space.

        It returns:
        An integer which shows how much more developed the current player is
        compared to the opponent.
        """
        hyp_board = board.copy()

    def current_pawnchain(self, board):
        """
        This function calculates the current number of pawn chains. 

        Arguments
        ---------
        board: the current board space.

        Returns
        -------
        An integer which indicates how many pawn chains the current player has.
        """
        hyp_board = board.copy()

        # Checks the color of the current player
        if hyp_board.turn == ChessEngine().white:
            C = 'P'
        else:
            C = 'p'

        # Numerical notation of pawn squares
        pawn_squares_num = [square for square, piece in hyp_board.piece_map().items() if piece == chess.Piece.from_symbol(C)]

        # String notation of pawn squares
        pawn_loc = ''.join([chess.square_name(i) for i in pawn_squares_num])
        pawn_loc = re.sub(r'\d+', '', pawn_loc)  # Remove all digits from the string
        pawn_loc = ''.join(sorted(pawn_loc))     # Sorts the columns alphabetically 

    def score_pos(self, board, weights=[1, 0.2]):
        """
        This function scores a position. It scores based on 4 categories:
        material, development, squares controlled, king safety, etc.

        It takes two arguments:
        board: The current board space.
        weights: The relative value of different points

        It returns:
        A numerical score of the position, where 0 means it is equal, a
        negative means it favors black, and a positive means it favors
        white.
        """
        mat = self.current_material(board)
        spac = self.current_space(board)
        if board.is_checkmate():
            score = -np.inf if board.turn else np.inf
        else:
            score = (weights[0] * (mat[0]-mat[1])
                     + weights[1] * (spac[0]-spac[1]))
        return score


# board.push_san(eng.find_best_move(board, depth=2)[0])