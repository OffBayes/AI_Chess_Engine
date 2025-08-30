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


class GreedyOrder(Orderer):
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


class AttackOrder(Orderer):
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
