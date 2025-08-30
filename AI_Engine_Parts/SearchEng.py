# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:42:38 2025

@author: Prior_Bayes
"""

# Imports
import numpy as np
from .Orderer import Orderer


class SearchEng:
    """
    A customizable search engine that allows different search approaches.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.
    """

    def __init__(self, pruner, orderer):
        """
        Initialize the search engine with a pruner and orderer.

        Arguments
        ---------
        pruner : The search engine's pruning component.
        orderer : The search engine's move ordering component.'
        """
        self.pruner = pruner
        self.orderer = orderer

    def minimax(self, board_node, eval_func):
        """
        Minimax finds the maximum value move for one full turn cycle (two ply).

        It assumes the opponent plays optimally (according to the evaluation
        function. This function minimizes the score for black and maximizes it
        for white.

        Arguments
        ---------
        board_node: a hypothetical board state that could be reached.

        It returns:
        best_move: A tuple with the best move and associated score.
        """
        hyp_board = board_node.copy()
        legal_moves = Orderer.legal_moves_list(board_node)

        scores = []

        # This layer of for loop scores all of the current player's moves - MAX
        for move in legal_moves:
            hyp_board.push_san(move)
            opp_legal_moves = Orderer.legal_moves_list(hyp_board)

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

    def search(self, board, eval_func, depth=2, alpha=-np.inf, beta=np.inf):
        """
        Search finds the best guaranteed board within a certain depth.

        It looks a certain ply deep and evaluates the score at that position.
        Using minimax, black tries to minimize and white maximize. The function
        searches recursively and searches depth first. This implementation of
        search can be extremely slow because the number of boards to be
        evaluated roughly grows approximately by 30^N, where N is the number of
        ply deep being searched. Since 2-ply is required even to look one move
        into the future, this grows extremely quickly, even looking 1 move deep
        requires evaluating 900 positions.

        Arguments
        ---------
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: how many ply deep the search goes.

        Returns
        -------
        best_move: A tuple with the best move and associated score.
        """
        white = True
        best_move = None
        if depth == 0 or board.is_game_over():
            return (None, eval_func(board))

        legal_moves = self.orderer.order_search(board)

        if board.turn is white:
            for move in legal_moves:
                board.push(move)
                _, value = self.search(board, eval_func, depth - 1)
                board.pop()
                if value > alpha:
                    alpha = value
                    best_move = move

                if self.pruner.should_prune(alpha, beta):
                    break

            return (best_move, alpha)

        else:
            for move in legal_moves:
                board.push(move)
                _, value = self.search(board, eval_func, depth - 1)
                board.pop()
                if value < beta:
                    beta = value
                    best_move = move

                if self.pruner.should_prune(alpha, beta):
                    break

            return (best_move, beta)
