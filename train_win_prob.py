import numpy as np
import tensorflow

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD, Adam

DELIMITER = ":"
WIN_PROB_SAVE_PATH = 'win_prob_model/'
WIN_PROB_FINAL_SAVE_PATH = 'win_prob_model_final/'

def train_win_prob(filename):
    inputs = []
    outputs = []

    with open(filename, 'r') as infile:
        for row in infile:
            line = row.strip().split(DELIMITER)
            inputs.append([float(n) for n in line[0].split(',')])
            outputs.append([float(n) for n in line[1].split(',')])

    x_train = np.matrix(inputs)
    y_train = np.matrix(outputs)

    # set the topology of the neural network
    # last loss: 2.3071e-05
    model = Sequential([
        Dense(units=25, input_dim=x_train.shape[1], activation='relu'),
        Dense(units=50, activation='relu'),
        Dense(units=100, activation='relu'),
        Dense(units=y_train.shape[1], activation='linear')
    ])

    # set up optimizer
    opt = Adam(learning_rate=0.0005)
    model.compile(optimizer=opt, loss='mean_squared_error')

    # train
    model.fit(x=x_train, y=y_train, epochs=800, batch_size=3000)
    return model

def load():
    model = keras.models.load_model(WIN_PROB_SAVE_PATH)
    return model

def save(model):
    model.save(WIN_PROB_SAVE_PATH)

if __name__ == '__main__':
    win_prob_filename = 'win_prob_data.dat'
    win_prob_model = train_win_prob(win_prob_filename)
    save(win_prob_model)
