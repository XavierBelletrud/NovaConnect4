import numpy as np

class Board:
    def __init__(self, nblines_int:int=6, nbcolumns_int:int=7):
        self.__nblines_int   = nblines_int
        self.__nbcolumns_int = nbcolumns_int
        self.grid            = np.zeros((self.__nblines_int, self.__nbcolumns_int), dtype=int)

    def get_nblines(self):
        return self.__nblines_int

    def get_nbcolumns(self):
        return self.__nbcolumns_int
    
    def reset_board(self):
        self.__init__(self.__nblines_int, self.__nbcolumns_int)
