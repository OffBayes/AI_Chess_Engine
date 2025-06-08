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
empty_board = chess.Board(
    fen='8/8/8/8/8/8/8/8')
stalemate = chess.Board(
    fen='3k4/3P4/3K4/8/8/8/8/8 b')
checkmate = chess.Board(
    fen='rnb1kbnr/ppppp1pp/5p2/8/5PPq/8/PPPPP2P/RNBQKBNR w')
end_game = chess.Board(
    fen='8/8/8/8/8/5k2/7P/7K w - - 0 1')
castling = chess.Board(
    fen='4k2r/8/8/8/8/8/8/R3K2R w KQk - 0 1')
forced = chess.Board(
    fen='rnb1kbnr/ppppp1pp/5p2/8/5P1q/2N5/PPPPP1PP/R1BQKBNR w')
queens = chess.Board(
    fen='qqqqqqqq/rrrrrrrr/8/8/8/8/RRRRRRRR/QQQQQQQQ')
italian = chess.Board(
    fen='r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b')


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
    def setup_method(self):
        self.eval = AI.HeuristicEval()

    # Testing Current Material
    def test_current_material_empty(self):
        assert self.eval.current_material(empty_board) == (0, 0)

    def test_current_material_end_game(self):
        assert self.eval.current_material(end_game) == (1, 0)

    def test_current_material_queens(self):
        assert self.eval.current_material(queens) == (112, 112)

    def test_current_material_starting(self):
        score = self.eval.current_material(starting_position)
        assert score == (39.4, 39.4)

    def test_current_material_italian(self):
        score = self.eval.current_material(italian)
        assert score == (39.4, 39.4)

    # Testing Current Space
    def test_current_space_empty(self):
        assert self.eval.current_space(empty_board) == (0, 0)

    def test_current_space_starting(self):
        assert self.eval.current_space(starting_position) == (0, 0)

    def test_current_space_stalemate(self):
        assert self.eval.current_space(stalemate) == (9, 0)

    def test_current_space_checkmate(self):
        assert self.eval.current_space(checkmate) == (4, 6)

    def test_current_space_end_game(self):
        assert self.eval.current_space(end_game) == (0, 8)

    def test_current_space_queens(self):
        assert self.eval.current_space(queens) == (24, 24)

    def test_current_space_forced(self):
        assert self.eval.current_space(forced) == (4, 7)

    def test_current_space_italian(self):
        assert self.eval.current_space(italian) == (9, 7)
