# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:40:56 2025

@author: Prior_Bayes
"""

# Imports
import chess
import re
from .AI_Engine_Functions import fen_to_space

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.5,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# Pre-computed bitboards for opponent territories
BB_WHITE_TERRITORY = chess.BB_RANK_5 | chess.BB_RANK_6 | chess.BB_RANK_7 | chess.BB_RANK_8
BB_BLACK_TERRITORY = chess.BB_RANK_1 | chess.BB_RANK_2 | chess.BB_RANK_3 | chess.BB_RANK_4


class EvalEng:
    """
    EvalEng represents the chess engine evaluation capability.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.

    Methods
    -------
        score_pos: Checks whether subclass has implemented scoring function.
    """

    def score_pos(self, board: chess.Board):
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





