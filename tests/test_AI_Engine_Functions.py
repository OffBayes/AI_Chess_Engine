# -*- coding: utf-8 -*-
"""
Created on Fri May 30 23:58:45 2025

@author: Prior_Bayes
"""

import pytest
import chess
import AI_Engine_Functions as AI

# Useful Postions
starting_position = chess.Board()
empty_board = chess.Board(fen='8/8/8/8/8/8/8/8')
stalemate = chess.Board(fen='3k4/3P4/3K4/8/8/8/8/8 b')
checkmate = chess.Board(fen='rnb1kbnr/ppppp1pp/5p2/8/5PPq/8/PPPPP2P/RNBQKBNR w')
end_game = chess.Board(fen='8/8/8/8/8/5k2/7P/7K w - - 0 1')
castling = chess.Board(fen='4k2r/8/8/8/8/8/8/R3K2R w KQk - 0 1')
forced = chess.Board(fen='rnb1kbnr/ppppp1pp/5p2/8/5P1q/2N5/PPPPP1PP/R1BQKBNR w')
queens = chess.Board(fen='qqqqqqqq/rrrrrrrr/8/8/8/8/RRRRRRRR/QQQQQQQQ')


class TestLegalMovesList:
    def test_empty(self):
        assert AI.legal_moves_list(empty_board) == []

    def test_stalemate(self):
        assert AI.legal_moves_list(stalemate) == []

    def test_checkmate(self):
        assert AI.legal_moves_list(checkmate) == []

    def test_endgame(self):
        eng_moves = set(AI.legal_moves_list(end_game))
        moves = set(["h1g1", "h2h3", "h2h4"])
        assert eng_moves ^ moves == set()

    def test_castling(self):
        eng_moves = set(AI.legal_moves_list(castling))
        moves = set(["e1c1", "e1g1"])
        assert moves - eng_moves == set()

    def test_forced(self):
        assert AI.legal_moves_list(forced) == ["g2g3"]


class TestHeuristicEval:
    # Testing Current Material
    def test_current_material_empty(self):
        assert AI.HeuristicEval.current_material(empty_board) == (0, 0)

    def test_current_material_end_game(self):
        assert AI.HeuristicEval.current_material(end_game) == (1, 0)

    def test_current_material_queens(self):
        assert AI.HeuristicEval.current_material(queens) == (112, 112)

    def test_current_material_starting(self):
        score = AI.HeuristicEval.current_material(starting_position)
        assert score == (39.4, 39.4)

    # Testing Current Space
    # def 1