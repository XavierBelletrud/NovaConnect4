import numpy as np

class Gamer():

    
    """
    attributs : identification, couleur, nom ou numéro 1 et -1
    methode : faire un choix de colonne

    
    
    joueur_humain(joueur)
    faire un choix de colonne(input)

    joueur_bot(joueur)
    faire un choix de colonne, 2 choix : random ou IA
    """

    def __init__(self, numero, couleur):
        self.numero = numero
        self.couleur = couleur
        #self.choicePlay = choicePlay
        # self.choice = choice


    

    def choicePlay(self):
           
            choice = int(input('Choose your game: \n 1: Player1 Vs Player2 \n 2: Player1 VS Bot \n 3: Bot VS Bot \n'))
            #if self.choice == 1:
            return choice

class HumanGamer(Gamer):

    def input_humain(self):
        print(f" gamer {self.numero :}")
        choice = int(input('Select a number between 0 and 6: '))
        return choice 

class CPUGamer(Gamer):
    
    def input_CPU(self):
        choice = np.random.randint(0, 7) # random player choice
        return choice 







class Board():
    """
    objets : joueurs,  interface d'affichage 
    attribut : plateau, type de joueur
    methode : vérification ligne, colonne, diagonale ; player_input ; global_player(42 coups)

    Principe de gravité (les colonnes se remplissent)


    is_board_full
    is_col_full

    """

    def __init__(self):
        self.nblines_int = 6
        self.nbcolumns_int = 7
        self.board = np.zeros((self.nblines_int, self.nbcolumns_int), dtype=int)
        self.__gagnant = 0  #privated

    def displayBoard(self):
        """
        DOCSTRING: Display the board
        """
        board = self.board
        return print(board, "\n")

    def isColFull(self, column:int):
        if 0 not in self.board[:,column]:
            return True
        else:
            return False

    def colChoice(self, player:int, choice:int):
        """
        DOCSTRING: Inserting a coin into a col
        """
    
        if self.isBoardFull():
            return -2
        elif self.isColFull(choice):
            print(f'Column {choice} full')
            return -1
        else:
            column = self.board[:,choice]
            for i in range(0, self.nblines_int)[::-1]:
                if column[i] == 0:
                    column[i] = player
                    break
            return i


    def isBoardFull(self):
        """
        DOCSTRING: 
        """
        return 0 not in self.board[0]

    

    def its_your_turn(self, player, choice):
        """
        DOCSTRING: 
        """

        line = self.colChoice(player, choice) # Shall we play ?
        print("line :", line)
        if line < 0:
            return line
        
        # Connect4 test on col
        column = self.board[:,choice]
        if np.all(column[line:line+4] == player) and len(column[line:line+4]) == 4:
            return self.board, 1, True
    
        # Connect4 test on line
        window = [player] * 4
        test = np.convolve(self.board[line, max(0, choice-3):choice+4], window)
        if player*4 in test:
            return self.board, 1, True #2
        
        # Connect4 test on diag
        board_padded = np.pad(self.board, (3, 3))
        #m8 = self.board[max(0, line-4):line+4, max(0, choice-4):choice+4]
        m8 = board_padded[line-3+3:line+4+3, choice-3+3:choice+4+3]
    
        d1 = np.diag(m8)
        d2 = np.diag(m8[::-1])
      
        #
        test = np.convolve(d1, window)
        if player*4 in test:
            return self.board, 1, True #3
        
        #
        test = np.convolve(d2, window)
        if player*4 in test:
            return self.board, 1, True
        
    def  gamePlay(self):
        
        B.displayBoard()
        player = 1
        G = Gamer(player, 'rouge')
        gamechoice = G.choicePlay()
        nbr_turn = (self.nblines_int * self.nbcolumns_int) / 2
        #print(type(nbr_turn))
        for i in range(int( nbr_turn)) :
           
            if gamechoice == 1 or gamechoice == 2:
                # the first gamer is only humain
                G1 = HumanGamer(player, 'jaune')
                choice1 = G1.input_humain()
               
               
            if gamechoice == 3 :
               # the first and the seconde gamers are CPU
                G1 = CPUGamer(player,'jaune')
                choice1 = G1.input_CPU()
                
            
            #B.colChoice(1,choice1)
            B.its_your_turn(player, choice1)
            B.displayBoard()
            
           
           ######### move to the second player
           
            player = 2
            if gamechoice == 1 :
                # the second player are humain gamer
                G2  = HumanGamer(player, 'rouge')
                choice2 = G2.input_humain()
            if gamechoice == 2 or gamechoice ==3 :
                #the second gamer is a CPU gamer
                G2  = CPUGamer(player, 'rouge')
                choice2= G2.input_CPU()
           # B.colChoice(player,choice2)
           
            B.its_your_turn(player, choice2)
            B.displayBoard()
            player -=1
    


class Interface():
    """ terminal et graphique """
    pass




if __name__ == "__main__":
    B = Board()
    B.gamePlay()