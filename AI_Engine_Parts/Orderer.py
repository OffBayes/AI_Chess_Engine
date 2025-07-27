# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:38:12 2025

@author: Prior_Bayes
"""


class Orderer:
    def legal_moves_list(self, board):
        """
        Legal_moves_list takes the moves generator and returns a list of moves.

        Arguments
        ---------
        board : the current board position.

        Returns
        -------
        legal_moves : A list of legal moves.
        """
        legal_moves = [i.uci() for i in board.legal_moves]
        return legal_moves

    def order_search(self, board):
        """
        Determine the order of moves to be searched.

        Arguments
        ---------
        board: the current board state.

        Returns
        -------
        search_order: a list ordered by the search order.
        """
        return self.legal_moves_list(board)


class GreedyOrder(Orderer):
    """
    An orderer which traverses the tree by looking at best options first.

    It inherits from Orderer.
    """

    def order_search(self, board, eval_func):
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