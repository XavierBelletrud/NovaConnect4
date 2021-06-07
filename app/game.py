import numpy as np
import pandas as pd
from app.gamer import HumanGamer, CPUGamerRandom, CPUGamerRL
from app.board import Board
from app.qlearning import Dqn
from collections import deque

class Game():
    """
    objets : joueurs,  interface d'affichage 
    attribut : plateau, type de joueur
    methode : vérification ligne, colonne, diagonale ; player_input ; global_player(42 coups)

    Principe de gravité (les colonnes se remplissent)


    is_board_full
    is_col_full

    """

    def __init__(self, gamechoice:str=None, nblines:int=6, nbcolumns:int=7, flag_train:bool=False, *args, **kwargs):
        
        # # if arguments are passed in a dictionnary  ### A DEBUG ###
        # if kwargs!={}:
        # gamechoice = kwargs.get('<gamechoice>', None)
        # nblines    = kwargs.get('<nblines>', 6)
        # nbcolumns  = kwargs.get('<nbcolumns>', 7)

        self.connect             = 4
        self.nblines_int         = int(nblines)
        self.nbcolumns_int       = int(nbcolumns)
        self.board               = Board(self.nblines_int, self.nbcolumns_int)
        self.mdl_with_conv       = False
        self.flag_running        = True
        self.__root_path         = './app/models/' 
        if self.mdl_with_conv:
            self.__model_name    = "convolution.h5"
        else:
            self.__model_name    = "denselayers.h5"     ## 'model_test.h5'
        self.__model_weigth_path = self.__root_path + self.__model_name
        self.__winner            = 0  #privated
        if gamechoice==None:
            self.gamechoice      = self.choice_play()
        else:
            self.gamechoice      = gamechoice

        self.__strategy          = 'RL' ## 'RL' 'random'
        self.__flag_is_train     = flag_train

        self.__init_gamer()           

        self.__idx_player        = 0
        self.possible_values     = [1, -1]
        self.cur_player          = self.G1
        self.adv_player          = self.G2

        if self.__flag_is_train:
            self.memory            = deque(maxlen=2000)
            self.__batch_size      = 32
            self.strategy_adverse  = 'qlearning'

    def reset(self):
        '''Reset the board.'''
        self.board.reset_board()
        self.__winner        = 0  #privated


    def __init_gamer(self):
        if self.gamechoice=='hxh':
            print("<---Initialize game Human Vs Human--->")
            self.G1 = HumanGamer(board=self.board, value=1)
            self.G2 = HumanGamer(board=self.board, value=-1)

        
        elif self.gamechoice=='hxr':
            print("<---Initialize game Human Vs Ia--->")

            self.G1 = HumanGamer(board=self.board, value=1)

            if self.__strategy=='random':
                self.G2 = CPUGamerRandom(board=self.board, value=-1)

            if self.__strategy=='RL':
                self.G2 = CPUGamerRL(board=self.board, value=-1, flag_train=self.__flag_is_train, is_train_model=True, model_weigth_path=self.__model_weigth_path, mdl_with_conv=self.mdl_with_conv)
            
        elif self.gamechoice=='rxr':
            print("<---Initialize game Ia Vs Ia--->")
            if self.__strategy=='random':
                self.G1 = CPUGamerRandom(board=self.board, value=1)
                self.G2 = CPUGamerRandom(board=self.board, value=-1)

            if self.__strategy=='RL':
                self.G1 = CPUGamerRL(board=self.board, value=1, flag_train=self.__flag_is_train, is_train_model=False, model_weigth_path =self.__model_weigth_path, mdl_with_conv=self.mdl_with_conv)
                self.G2 = CPUGamerRL(board=self.board, value=-1, flag_train=self.__flag_is_train, is_train_model=True, model_weigth_path =self.__model_weigth_path, mdl_with_conv=self.mdl_with_conv)
            
            
        else :
            print("None valid choice")


    def change_player(self):
        """
            -------------
            DESCRIPTION :   Permute players when called
            -------------  
        """
        ## value to add
        self.__idx_player = [0, 1][[0, 1].index(self.__idx_player)-1] ## permutation of players
        n_player  = self.possible_values[self.__idx_player]

        if n_player == 1:
            self.cur_player = self.G1
            self.adv_player = self.G2
        if n_player == -1:
            self.cur_player = self.G2
            self.adv_player = self.G1


    def choice_play(self):
        choice = 0
        
        while type(choice) != str or choice not in ['hxh', 'hxr', 'rxr']:
              
            try : 
                choice = input('Choose your game: \n hxh: Player 1 Vs Player 2 \n hxr: Player 1 Vs Bot \n rxr: Bot Vs Bot \n')
                if choice in ['hxh', 'hxr', 'rxr']:
                    return choice
                
            except ValueError: 
                #raise TypeError(" choice must be integer")
                print(" choice must be integer")
        

    def display_board(self):
        """
        DOCSTRING: Display the board
        """
        # liste zero
        liste_zero = np.arange(1, self.nblines_int+1)
        #liste name colonnes
        name       = ['c'+ str(i+1) for i in range(self.nbcolumns_int)]
        grid_df    = pd.DataFrame(self.board.grid, columns=name, index=liste_zero)
        return print(grid_df)


    def __is_col_full(self, column:int):
        if 0 not in self.board.grid[:,column]:
            return True
        else:
            return False


    def __col_choice(self, choice:int):
        """
        DOCSTRING: Inserting a coin into a col
        """
    
        if self.__is_board_full():
            return -2
        elif self.__is_col_full(choice):
            print(f'Column {choice} full')
            return -1
        else:
            column = self.board.grid[:,choice]
            for i in range(0, self.nblines_int)[::-1]:
                if column[i] == 0:
                    column[i] = self.cur_player.value
                    break
            return i


    def __is_board_full(self):
        """
        DOCSTRING: 
        """
        return 0 not in self.board.grid[0]

    
    def __check_col(self, choice:int, line:int):
        flag_win = False
        column   = self.board.grid[:,choice]
        if np.all(column[line:line+4] == self.cur_player.value) and len(column[line:line+4]) == 4:
            self.__winner  = self.cur_player.value
            flag_win       = True
            print("self.__winner  col:", self.__winner)
        return flag_win


    def __check_line(self, choice:int, line:int):
        flag_win = False
        window   = [self.cur_player.value] * self.connect
       
        test     = np.convolve(self.board.grid[line, max(0, choice-3):choice+4], window)
        # print(self.cur_player.value, test)
        if self.connect in test:
            self.__winner  = self.cur_player.value
            flag_win       = True
            print("self.__winner  line:", self.__winner)

        return flag_win

    def __check_diag(self, choice:int, line:int):
        flag_win     = False
        window       = [self.cur_player.value] * self.connect

        board_padded = np.pad(self.board.grid, (3, 3))
        m8           = board_padded[line-3+3:line+4+3, choice-3+3:choice+4+3]
    
        d1           = np.diag(m8)
        d2           = np.diag(m8[::-1])

        # Test connect 4 in diag 1
        test_diag1   = np.convolve(d1, window)
        if self.connect in test_diag1:
            flag_win = True
            self.__winner  = self.cur_player.value
            print("self.__winner :", self.__winner)

            return flag_win

        # Test connect 4 in diag 2
        test_diag2   = np.convolve(d2, window)
        if self.connect in test_diag2:
            flag_win = True
            self.__winner  = self.cur_player.value
            print("self.__winner :", self.__winner)

            return flag_win

        return flag_win


    def __check_diago(self):
        flag_win     = False
        row = 2
        column = 3
        column1 = column - 3
        gagnant = 0
        # une fenetre de 4x4 , on calucle les 2 diagonales
        # des que l'on trouve, on fait un break

        sum_diag1 = 0
        sum_diag2 = 0

        for k in range(3):
            # la matrice se déplace sur la verticale  vers la l'haut
            for j in range(4) :
                     # la matrice se déplace sur l'horisontal vers la droite

                sum_diag1 = sum([self.board.grid[row+i-k,column-i+j] for i in range(4)])
                sum_diag2 = sum([self.board.grid[row+i-k,column1+i+j] for i in range(4)])
                if (sum_diag1 == self.cur_player.value*4 or sum_diag2 == self.cur_player.value*4):
                    flag_win = True
                    self.__winner  = self.cur_player.value
                    print("self.__winner :", self.__winner)
                    
                    return flag_win

        return flag_win

    def play(self, choice:int, value:int):
        """
        DOCSTRING: 
        """
        # if board is None:
        #     board = self.board

        line     = self.__col_choice(choice) # Shall we play ?
        
        # Test if column is full or board is full
        if line < 0:
            if line==-1:
                return self.board.grid, -2*20, False
            return line
        
        # Connect4 test on col
        flag_win = self.__check_col(choice, line)
        if flag_win:
            return self.board.grid, value*20, True
    
        # Connect4 test on line
        flag_win = self.__check_line(choice, line)
        if flag_win:
            return self.board.grid, value*20, True #2
        
        # Connect4 test on diag
        flag_win = self.__check_diago()
        if flag_win:
            return self.board.grid, value*20, True
        
        return self.board.grid, 0, False


    def run(self):
        while self.flag_running==True:
            self.game_play()
            continu = ''
            while continu not in ['y', 'n']:
                continu = input("Do you want to play another party ? (y/n)")
            if continu=='n':
                self.flag_running=False
            self.change_player()
            self.reset()

    def game_play(self):
        
        self.display_board()
        nbr_turn = (self.nblines_int * self.nbcolumns_int) / 2
      
        while self.__is_board_full()==False:
            
            self.change_player()
            choice     = self.cur_player.input_game()  
            while self.__is_col_full(choice):
                choice = self.cur_player.input_game() 

            self.play(choice, self.cur_player.value)
          
            self.display_board()
            if self.__winner != 0 :
                print("bingo winner", self.cur_player.value)
                break
    

    def play_one(self, value:int, player, board=None):
        if board is None:
            board = self.board.grid

        action = player.act(board)
        return self.play(action, value), action


    def remember(self, state, action:int, reward:int, new_state, done:bool):
        self.memory.append([state, action, reward, new_state, done])


    def train_long(self, trials:int=10):
        steps         = []
        # loss          = []
        # n_played_game = []
        # n_win_game    = []
        # n_lose_game   = []
        # r_win_game    = []
        # n_win         = 0
        # n_lose        = 0

        for trial in range(trials):
            # Reset board 
            self.reset()
            # Modify who begin the game 
            if trial % 2 == 0:
                pass
            else:
                self.change_player()

            if self.G2.mdl_with_conv==False:
                cur_state = self.board.grid.reshape(1,-1)
            else:
                cur_state = self.board.grid

            step, reward = self.train(cur_state)

            # if trial % 10 == 0:
            print(f"Completed trials {trial} in {step+1} steps. Result : {reward}")
            self.G2.save_model(self.__model_weigth_path)
            # n_played_game.append(trial+1)
            # if reward==20:
            #     n_win  += 1
            # elif reward==-20:
            #     n_lose += 1
            # n_win_game.append(n_win)
            # n_lose_game.append(n_lose)
            # r_win_game.append(n_win / (trial+1))


    def train(self, cur_state):
        if self.G2.strategy_replay=='trial':
            self.memory.clear()

        for step in range(int(self.board.get_nblines()*self.board.get_nbcolumns()/2)):
            
            if self.G2.mdl_with_conv==True:
                cur_state      = np.reshape(cur_state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))


            ## Coup 1 joueur 
            step_return, action   = self.play_one(self.cur_player.value, self.cur_player)
            ## Test if the board is full
            if (step_return==-2):
                break
            else:
                new_state, reward, done = step_return
                if done == True:
                    break
                       
            ## Coup l'autre joueur
            self.change_player()
            step_return , adv_action   = self.play_one(self.cur_player.value, self.cur_player)
            # Test if the board is full
            if (step_return==-2):
                break
            else:
                new_state, reward, done = step_return
                if done == True:
                    break

            self.change_player()

            # # reward = reward if not done else -20
            if self.G2.mdl_with_conv==False:
                new_state = new_state.reshape(1,-1)
            self.remember(cur_state, action, reward, new_state, done)
            
            ## Replay strategy choice
            if self.G2.strategy_replay=='random':
                error = self.G2.replay_random(self.memory, self.__batch_size) # internally iterates default (prediction) model
            elif self.G2.strategy_replay=='trial':
                error = self.G2.replay(self.memory) # internally iterates default (prediction) model
            else:
                print('Error: Unknown replay strategy')

            # print(error)
            # loss.append(error)
            self.G2.target_train()        # iterates target model
            if self.strategy_adverse =='qlearning':
                self.G1.adverse_train(self.G2)   # iterates adverse model

            cur_state = new_state
            if done:
                break
        return step, reward   



    
