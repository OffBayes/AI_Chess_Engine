# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 23:47:03 2025

@author: Clarke
"""

import chess
from .HeuristicEval import HeuristicEval


class BBHeuristicEval(HeuristicEval):
    """
    BBHeuristicEval optimizes HeuristicEval using BitBoard operations.

    Traditional heuristics include material count, squares controlled, piece
    development, pawn structure, king safety, etc.

    Methods
    -------
        current_material: calculatest the material score of the position.
        current_space: calculates the number of opponent's squares controlled.
        current_development: counts the number of pieces developed.
        current_pawnshain: counts the number of pawn-cahins.

    """

    def pawn_control_squares(self, board: chess.Board, color: bool):
        """
        Returns a bitboard of squares controlled by pawns of the given color.
        Includes diagonal influence even if no capture is possible.
        """
        pawns = board.pieces(chess.PAWN, color)
        attacks = 0
        direction = 8 if color == chess.WHITE else -8

        for square in pawns:
            # Left diagonal
            if chess.square_file(square) > 0:
                attacks |= chess.BB_SQUARES[square + direction - 1]
            # Right diagonal
            if chess.square_file(square) < 7:
                attacks |= chess.BB_SQUARES[square + direction + 1]
        return attacks

    def current_material(self, board: chess.Board) -> tuple:
        white_score = 0
        black_score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP,
                           chess.ROOK, chess.QUEEN]:

            white_pieces = chess.popcount(board.pieces(
                piece_type, chess.WHITE))
            black_pieces = chess.popcount(board.pieces(
                piece_type, chess.BLACK))

            white_score += white_pieces * PIECE_VALUES[piece_type]
            black_score += black_pieces * PIECE_VALUES[piece_type]

        return (white_score, black_score)

    def current_space(self, board: chess.Board) -> tuple:
        color = board.turn
        territory = BB_WHITE_TERRITORY if color else BB_BLACK_TERRITORY
        white_score = 0
        black_score = 0

        # Non-pawn pieces
        piece_mask = board.occupied_co[color] & ~board.pieces_mask(chess.PAWN, color)
        while piece_mask:
            sq = chess.square_msb(piece_mask)
            attacks = board.attacks(sq)
            total_score += chess.popcount(attacks & territory)
            piece_mask &= piece_mask - 1

        # Pawns
        for sq in board.pieces(chess.PAWN, color):
            attacks = board.attacks(sq)
            total_score += chess.popcount(attacks & territory)

        return total_score