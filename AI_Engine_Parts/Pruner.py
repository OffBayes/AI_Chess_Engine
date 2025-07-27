# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:39:35 2025

@author: Prior_Bayes
"""


class Pruner:
    """
    Prunes leaves on the search tree.

    Methods
    -------
    should_prune: Determine whether a tree should be pruned.
    """

    def should_prune(self, alpha, beta):
        """
        Determine whether a tree should be pruned.

        By default, it is set to False. Other implementations use some logic to
        determine pruning logic.
        """
        return False


class AlphaBetaSearch(Pruner):
    """
    AlphaBetaSearch seeks to improve the search efficiency by pruning.

    It specifically uses alpha-beta pruning to reduce the number of moves to be
    considered. Alpha-beta pruning allows you to skip analyzing certain move
    trees if you already know the opponent can force a worse position than
    another move.
    """

    def should_prune(self, alpha, beta):
        """
        Determine if pruning should occur.

        Alpha beta pruning occurs if alpha >= beta

        Arguments
        ---------
        alpha: Current alpha value
        beta: Current beta value

        Returns
        -------
        to_prune: True if pruning should occur, False otherwise
        """
        to_prune = False
        if alpha >= beta:
            to_prune = True
        return to_prune