# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:40:56 2025

@author: Prior_Bayes
"""

# Imports
import chess
import re
import numpy as np
from .AI_Engine_Functions import fen_to_space


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
        Return list of controlled squares.

        Returns a list of squares that are controlled by pawns of the given
        color, even if there are no pieces to capture (i.e., includes diagonal
        influence).

        Arguments
        ---------
            board: a python-chess Board object.
            color: chess.WHITE or chess.BLACK

        Returns
        -------
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
        Calculate the current material score.

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
        Calculate the current space control.

        This function calculates the current space control. It scores space
        based on the number of opponent squares that can currently be moved to
        or a pawn could move to if a piece was there.

        It takes one argument:
        board: the current board state.

        It returns:
        A tuple where the first position is the white space score and the
        second is the black space score.
        """
        score = []
        for color in ['white', 'black']:
            if color == 'white':
                board.turn = True
                opponent_rows = ["5", "6", "7", "8"]
            else:
                board.turn = False
                opponent_rows = ["1", "2", "3", "4"]

            # Generate pseudo-legal moves, excluding all pawn moves
            legal_moves = ''.join([
                move.uci()
                for move in board.generate_pseudo_legal_moves()
                if board.piece_type_at(move.from_square) != chess.PAWN
            ])

            result = ''

            # Removes the starting squares so that only the end squares remain
            for i in range(2, len(legal_moves), 4):
                result += legal_moves[i:i+2]  # take 2 characters, skip 2

            # Adds the squares pawns can control
            pawn_controls = self.pawn_control_squares(
                board, board.turn)
            result += ''.join(pawn_controls)

            score.append(sum(result.count(moves) for moves in opponent_rows))
        score = tuple(score)
        return score

    def current_development(self, board):
        """
        Calculate the current development.

        This function calculates the current piece development. It scores
        development based on whether the current square is the same as the
        starting square.

        Arguments
        ---------
        board: the current board space.

        Returns
        -------
        development: the number of developed pieces
        """
        start_pos = fen_to_space(chess.Board()).split(' ')[0]
        start_pos = start_pos.split('/')
        curr_pos = fen_to_space(board).split(' ')[0]
        curr_pos = curr_pos.split('/')
        white_start_rows = "".join(start_pos[6:8])
        white_curr_rows = "".join(curr_pos[6:8])
        black_start_rows = "".join(start_pos[0:2])
        black_curr_rows = "".join(curr_pos[0:2])

        white_moved = sum([1 for white_start_rows, white_curr_rows in
                           zip(white_start_rows, white_curr_rows)
                           if white_start_rows != white_curr_rows])
        black_moved = sum([1 for black_start_rows, black_curr_rows in
                           zip(black_start_rows, black_curr_rows)
                           if black_start_rows != black_curr_rows])
        white_taken = 16 - sum([1 for char in "".join(curr_pos)
                                if char.isupper()])
        black_taken = 16 - sum([1 for char in "".join(curr_pos)
                                if char.islower()])
        development = (white_moved - white_taken, black_moved - black_taken)
        return development

    def current_pawnisland(self, board):
        """
        Current_pawnchain calculates the current number of pawn chains.

        Arguments
        ---------
        board: the current board space.

        Returns
        -------
        chain_num: An integer representing the pawn chain number.
        """
        # Numerical notation of pawn squares
        pawn_squares_num = ([square for square, piece
                             in board.piece_map().items()
                             if piece == chess.Piece.from_symbol('P')])

        # String notation of pawn squares
        pawn_loc = ''.join([chess.square_name(i) for i in pawn_squares_num])
        # Remove all digits from string
        pawn_loc = re.sub(r'\d+', '', pawn_loc)
        # Sorts the columns alphabetically
        pawn_loc = ''.join(sorted(pawn_loc))

    def score_pos(self, board, weights=[1, 0.2, 0.2]):
        """
        Scores a position.

        It scores based on multiple categories:
        material, development, squares controlled, king safety, etc.

        It takes two arguments:
        board: The current board space.
        weights: The relative value of different points

        It returns:
        A numerical score of the position, where 0 means it is equal, a
        negative means it favors black, and a positive means it favors
        white.
        """
        white_mat, black_mat = self.current_material(board)
        white_spac, black_spac = self.current_space(board)
        white_dev, black_dev = self.current_development(board)
        if board.is_checkmate():
            score = -np.inf if board.turn else np.inf
        else:
            score = (weights[0] * (white_mat - black_mat)
                     + weights[1] * (white_spac - black_spac)
                     + weights[2] * (white_dev - black_dev))
        return score
