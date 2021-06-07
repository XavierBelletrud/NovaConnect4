import numpy as np
from board import Board

class MinMax:
    # init of minmax
    def __init__(self, board, bot, adverse_player):
        self.board          = board
        self.value          = 1
        self.bot            = bot
        self.adverse_player = adverse_player

    ## Checker
    def is_action_win(self, grid, player):
    
        #test de toutes les positions horizontales
        for c in range (self.board.get_nbcolumns()-3):
            for r in range (self.board.get_n_rows()):
                if grid[r][c]== player and grid[r][c+1]== player and grid[r][c+2]== player and grid[r][c+3]== player:            
                    return True
        
        #test de toutes les positions verticales
        for c in range (self.board.get_nbcolumns()):
            for r in range (self.board.get_n_rows()-3):
                if grid[r][c]== player and grid[r+1][c]== player and grid[r+2][c]== player and grid[r+3][c]== player:             
                    return True
        
        #test de toutes les positions diagonales orientées vers la droite
        for c in range (self.board.get_nbcolumns()-3):
            for r in range (self.board.get_n_rows()-3):
                if grid[r][c]== player and grid[r+1][c+1]== player and grid[r+2][c+2]== player and grid[r+3][c+3]== player:            
                    return True
        
        #test de toutes les positions diagonales orientées vers la gauche
        for c in range (self.board.get_nbcolumns()-3):
            for r in range (3,self.board.get_n_rows()):
                if grid[r][c]== player and grid[r-1][c+1]== player and grid[r-2][c+2]== player and grid[r-3][c+3]== player:            
                    return True

    ## Simulate addition of a pawn
    def __apply_one(self, grid, column, player):
        row               = self.board.get_n_rows() - self.__is_empty_box_in_column(grid, column)
        grid[row][column] = player 
        return grid

    #renvoie le nombre de cases libres dans une colonne
    def __is_empty_box_in_column(self, grid, column):
        result = 0
        for row in range(self.board.get_nblines()):
            if grid[row][column]==0:
                result +=1    
        return result    

    # Return the number of free box in a column
    def __exits_free_boxes_in_column(self, grid, column):
        result = 0
        for row in range(self.board.get_nbcolumns()):
            if grid[row][column]==0:
                result +=1    
        return result    

    # Is there an interesting box in a given direction?
    # Is it possible to align 4 pawns
    def __interest_boxes_in_direction(self, row, column, dx, dy, player):
        maxx = column+3*dx
        maxy = row+3*dy
        if (maxx >self.board.get_nbcolumns() - 1) or (maxx <0) or (maxy > self.board.get_nbrows() -1) or (maxy < 0):
            return 0
        else:
            if player == self.bot:
                adverse_player = self.adverse_player
            else:
                adverse_player = self.bot
            
            i=0
            # Boxes empty or occupied by the adverse player are interesting
            while (i<4) and (self.board.grid[row+i*dy][column+i*dx] != adverse_player):
                i+=1
            if i==4:
                return 1
            else:
                return 0


    #Is a box intersting, regarding in all directions?
    def __interest_of_box(self, row, column, player):
        result = self.__interest_boxes_in_direction(row, column, 1, 0, player) +\
                self.__interest_boxes_in_direction(row, column, 1, 1, player) +\
                self.__interest_boxes_in_direction(row, column, 0, 1, player) +\
                self.__interest_boxes_in_direction(row, column, 1, -1, player)+\
                self.__interest_boxes_in_direction(row, column, -1, 1, player) +\
                self.__interest_boxes_in_direction(row, column, -1, -1, player) 
        return result

    #For a given player the current board is interesting?
    def __interest_board(self, player):
        result = 0
        for column in range(self.board.get_nbcolumns()):
            for row in range(self.board.get_nbcols()):
                result += self.__interest_of_box(row, column, player)
                
        return result   

    # Interest of the board regarding the two players
    # The final value is the difference   
    def __terminal_value(self):
        return self.__interest_board(self.bot) - self.__interest_board(self.adverse_player)

    # Pacours of the Min Max Tree at a given deep
    def __minmax_value(self, grid, deep, is_max):
        win = self.is_action_win(grid, self.bot) 
        if win:
            return 10000
        win = self.is_action_win(grid, self.adverse_player)
        if win:
            return -10000
        if deep == 0:
            return self.__terminal_value()
        # Possible action of the bot at a given deep
        if is_max:
            #coup possible de l'ordinateur
            result = -10001

            #Pour chaque colonne du tableau à cette profondeur
            for column in range(self.board.get_nbcolumns()):
                if self.__exits_free_boxes_in_column(grid, column)>0:
                    # copy the board
                    grid2 = np.copy(grid)
                    # Calculate score at a given deep 
                    score = self.__minmax_value(self.__apply_one(grid2, column, self.bot), deep-1, False)                    
                    if score > result:
                        result = score
            return result
        else:
            # Possible action for the adverse player
            result = 10001
            for column in range(self.board.get_nbcolumns()):
                # For all column at a the given deep
                if self.__exits_free_boxes_in_column(grid, column)>0:
                    # copy the board
                    grid2 = np.copy(grid)
                    # Calculate score at a given deep 
                    score = self.__minmax_value(self.__apply_one(grid2, column, self.adverse_player), deep-1, True)

                    if score < result:
                        result = score
            return result

    # Find the optimal action for the Bot using Min Max algorithm
    def decision_minmax(self, deepmax):
        result = -1
        bscore = -10001
        for column in range(self.board.get_nbcolumns()):
            if self.__exits_free_boxes_in_column(self.board.grid, column)>0: 
                # Compute MinMax Value for all columns in the board
                grid2 = np.copy(self.board.grid)   

                score = self.__minmax_value(self.__apply_one(grid2, column, self.bot), deepmax, False)                    
                if score > bscore:
                    bscore = score
                    result = column
                    #print("score ", score, "col: ", column)
        
        return result


if __name__ == '__main__':
    n_rows    = 6
    n_columns = 7
    board     = Board(n_rows, n_columns)
    MinMax    = MinMax(board, 1, -1)
