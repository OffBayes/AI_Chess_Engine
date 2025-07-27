# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 19:00:28 2025

@author: Prior_Bayes
"""

# Imports
from .Pruner import Pruner


class ChessEngine:
    """
    A customizable chess engine.

    ChessEngine allows users to configure the engine's behavior by supplying
    different components at initialization time. ChessEngine requires a search
    engine and evaluation engine to create an object. These engines determine
    the logic used to determine what move to make.
    """

    def __init__(self, search, evaluation, pruner=Pruner):
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
        self.depth = 4

    def evaluate(self, board):
        """Return the evaluation score of the given board."""
        return self.evalEng.score_pos(board)

    def find_best_move(self, board, depth):
        """Use the composed search engine to find the best move."""
        hyp_board = board.copy()
        return self.searchEng.search(hyp_board, self.evaluate, depth)
