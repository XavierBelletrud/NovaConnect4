import sys
sys.path.append("../") #marche quand je me trouve dans tests

import numpy as np
#from board import Board
import board, game
from game import *
from gamer import *

def test_board_size():
    b = Board(6, 7)
    assert b.grid.shape == (b.get_nblines(), b.get_nbcolumns())
    #assert 1 == 1

def test_grid():
    b = Board(20, 10)
    assert type(b) != None

# def test_input_game():
#     g = HumanGamer.input_game()
#     assert g == int


#     assert type(b.grid) == "<class 'numpy.ndarray'>"

# def test_display_board():
#         b = game.
#         g = game.Game()
#         assert type(g.display_board()) == "<class 'numpy.ndarray'>"

#def test_is_col_full():