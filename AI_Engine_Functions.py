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
    A tuple where ther first position is the white space score and the second
    is the black space score.
    """
    hyp_board = board.copy()
    
    # Creates a list of strings containing all the current legal moves
    hyp_board.turn = white
    white_legal_moves = ''.join([i.uci() for i in hyp_board.legal_moves])
    result=''
    # Removes the starting squares so that only the end squares remain
    for i in range(0, len(white_legal_moves), 4):
        result += white_legal_moves[i:i+2]  # take 2 characters, skip 2
    
    white_score = legal_moves.count()
    
    hyp_board.turn = black
    black_legal_moves = ''.join([i.uci() for i in hyp_board.legal_moves])
    black_score = legal_moves.count()

    
def score_pos(board, depth):
    """
    This function scores a position. It scores based on 4 categories — material,
    development, squares controlled, king safety, etc.
    
    It takes two arguments:
    board: the current board space.
    depth: how many moves ahead should be calculated.
    
    It returns:
    A numerical score of the position, where 0 means it is equal, a negative
    means it favors black, and a positive means it favors white.
    """
    
    # Makes a copy of the board so the function does not change the true board.
    hyp_board = board.copy()
    # Creates a list of strings containing all the current legal moves
    legal_moves = [i.uci() for i in hyp_board.legal_moves]