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
