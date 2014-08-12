"""
Monte Carlo Tic-Tac-Toe Player

Author: John Liu
Date: 2014-29-Jun
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Predefined Constants:  EMPTY, PLAYERX, PLAYERO, and DRAW    

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player 
    by making random moves, alternating between players. The function 
    should return when the game is over. The modified board will contain
    the state of the game, so the function does not return anything.
    """
    whose_turn = player
    while board.check_win() == None:
        open_squares = board.get_empty_squares()
        next_move = random.randrange(len(open_squares))
        board.move(open_squares[next_move][0],open_squares[next_move][1],whose_turn)
        whose_turn = provided.switch_player(whose_turn)
            

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same 
    dimensions as the Tic-Tac-Toe board, a board from a completed game, 
    and which player the machine player is. The function should score the 
    completed board and update the scores grid. As the function updates 
    the scores grid directly, it does not return anything,
    """
    board_size = board.get_dim()

    for row in range(board_size):
        for col in range(board_size):
            if board.check_win() == player:
                if board.square(row,col) == player:
                    scores[row][col] += MCMATCH
                elif board.square(row,col) == provided.switch_player(player):
                    scores[row][col] -= MCOTHER
            elif board.check_win() == provided.switch_player(player):
                if board.square(row,col) == player:
                    scores[row][col] -= MCMATCH
                elif board.square(row,col) == provided.switch_player(player):
                    scores[row][col] += MCOTHER

                    
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function 
    should find all of the empty squares with the maximum score and randomly 
    return one of them as a (row, column) tuple.
    """
    empty_squares = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row,col) == provided.EMPTY:
                empty_squares.append((row,col))

    if len(empty_squares) == 0:
        return (0,0)
    
    max_score = -999
    for index in empty_squares:
        value = scores[index[0]][index[1]]
        if value > max_score:
                max_score = value
    
    best_squares = []
    for index in empty_squares:
        value = scores[index[0]][index[1]]
        if value == max_score:
            best_squares.append(index)

    best_index = random.randrange(len(best_squares))
    return best_squares[best_index]

                
def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. The function should use the Monte Carlo 
    simulation described above to return a move for the machine player in the 
    form of a (row, column) tuple.
    """
    scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
    for dummy_count in range(trials):
        play_board = board.clone()
        mc_trial(play_board,player)
        mc_update_scores(scores, play_board, player)
    
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY],
#                                           [provided.PLAYERO, provided.PLAYERO, provided.EMPTY],
#                                           [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]),
#              provided.PLAYERX, NTRIALS)
#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
