# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 23:33:19 2025

@author: Prior_Bayes
"""
import chess
from .Orderer import Orderer


class AttackOrderer(Orderer):
    """
    AttackOrder orders the moves by looking at attacking moves first.
    """

    def get_attackers(self, board: chess.Board) -> chess.SquareSet:
        """
        Get the squares with attacking pieces on them.

        Arguments
        ---------
        board : the current board state.

        Returns
        -------
        attackers: a SquareSet of the attacking pieces
        """
        attackers = chess.SquareSet()
        # Check each enemy piece position
        for square in chess.SquareSet(board.occupied_co[not board.turn]):
            # Find which of my pieces are attacking this enemy piece
            my_attackers = board.attackers(board.turn, square)
            attackers |= my_attackers
        return attackers

    def order_search(self, board: chess.Board) -> list[chess.Move]:
        """
        Order moves by checking attackers first.

        Arguments
        ---------
        board: the current board state.

        Returns
        -------
        search_order: a list ordered by the search order.
        """
        legal_moves = self.legal_moves_list(board)
        attackers = self.get_attackers(board)

        # Moves where the starting square is an attacker square get priority
        capture_moves = [move for move in legal_moves
                         if move.from_square in attackers]
        quiet_moves = [move for move in legal_moves
                       if move.from_square not in attackers]

        return capture_moves + quiet_moves