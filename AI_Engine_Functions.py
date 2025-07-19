# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 20:19:46 2025.

@author: Prior_Bayes

Purpose: Create a Chessbot
"""
# Imports
import chess
import chess.polyglot
import re
import numpy as np

white = True


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

# Classes
class Orderer:
    def legal_moves_list(self, board):
        """
        Legal_moves_list takes the moves generator and returns a list of moves.

        Arguments
        ---------
        board : the current board position.

        Returns
        -------
        legal_moves : A list of legal moves.
        """
        legal_moves = [i.uci() for i in board.legal_moves]
        return legal_moves

    def order_search(self, board):
        """
        Determine the order of moves to be searched.

        Arguments
        ---------
        board: the current board state.

        Returns
        -------
        search_order: a list ordered by the search order.
        """
        return self.legal_moves_list(board)


class GreedyOrder(Orderer):
    """
    An orderer which traverses the tree by looking at best options first.

    It inherits from Orderer.
    """

    def order_search(self, board, eval_func):
        """
        Determine the order of moves to be searched.

        This function determines the search order by evaluating the current
        score of each position. The move it checks first at each tree is the
        move which provides the best immediate value.

        Arguments
        ---------
        board: the current board state.
        eval_func: the function which scores a given position.

        Returns
        -------
        search_order: a list ordered by the search order.
        """
        unsorted_legal_moves = self.legal_moves_list(board)
        legal_move_scores = [(eval_func(move), move)
                             for move in unsorted_legal_moves]
        return sorted(legal_move_scores, reverse=board.Turn)


class Pruner:
    """
    Prunes leaves on the search tree.

    Methods
    -------
    should_prune: Determine whether a tree should be pruned.
    """

    def should_prune(self, alpha, beta):
        """
        Determine whether a tree should be pruned.

        By default, it is set to False. Other implementations use some logic to
        determine pruning logic.
        """
        return False


class ChessEngine:
    """
    A customizable chess engine.

    ChessEngine allows users to configure the engine's behavior by supplying
    different components at initialization time. ChessEngine requires a search
    engine and evaluation engine to create an object. These engines determine
    the logic used to determine what move to make.
    """

    def __init__(self, search, evaluation, pruner=Pruner):
        """
        Initialize the engine with specific components.

        Arguments
        ---------
            search: The engine's search component.
            evaluation: The engine's board evaluation component.
        """
        self.searchEng = search
        self.evalEng = evaluation
        self.white = True
        self.black = False
        self.depth = 4

    def evaluate(self, board):
        """Return the evaluation score of the given board."""
        return self.evalEng.score_pos(board)

    def find_best_move(self, board, depth):
        """Use the composed search engine to find the best move."""
        hyp_board = board.copy()
        return self.searchEng.search(hyp_board, self.evaluate, depth)


class SearchEng:
    """
    A customizable search engine that allows different search approaches.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.
    """

    def __init__(self, pruner, orderer):
        """
        Initialize the search engine with a pruner and orderer.

        Arguments
        ---------
        pruner : The search engine's pruning component.
        orderer : The search engine's move ordering component.'
        """
        self.pruner = pruner
        self.orderer = orderer

    def minimax(self, board_node, eval_func):
        """
        Minimax finds the maximum value move for one full turn cycle (two ply).

        It assumes the opponent plays optimally (according to the evaluation
        function. This function minimizes the score for black and maximizes it
        for white.

        Arguments
        ---------
        board_node: a hypothetical board state that could be reached.

        It returns:
        best_move: A tuple with the best move and associated score.
        """
        hyp_board = board_node.copy()
        legal_moves = Orderer.legal_moves_list(board_node)

        scores = []

        # This layer of for loop scores all of the current player's moves - MAX
        for move in legal_moves:
            hyp_board.push_san(move)
            opp_legal_moves = Orderer.legal_moves_list(hyp_board)

            # This is a list of the scores after the opponent makes each move
            response_scores = []

            # This layer of for loop scores all of the opponent's moves - MIN
            for opp_move in opp_legal_moves:
                hyp_board.push_san(opp_move)
                response_scores.append(eval_func(hyp_board))
                hyp_board.pop()
            # Assume opponent makes best move by minimizes the score
            scores.append(min(response_scores))
            hyp_board.pop()

        # Return the best move and associated maximum score value
        best_move = (legal_moves[scores.index(max(scores))], max(scores))

        return best_move

    def search(self, board, eval_func, depth=2, alpha=-np.inf, beta=np.inf):
        """
        Search finds the best guaranteed board within a certain depth.

        It looks a certain ply deep and evaluates the score at that position.
        Using minimax, black tries to minimize and white maximize. The function
        searches recursively and searches depth first. This implementation of
        search can be extremely slow because the number of boards to be
        evaluated roughly grows approximately by 30^N, where N is the number of
        ply deep being searched. Since 2-ply is required even to look one move
        into the future, this grows extremely quickly, even looking 1 move deep
        requires evaluating 900 positions.

        Arguments
        ---------
        board: the current board space.
        eval_func: the function which scores a given position.
        depth: how many ply deep the search goes.

        Returns
        -------
        best_move: A tuple with the best move and associated score.
        """
        white = True
        best_move = None
        if depth == 0 or board.is_game_over():
            return (None, eval_func(board))

        legal_moves = self.orderer.order_search(board)

        if board.turn is white:
            for move in legal_moves:
                board.push_uci(move)
                _, value = self.search(board, eval_func, depth - 1)
                board.pop()
                if value > alpha:
                    alpha = value
                    best_move = move

                if self.pruner.should_prune(alpha, beta):
                    break

            return (best_move, alpha)

        else:
            for move in legal_moves:
                board.push_uci(move)
                _, value = self.search(board, eval_func, depth - 1)
                board.pop()
                if value < beta:
                    beta = value
                    best_move = move

                if self.pruner.should_prune(alpha, beta):
                    break

            return (best_move, beta)


class AlphaBetaSearch(Pruner):
    """
    AlphaBetaSearch seeks to improve the search efficiency by pruning.

    It specifically uses alpha-beta pruning to reduce the number of moves to be
    considered. Alpha-beta pruning allows you to skip analyzing certain move
    trees if you already know the opponent can force a worse position than
    another move.
    """

    def should_prune(self, alpha, beta):
        """
        Determine if pruning should occur.

        Alpha beta pruning occurs if alpha >= beta

        Arguments
        ---------
        alpha: Current alpha value
        beta: Current beta value

        Returns
        -------
        to_prune: True if pruning should occur, False otherwise
        """
        to_prune = False
        if alpha >= beta:
            to_prune = True
        return to_prune


class EvalEng:
    """
    EvalEng represents the chess engine evaluation capability.

    This class allows users to configure the engine's behavior by supplying
    different components at initialization time.

    Methods
    -------
        score_pos: Checks whether subclass has implemented scoring function.
    """

    def score_pos(self, board):
        """
        score_pos scores a position to see which player has the advantage.

        It

        """
        raise NotImplementedError("Subclasses must implement score_pos")

    def pawn_control_squares(self, board, color):
        """
        Return list of controlled squares.

        Returns a list of squares that are controlled by pawns of the given
        color, even if there are no pieces to capture (i.e., includes diagonal
        influence).

        Arguments
        ---------
            board: a python-chess Board object.
            color: chess.WHITE or chess.BLACK

        Returns
        -------
        - A list of controlled square names (e.g., ["e4", "f5", "e4"])
        """
        controlled = []
        direction = 1 if color == chess.WHITE else -1

        for square in board.pieces(chess.PAWN, color):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            for df in [-1, 1]:
                f = file + df
                r = rank + direction
                if 0 <= f <= 7 and 0 <= r <= 7:
                    target_square = chess.square(f, r)
                    controlled.append(chess.square_name(target_square))
        return controlled

class HeuristicEval(EvalEng):
    """
    HeuristicEval attempts to evaluate the position using chess heuristics.

    Traditional heuristics include material count, squares controlled, piece
    development, pawn structure, king safety, etc.

    Methods
    -------
        current_material: calculatest the material score of the position.
        current_space: calculates the number of opponent's squares controlled.
        current_development: counts the number of pieces developed.
        current_pawnshain: counts the number of pawn-cahins.

    """

    def current_material(self, board):
        """
        Calculate the current material score.

        This function calculates the current material score. It uses common
        scoring values — pawn: 1, knight: 3, bishop: 3.2, rook: 5, queen: 9.

        It takes one argument:
        board: the current board state.

        It returns:
        A tuple where the first position is the white material score and the
        second is the black material score.
        """
        state = board.board_fen()
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
        scores = (white_score, black_score)
        return scores

    def current_space(self, board):
        """
        Calculate the current space control.

        This function calculates the current space control. It scores space
        based on the number of opponent squares that can currently be moved to
        or a pawn could move to if a piece was there.

        It takes one argument:
        board: the current board state.

        It returns:
        A tuple where the first position is the white space score and the
        second is the black space score.
        """
        score = []
        for color in ['white', 'black']:
            if color == 'white':
                board.turn = True
                opponent_rows = ["5", "6", "7", "8"]
            else:
                board.turn = False
                opponent_rows = ["1", "2", "3", "4"]

            # Generate pseudo-legal moves, excluding all pawn moves
            legal_moves = ''.join([
                move.uci()
                for move in board.generate_pseudo_legal_moves()
                if board.piece_type_at(move.from_square) != chess.PAWN
            ])

            result = ''

            # Removes the starting squares so that only the end squares remain
            for i in range(2, len(legal_moves), 4):
                result += legal_moves[i:i+2]  # take 2 characters, skip 2

            # Adds the squares pawns can control
            pawn_controls = self.pawn_control_squares(
                board, board.turn)
            result += ''.join(pawn_controls)

            score.append(sum(result.count(moves) for moves in opponent_rows))
        score = tuple(score)
        return score

    def current_development(self, board):
        """
        Calculate the current development.

        This function calculates the current piece development. It scores
        development based on whether the current square is the same as the
        starting square.

        Arguments
        ---------
        board: the current board space.

        Returns
        -------
        development: the number of developed pieces
        """
        start_pos = fen_to_space(chess.Board()).split(' ')[0]
        start_pos = start_pos.split('/')
        curr_pos = fen_to_space(board).split(' ')[0]
        curr_pos = curr_pos.split('/')
        white_start_rows = "".join(start_pos[6:8])
        white_curr_rows = "".join(curr_pos[6:8])
        black_start_rows = "".join(start_pos[0:2])
        black_curr_rows = "".join(curr_pos[0:2])

        white_moved = sum([1 for white_start_rows, white_curr_rows in
                           zip(white_start_rows, white_curr_rows)
                           if white_start_rows != white_curr_rows])
        black_moved = sum([1 for black_start_rows, black_curr_rows in
                           zip(black_start_rows, black_curr_rows)
                           if black_start_rows != black_curr_rows])
        white_taken = 16 - sum([1 for char in "".join(curr_pos)
                                if char.isupper()])
        black_taken = 16 - sum([1 for char in "".join(curr_pos)
                                if char.islower()])
        development = (white_moved - white_taken, black_moved - black_taken)
        return development


    """
        def current_pawnisland(self, board):
    ###
            Current_pawnchain calculates the current number of pawn chains.

            Arguments
            ---------
            board: the current board space.

            Returns
            -------
            chain_num: An integer representing the pawn chain number.
    ###

            # Numerical notation of pawn squares
            pawn_squares_num = ([square for square, piece
                                 in board.piece_map().items()
                                 if piece == chess.Piece.from_symbol(C)])

            # String notation of pawn squares
            pawn_loc = ''.join([chess.square_name(i) for i in pawn_squares_num])
            # Remove all digits from string
            pawn_loc = re.sub(r'\d+', '', pawn_loc)
            # Sorts the columns alphabetically
            pawn_loc = ''.join(sorted(pawn_loc))
    """

    def score_pos(self, board, weights=[1, 0.2, 0.2]):
        """
        Scores a position.

        It scores based on multiple categories:
        material, development, squares controlled, king safety, etc.

        It takes two arguments:
        board: The current board space.
        weights: The relative value of different points

        It returns:
        A numerical score of the position, where 0 means it is equal, a
        negative means it favors black, and a positive means it favors
        white.
        """
        white_mat, black_mat = self.current_material(board)
        white_spac, black_spac = self.current_space(board)
        white_dev, black_dev = self.current_development(board)
        if board.is_checkmate():
            score = -np.inf if board.turn else np.inf
        else:
            score = (weights[0] * (white_mat - black_mat)
                     + weights[1] * (white_spac - black_spac)
                     + weights[2] * (white_dev - black_dev))
        return score


# board.push_san(eng.find_best_move(board, depth=2)[0])
