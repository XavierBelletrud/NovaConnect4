#!/usr/bin/env python
"""
Test docopt
Usage:
    app.py
    app.py <gamechoice> [--train] [<trails>]
    app.py [<gamechoice>] [--train] [<trails>] --dim <nblines> <nbcolumns>
    app.py -H | --help
    app.py -V | --version

Options:
    -H --help              Show this screen.
    -V --version           Show version.
"""

#   --choice <gamechoice>  Choice of game type, hxh (Human Vs Human), hxr (Human Vs Bot), rxr (Bot Vs Bot)
from docopt import docopt
from app.game import Game
import sys
""" 
parametres : - game choice hxh hxb bxb
             - strategy : (choix du type de bot) 'random' ou 'RL' ou 'autre' si on y arrive
options    : - train (__flag is train)
             - battle

"""
def main():
    test = 1    # 1: Test fonction >>>  game_play()  <<<
                # 2: Test fonction >>>     run()     <<<
                # 3: Test fonction >>>  train_long() <<<

    ## Test game_play()
    if test==1:
        print("Test de la fonction game_play()")
        game = Game()
        game.game_play()
    ## Test run()
    elif test==2:
        print("Test de la fonction run()")
        game = Game()
        game.run()
    ## Test train_long
    elif test==3:
        game = Game(3, flag_train=True)
        game.train_long(1000)

if __name__ == '__main__':
    # main()
    
    args = docopt(__doc__, version='Connect 4 v1.0')
    print(args)
    if args=={}:
        game = Game()
    
    if args['--dim']==True:
        game = Game(gamechoice=args['<gamechoice>'], nblines=args['<nblines>'], nbcolumns=args['<nbcolumns>'], flag_train=args['--train'])
    else:
        game = Game(gamechoice=args['<gamechoice>'], flag_train=args['--train'])

    # game = Game(gamechoice=args['<gamechoice>'], nblines=args['<nblines>'], nbcolumns=args['<nbcolumns>'])
    # game = Game(**args)
    if args['<gamechoice>']=='rxr' and args['--train']:    

        if args['<trails>']!=None:
            game.train_long(trials=int(args['<trails>']))     
        else:
            game.train_long()   

    else:         
        game.run()
