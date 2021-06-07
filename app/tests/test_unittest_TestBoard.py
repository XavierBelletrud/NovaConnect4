# import unittest
# import sys, numpy as np
# sys.path.append("..")
# from board import Board

# class TestBoard(unittest.TestCase):
#     def setUp(self):
#         self.b = Board(6, 7)

#     def test_board_is_instance_of_board(self):
#         self.assertIsInstance(self.b, Board)

#     def test_board_not_null(self):
#         self.assertIsNotNone(self.b)

#     def test_board_is_nbcolumns_positive(self):
#         self.assertGreater(self.b.get_nbcolumns(), 0)

#     def test_board_is_nblines_positive(self):
#         self.assertGreater(self.b.get_nblines(), 0)

# if __name__ == '__main__':
#     unittest.main()

import unittest
import sys, numpy as np
import os

# print(os.getcwd())
# print("*"*40)
# print("sys.path", sys.path)
# print("*"*40)
sys.path.append(os.getcwd())
print("sys.path", sys.path)

#sys.path.insert(len(sys.path)+1, os.getcwd()+"/app")

from app.board import Board
from app.game import Game

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board(6, 7)

    def test_board_is_instance_of_board(self):
        self.assertIsInstance(self.b, Board)

    def test_board_not_null(self):
        self.assertIsNotNone(self.b)

    def test_board_is_nbcolumns_positive(self):
        self.assertGreater(self.b.get_nbcolumns(), 0)

    def test_board_is_nblines_positive(self):
        self.assertGreater(self.b.get_nblines(), 0)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.g = Game("hxh")

    def test_game_is_connect_an_int(self):
        self.assertIsInstance(self.g.connect, int)

    def test_game_is_connect2_an_int(self):
        self.assertIsInstance(self.g.nblines_int, int)

    def test_game_choicePlay(self):
        self.assertIsInstance(self.g.choice_play(), int)

if __name__ == '__main__':
    unittest.main()
