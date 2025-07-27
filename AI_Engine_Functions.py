# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025.

@author: Prior_Bayes

Purpose: Create a Chessbot
"""


# Functions
def fen_to_space(board):
    """
    Convert a FEN to have one character for each space on the board.

    Arguments
    ---------
    board : the current board position.

    Returns
    -------
    board_fen: a string of the current board position, where a char represents
               each square.
    """
    board_fen = board.fen()
    for i in range(1, 9):
        board_fen = board_fen.replace(str(i), '-'*i)
    return board_fen
