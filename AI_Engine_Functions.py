# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025

@author: Prior_Bayes

Purpose: Create a Chessbot 
"""
# Imports
import chess
import re
import numpy as np

class ChessEngine:
    """
    This class provides a base set of functions that may apply to all chess 
    engines.
    
    """
    
    white = True
    black = False
    
    @staticmethod
    def legal_moves_list(board):
        hyp_board = board.copy()
        legal_moves = [i.uci() for i in hyp_board.legal_moves]
        return legal_moves
   
    
    #def find_move(board, eval_func, depth=4, deep_search='None'):
        """
        This function calculates the best move based on the position evaluation
        function. Any position evaluation function can be passed to it. Find_move
        assumes the current player is the player to optimize winning chances for.
        
        It takes four arguments:
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: the amount of moves deep the engine searches.
        deep_search: the function which selects which lines should go beyond the depth.
        
        It returns:
        A list of tuples of the top five move choices and their associated scores.
        """        
        """
        hyp_board = board.copy()
        
        # The moves to be considered
        candidate_moves = ChessEngine().legal_moves_list(hyp_board)
        # This is a list that records how many move turns deep each move is
        move_depth = [0.5]*len(candidate_moves)
        """
        """ 
        This function can analyze arbitrarily deep by using a move stack. With this
        approach, we keep two lists: a list of moves to analyze and the current
        analysis depth of each of the aforementioned moves. For each move in the
        move list, 
        """
        
        """
        while candidate_moves:
            if move_depth[-1] == depth:
        """       
    
    def search(self, board, eval_func, depth=4):
        """
        This function evaluates the best score that can be achieved from the current
        position using a recursive minimax search up to a given depth.

        It takes three arguments:
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: how many ply deep the search goes.

        It returns:
        A numerical score for the current position.
        """
        hyp_board = board.copy()

        if depth == 0 or hyp_board.is_game_over():
            return eval_func(hyp_board)

        legal_moves = ChessEngine().legal_moves_list(hyp_board)

        if hyp_board.turn == ChessEngine.white:
            best_value = -np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                value = ChessEngine().search(hyp_board, eval_func, depth - 1)
                best_value = max(best_value, value)
                hyp_board.pop()
            return best_value
        else:
            best_value = np.inf
            for move in legal_moves:
                hyp_board.push_uci(move)
                value = ChessEngine().search(hyp_board, eval_func, depth - 1)
                best_value = min(best_value, value)
                hyp_board.pop()
            return best_value
                
        
    
    def minimax(board_node, eval_func):
        """
        This function finds the maximum value move for one full turn cycle.
        It assumes the opponent plays optimally (according to the evaluation
        function. It returns the maximum value move and the value for the
        current player.
        
        It takes four arguments:
        board_node: a hypothetical board state that could be reached..
        
        It returns:
        A tuple where the best move is first and the score is second.
        """    
        hyp_board = board_node.copy()
        legal_moves= ChessEngine().legal_moves_list(board_node)
        
        scores = []
        
        # This layer of for loop scores all of the current player's moves - MAX
        for move in legal_moves:
            hyp_board.push_san(move)
            opp_legal_moves = ChessEngine().legal_moves_list(hyp_board)
            
            # This is a list of the scores after the opponent makes each move
            response_scores = []
            
            # This layer of for loop scores all of the opponent's moves - MIN
            for opp_move in opp_legal_moves:
                hyp_board.push_san(opp_move)
                response_scores.append(eval_func(hyp_board))
                hyp_board.pop()
            # We assume the opponent makes the best move, which is the move the minimizes the score
            scores.append(min(response_scores))
            hyp_board.pop()
            
        # Return the best move and associated maximum score value
        best_move = (legal_moves[scores.index(max(scores))], max(scores))

        return best_move
                    
    @staticmethod
    def current_material(board):
        """
        This function calculates the current material score. It uses common scoring
        values — pawn: 1, knight: 3, bishop: 3.2, rook: 5, queen: 9.
        
        It takes one argument:
        board: the current board space.
        
        It returns:
        A tuple where the first position is the white material score and the second
        is the black material score.
        """
        state = board.epd()
        white_score = (state.count('P')
                      + 3*state.count('N')
                      + 3.2*state.count('B')
                      + 5*state.count('R')
                      + 9*state.count('Q'))
        black_score = (state.count('p')
                      + 3*state.count('n')
                      + 3.2*state.count('b')
                      + 5*state.count('r')
                      + 9*state.count('q'))
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
        if hyp_board.turn == ChessEngine().white:
            opponent_rows = ["5","6","7","8"]
        else:
            opponent_rows = ["1","2","3","4"]
        score = sum(result.count(moves) for moves in opponent_rows)
        return score
    
    def current_development(board):
        """
        This function calculates the current piece development. It scores 
        development based on whether the current square is the same as the starting
        square.
        
        It takes one argument:
        board: the current board space.
        
        It returns:
        An integer which shows how much more developed the current player is
        compared to the opponent.
        """
        hyp_board = board.copy()
        
        
        
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
        if hyp_board.turn == ChessEngine().white:
            C = 'P'
        else:
            C = 'p'
        
        # Numerical notation of pawn squares
        pawn_squares_num = [square for square, piece in hyp_board.piece_map().items() if piece == chess.Piece.from_symbol(C)]
        
        # String notation of pawn squares
        pawn_loc = ''.join([chess.square_name(i) for i in pawn_squares_num])
        pawn_loc = re.sub(r'\d+', '', pawn_loc)  # Remove all digits from the string
        pawn_loc = ''.join(sorted(pawn_loc))     # Sorts the columns alphabetically
        
    
    def score_pos(self, board, weights=[1, 0.5]):
        """
        This function scores a position. It scores based on 4 categories — material,
        development, squares controlled, king safety, etc.
        
        It takes two arguments:
        board: The current board space.
        weights: The relative value of different points
        
        It returns:
        A numerical score of the position, where 0 means it is equal, a negative
        means it favors black, and a positive means it favors white.
        """
        w,b = ChessEngine().current_material(board)
        return weights[0]*(w-b)
    