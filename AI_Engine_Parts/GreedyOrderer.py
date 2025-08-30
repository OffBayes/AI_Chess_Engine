# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 23:35:12 2025

@author: Prior_Bayes
"""
import chess
from .Orderer import Orderer


class GreedyOrderer(Orderer):
    """
    An orderer which traverses the tree by looking at best options first.

    It inherits from Orderer.
    """

    def order_search(self, board: chess.Board, eval_func) -> list[chess.Move]:
        """
        Determine the order of moves to be searched.

        This function determines the search order by evaluating the current
        score of each position. The move it checks first at each tree is the
        move which provides the best immediate value.

        Arguments
        ---------
        board: the current board state.
        eval_func: the function which scores a given position.

        Returns
        -------
        search_order: a list ordered by the search order.
        """
        unsorted_legal_moves = self.legal_moves_list(board)
        legal_move_scores = [(eval_func(move), move)
                             for move in unsorted_legal_moves]
        return sorted(legal_move_scores, reverse=board.Turn)
