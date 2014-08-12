"""
Mini-max Tic-Tac-Toe Player

Author: John Liu
Date: 2014-30-Jul
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winflag = board.check_win()
    if winflag != None:
        return SCORES[winflag], (-1,-1)
    empty_sq = board.get_empty_squares()
    subscore = [0 for dummy_i in range(len(empty_sq))]
    for idx in range(len(empty_sq)):
        newboard = board.clone()
        newboard.move(empty_sq[idx][0],empty_sq[idx][1],player)
        subscore[idx] = mm_move(newboard,provided.switch_player(player))[0]
        subscore[idx] *= SCORES[player]
    topscore = max(subscore)
    topmove = empty_sq[subscore.index(topscore)]
    return topscore * SCORES[player], topmove

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


#board = provided.TTTBoard(3)
#board.move(0,0,provided.PLAYERX)
#board.move(1,1,provided.PLAYERO)
#board.move(1,0,provided.PLAYERX)
#board.move(0,1,provided.PLAYERO)
#board.move(0,2,provided.PLAYERX)
#board.move(2,0,provided.PLAYERO)
#print board
#print mm_move(board,provided.PLAYERO)