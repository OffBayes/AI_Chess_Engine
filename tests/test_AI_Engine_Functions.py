# -*- coding: utf-8 -*-
"""
Created on Fri May 30 23:58:45 2025

@author: Prior_Bayes
"""

import pytest
import chess
import AI_Engine_Parts as AI

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
fried_liver = chess.Board(
    fen='r1bqkb1r/ppp2Npp/2n5/3np3/2B5/8/PPPP1PPP/RNBQK2R b')


class TestFenToSpace:
    def setup_method(self):
        self.object = AI

    def test_fen_to_space_empty(self):
        board = '--------/' * 8
        board = board[:-1]
        assert board in self.object.fen_to_space(empty_board)

    def test_fen_to_space_stalemate(self):
        board = '---k----/---P----/---K----' + 5*'/--------'
        assert board in self.object.fen_to_space(stalemate)

    def test_fen_to_space_checkmate(self):
        board = 'rnb-kbnr/ppppp-pp/-----p--/--------/-----PPq/--------'
        board = board + '/PPPPP--P/RNBQKBNR'
        assert board in self.object.fen_to_space(checkmate)

    def test_fen_to_space_queens(self):
        board = 'qqqqqqqq/rrrrrrrr/' + 4*'--------/' + 'RRRRRRRR/QQQQQQQQ'
        assert board in self.object.fen_to_space(queens)


class TestOrderer:
    def setup_method(self):
        self.orderer = AI.Orderer()

    # Testing Legal Moves List
    def test_legal_moves_list_empty(self):
        assert self.orderer.legal_moves_list(empty_board) == []

    def test_legal_moves_list_stalemate(self):
        assert self.orderer.legal_moves_list(stalemate) == []

    def test_legal_moves_list_checkmate(self):
        assert self.orderer.legal_moves_list(checkmate) == []

    def test_legal_moves_list_endgame(self):
        eng_moves = set(self.orderer.legal_moves_list(end_game))
        moves = set(["h1g1", "h2h3", "h2h4"])
        assert eng_moves ^ moves == set()

    def test_legal_moves_list_castling(self):
        eng_moves = set(self.orderer.legal_moves_list(castling))
        moves = set(["e1c1", "e1g1"])
        assert moves - eng_moves == set()

    def test_legal_moves_list_italian(self):
        eng_moves = set(self.orderer.legal_moves_list(italian))
        moves = set(["a7a6", "a7a5", "b7b6", "b7b5", "d7d6", "d7d5", "f7f6",
                     "f7f5", "g7g6", "g7g5", "h7h6", "h7h5", "c6b8", "c6a5",
                     "c6b4", "c6d4", "c6e7", "a8b8", "d8e7", "d8f6", "d8g5",
                     "d8h4", "e8e7", "f8e7", "f8d6", "f8c5", "f8b4", "f8a3",
                     "g8e7", "g8f6", "g8h6"])
        assert eng_moves == moves

    def test_legal_moves_list_forced(self):
        assert self.orderer.legal_moves_list(forced) == ["g2g3"]

    # Testing Order Search
    def test_order_search(self):
        assert (self.orderer.legal_moves_list(italian)
                == self.orderer.order_search(italian))


class TestAttackOrder:
    def setup_method(self):
        self.orderer = AI.AttackOrder()

    def test_get_attackers_empty(self):
        assert self.get_attackers(empty_board) == []

    def test_get_attackers_stalemate(self):
        assert self.get_attackers(stalemate) == []

    def test_get_attackers_checkmate(self):
        assert self.get_attackers(checkmate) == []

    def test_get_attackers_italian(self):
        assert self.get_attackers(italian) == []

    def test_get_attackers_fried_liver(self):
        assert self.get_attackers(fried_liver) == 

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

    # Testing Current Development
    def test_current_development_empty(self):
        assert self.eval.current_development(empty_board) == (0, 0)

    def test_current_development_starting(self):
        assert self.eval.current_development(starting_position) == (0, 0)

    def test_current_development_stalemate(self):
        assert self.eval.current_development(stalemate) == (2, 1)

    def test_current_development_checkmate(self):
        assert self.eval.current_development(checkmate) == (2, 2)

    def test_current_development_end_game(self):
        assert self.eval.current_development(end_game) == (1, 1)

    def test_current_development_forced(self):
        assert self.eval.current_development(forced) == (2, 2)

    def test_current_development_italian(self):
        assert self.eval.current_development(italian) == (3, 2)