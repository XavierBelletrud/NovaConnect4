import numpy as np
from abc import ABC, abstractmethod

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Dropout, Flatten
from keras.optimizers import Adam
from keras.backend import clear_session


class Gamer(ABC):
    def __init__(self, board, value=1):
        self.board      = board
        self.value      = value


    @abstractmethod ## méthode abstraite doit être redéfinie dans les class filles
    def input_game(self):
       pass

class HumanGamer(Gamer):

    def input_game(self):
        choice = ""
        possible_choice = np.arange(0, self.board.get_nbcolumns())
        while type(choice) != int or choice not in possible_choice:
              
            try : 
                choice = int(input(f'Select a number between 1 and {self.board.get_nbcolumns()}: '))-1
                if choice in possible_choice:
                    return choice
                
            except ValueError: 
                print(f" choice must be integer between 1 to {self.board.get_nbcolumns()}") 

class CPUGamerRandom(Gamer):

    def input_game(self):
        choice = np.random.randint(0, self.board.get_nbcolumns()) 
        return choice
        


class CPUGamerRL(Gamer):

    def __init__(self, board, value:int=1, flag_train:bool=False,is_train_model:bool=True, model_weigth_path:str='', mdl_with_conv=True):
        Gamer.__init__(self, board, value)

        ## variable
        self.__learning_rate   = 0.001      # 0.005     0.001
        ##### POUR battle Fixer Epsilon petit pour prise decision
        self.__epsilon           = 1.0
        self.__epsilon_min       = 0.01
        self.__epsilon_decay     = 0.99985   ## Attention modif epsilon par actions .... ou par parties ....
        self.__gamma             = 0.95
        self.__tau               = .125

        self.mdl_with_conv       = mdl_with_conv
        self.__pre_trained       = False # False create convoltion.h5+pretrained.h5
        self.__model_weigth_path = model_weigth_path 
        self.__flag_is_train     = flag_train
        self.__is_train_model    = is_train_model
        self.strategy_replay     = 'trial'    # 'random'


        if self.mdl_with_conv:
            self.state_shape = (self.board.get_nblines(), self.board.get_nbcolumns(), 1)
        else:
            self.state_shape = self.board.get_nblines()*self.board.get_nbcolumns()

        ## Condition to create a target model
        cond_target = (self.__flag_is_train and self.__is_train_model)

        if self.__pre_trained==False:
            self.model            = self.create_model()
            if cond_target:
                self.target_model = self.create_model()
        else:
            filepath = self.__model_weigth_path# 
            self.model            = load_model(filepath, custom_objects=None, compile=True, options=None)

            if cond_target:
                self.target_model = load_model(filepath, custom_objects=None, compile=True, options=None)


    def create_model(self):
        model   = Sequential()

        ## add layers
        if self.mdl_with_conv:
            model.add(Conv2D(filters=16, kernel_size=3, padding='same', input_shape=self.state_shape, activation='relu'))
            model.add(MaxPool2D())
            model.add(Conv2D(filters=32, kernel_size=3, padding='same', activation='relu'))
            model.add(MaxPool2D())
            model.add(Dropout(0.2))
            model.add(Flatten())
            model.add(Dense(units=50, activation="relu"))
        else:
            model.add(Dense(units=50, input_dim=self.state_shape, activation="elu"))

        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(units=50, activation="relu"))

        model.add(Dense(units=self.board.get_nbcolumns(), activation="linear"))

        ## compile the model
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.__learning_rate),
                      metrics=["mean_squared_error"])
        model.summary()
        return model
        
    def input_game(self):
        if self.mdl_with_conv==True:
            current_state = np.reshape(self.board.grid, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
        else:
            current_state = self.board.grid.reshape(1,-1)
            
        choice = np.argmax(self.model.predict(current_state)[0])
        print("Qlearning model choice of column", choice+1)
        return choice 


    def act(self, state):
        self.__epsilon     *= self.__epsilon_decay
        self.__epsilon      = max(self.__epsilon_min, self.__epsilon)

        if np.random.random() < self.__epsilon:
            return np.random.randint(0, self.board.get_nbcolumns())
            print(state)
        if self.mdl_with_conv:
            state      = np.reshape(state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
        else: 
            state = state.reshape(1,-1)
        prediction = np.argmax(self.model.predict(state)[0])## à changer lorsque l'adverse joue
        return prediction


    def replay_random(self, memory, batch_size:int=32):

        if len(memory) < batch_size: 
            return

        samples = random.sample(memory, batch_size)

        for sample in samples:
            state, action, reward, new_state, done = sample
            if self.mdl_with_conv:
                state = np.reshape(state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
                new_state = np.reshape(new_state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
            
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future          = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.__gamma
            history               = G2.model.fit(state, target, epochs=1, verbose=0)
            return history.history['mean_squared_error']


    def replay(self, memory):

        for sample in memory:

            state, action, reward, new_state, done = sample
            # print(state)
            if self.mdl_with_conv:
                state = np.reshape(state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
                new_state = np.reshape(new_state, (1, self.board.get_nblines(), self.board.get_nbcolumns(), 1))
            
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:

                Q_future          = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.__gamma
            history               = self.model.fit(state, target, epochs=1, verbose=0)
            return history.history['mean_squared_error']


    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.__tau + target_weights[i] * (1 - self.__tau)
        self.target_model.set_weights(target_weights)


    def adverse_train(self, G2):
        adverse_weights = G2.model.get_weights()
        weights = self.model.get_weights()
        for i in range(len(adverse_weights)):
            weights[i] = adverse_weights[i] * self.__tau + weights[i] * (1 - self.__tau)
        self.model.set_weights(weights)


    def save_model(self, path:str):
        self.model.save(path)
