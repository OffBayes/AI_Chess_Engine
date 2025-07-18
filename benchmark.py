# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 22:31:18 2025

@author: Clarke
"""

import time
import chess
import AI_Engine_Functions as AI

Eng = AI.ChessEngine(AI.SearchEng(), AI.HeuristicEval())
abEng = AI.ChessEngine(AI.AlphaBetaSearch(), AI.HeuristicEval())


def tictoc(func, arg1=None, arg2=None):
    """
    Tictoc measures how long a function takes to complete.

    Arguments
    ---------
    func: The function to be timed.
    arg1: The first argument of the function
    arg2: The second argument of the function

    Returns
    -------
    elapsed: The time passed.

    """
    if (arg1 is None) & (arg2 is None):
        t0 = time.perf_counter()
        func()
        t1 = time.t()
    elif (arg2 is None):
        t0 = time.perf_counter()()
        func(arg1)
        t1 = time.perf_counter()()
    else:
        t0 = time.perf_counter()()
        func(arg1, arg2)
        t1 = time.perf_counter()()

    elapsed = t1 - t0

    return elapsed

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
mateInTwo = chess.Board(
    fen='r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w')

useful_positions = [
    starting_position,
    stalemate,
    checkmate,
    end_game,
    castling,
    forced,
    italian,
    mateInTwo]

for pos in useful_positions:
    print(f"{pos=}", "/n",
          "Alpha-Beta Search: ", tictoc(abEng.find_best_move, pos, 4),
          "Default Search: ", tictoc(Eng.find_best_move, pos, 4))
