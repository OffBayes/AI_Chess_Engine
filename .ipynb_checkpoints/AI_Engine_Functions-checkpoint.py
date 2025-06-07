# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025

@author: Clarke Merritt

Purpose: Create a Chessbot 
"""
# Imports
import chess
white = True
black = False

board = chess.Board()

def current_material(board):
    """
    This function calculates the current material score. It uses common scoring
    values — pawn: 1, knight: 3, bishop: 3.2, rook: 5, queen: 9.
    
    It takes one argument:
    arg1: board.
    
    It returns:
    A tuple where ther first position is the white material score and the second
    is the black material score.
    """
    state = board.epd()
    white_score = state.count('P') + 3*state.count('N') + 3.2*state.count('B') + 5*state.count('R') + 9*state.count('Q')
    black_score = state.count('p') + 3*state.count('n') + 3.2*state.count('b') + 5*state.count('r') + 9*state.count('q')
    scores = (white_score,black_score)
    return scores
    
    
    
def score_pos():
    """
    This function scores a position. It scores based on 4 categories — material,
    development, squares controlled, king safety, etc.
    
    It takes two arguments:
    arg1: Description of the first argument.
    arg2: Description of the second argument.
    
    It returns:
    A numerical score of the position, where 0 means it is equal, a negative
    means it favors black, and a positive means it favors white.
    """
