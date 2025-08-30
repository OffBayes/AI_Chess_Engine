# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:38:12 2025

@author: Prior_Bayes
"""
import chess

class Orderer:
    def legal_moves_list(self, board: chess.Board):
        """
        Legal_moves_list takes the moves generator and returns a list of moves.

        Arguments
        ---------
        board : the current board position.

        Returns
        -------
        legal_moves : A list of legal moves.
        """
        return list(board.legal_moves)

    def order_search(self, board: chess.Board) -> list[chess.Move]:
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
