# -*- coding: utf-8 -*-
"""
Created on Fri May 30 23:58:45 2025

@author: Prior_Bayes
"""

import pytest
import chess
import numpy as np
import AI_Engine_Functions as AI

# Useful Postions
empty_board = chess.Board(fen='8/8/8/8/8/8/8/8')
stalemate = chess.Board(fen='3k4/3P4/3K4/8/8/8/8/8 b')
checkmate = chess.Board(fen='rnb1kbnr/ppppp1pp/5p2/8/5PPq/8/PPPPP2P/RNBQKBNR w')


class TestLegalMoves:
    def test_empty(self):
        assert AI.legal_moves_list(empty_board) == []

    def test_stalemate(self):
        assert AI.legal_moves_list(stalemate) == []

    def test_checkmate(self):
        assert AI.legal_moves_list(checkmate) == []

