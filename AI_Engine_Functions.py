# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025

@author: Clarke Merritt

Purpose: Create a Chessbot 
"""
# Imports
import chess
import re

white = True
black = False


def current_material(board):
    """
    This function calculates the current material score. It uses common scoring
    values — pawn: 1, knight: 3, bishop: 3.2, rook: 5, queen: 9.
    
    It takes one argument:
    board: the current board space.
    
    It returns:
    A tuple where ther first position is the white material score and the second
    is the black material score.
    """
    state = board.epd()
    white_score = state.count('P') + 3*state.count('N') + 3.2*state.count('B') + 5*state.count('R') + 9*state.count('Q')
    black_score = state.count('p') + 3*state.count('n') + 3.2*state.count('b') + 5*state.count('r') + 9*state.count('q')
    scores = (white_score,black_score)
    return scores

def current_space(board):
    """
    This function calculates the current space control. It scores space based 
    on the number of opponent squares that can currently be moved to.
    
    It takes one argument:
    board: the current board space.
    
    It returns:
    An integer which indicates how much space the current player controls.
    """
    hyp_board = board.copy()
    
    # Creates a list of strings containing all the current legal moves
    legal_moves = ''.join([i.uci() for i in hyp_board.generate_legal_moves()])
    result=''
    # Removes the starting squares so that only the end squares remain
    for i in range(2, len(legal_moves), 4):
        result += legal_moves[i:i+2]  # take 2 characters, skip 2
    
    """
    Checks which color the current player is. This is necessary to know what 
    rows are owned by the oppononent.
    """
    if hyp_board.turn == white:
        opponent_rows = ["5","6","7","8"]
    else:
        opponent_rows = ["1","2","3","4"]
    score = sum(result.count(moves) for moves in opponent_rows)
    return score
    
def current_pawnchain(board):
    """
    This function calculates the current number of pawn chains. 
    
    It takes one argument:
    board: the current board space.
    
    It returns:
    An integer which indicates how many pawn chains the current player has.
    """
    hyp_board = board.copy()
    
    # Checks the color of the current player
    if hyp_board.turn == white:
        C = 'P'
    else:
        C = 'p'
    
    # Numerical notation of pawn squares
    pawn_squares_num = [square for square, piece in hyp_board.piece_map() if piece == chess.Piece.from_symbol(C)]
    
    # String notation of pawn squares
    pawn_loc = ''.join([chess.square_name(i) for i in pawn_squares_num])

def score_pos(board, depth, weights=[1,1,1]):
    """
    This function scores a position. It scores based on 4 categories — material,
    development, squares controlled, king safety, etc.
    
    It takes three arguments:
    board: The current board space.
    depth: How many moves ahead should be calculated.
    weights:  
    
    It returns:
    A numerical score of the position, where 0 means it is equal, a negative
    means it favors black, and a positive means it favors white.
    """
    
    # Makes a copy of the board so the function does not change the true board.
    hyp_board = board.copy()
    # Creates a list of strings containing all the current legal moves
    legal_moves = [i.uci() for i in hyp_board.legal_moves]