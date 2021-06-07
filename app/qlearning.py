import numpy as np
import random
# from keras.models import Sequential, load_model
# from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Dropout, Flatten
# from keras.optimizers import Adam
# from keras.backend import clear_session

from collections import deque

class Dqn:
    def __init__(self, board):
        self.board             = board



def main(strategy):
    clear_session()
    strategy      = strategy # 'random',  'qlearning',   'human'
    pre_trained   = True
    reverse_game  = True     # False -> Agent begin  
                             # True  -> Adverse player begin
    n_rows        = 6
    n_columns     = 7
    env           = Connect4(n_rows=n_rows, n_columns=n_columns)
    if pre_trained == False:
        epsilon   = .95
    else:
        epsilon   = 1 # old_epsilon
    epsilon_min   = 0.01      # au départ 0.01
    learning_rate = 0.001    # au départ 0.005

    trials        = 3000
    trial_len     = 21

    # updateTargetNetwork = 1000
    dqn_agent = DQN(mdl_with_conv=True, pre_trained=pre_trained, root_path=root_path)
    dqn_agent.train_long()

if __name__ == '__main__':
    strategy = 'qlearning' # 'random' OR  'qlearning'  OR   'human'
    main(strategy)