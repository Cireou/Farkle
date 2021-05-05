import numpy as np
import tensorflow

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD, Adam

DELIMITER = ":"
ACTION_SAVE_PATH = 'action_model/'
ACTION_FINAL_SAVE_PATH = 'action_model_final/'

def train_action(filename):
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
    # last loss: 0.0227
    model = Sequential([
        Dense(units=16, input_dim=x_train.shape[1], activation='relu'),
        Dense(units=64, activation='relu'),
        Dense(units=32, activation='relu'),
        Dense(units=y_train.shape[1], activation='sigmoid')
    ])

    # set up optimizer
    opt = Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

    # train
    model.fit(x=x_train, y=y_train, epochs=400, batch_size=1000)
    return model

def load():
    model = keras.models.load_model(ACTION_SAVE_PATH)
    return model

def save(model):
    model.save(ACTION_SAVE_PATH)

if __name__ == '__main__':
    action_filename = 'action_data.dat'
    action_model = train_action(action_filename)
    save(action_model)
