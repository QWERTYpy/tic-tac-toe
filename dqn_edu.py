import numpy as np
import random
from collections import deque
from tensorflow.python.keras.optimizer_v1 import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import tensorflow as tf
import os

tf.compat.v1.disable_eager_execution()


class DQNAgent:
    def __init__(self):  # +
        self.output_dir = 'model_output/'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.n_episodes = 3000
        self.batch_size =64

        self.state_size = 9
        self.action_size = 9
        self.memory = deque(maxlen=500)  # Двусторонняя очередь для хранения воспоминаний
        self.gamma = 0.95  # Скорость затухания
        self.epsilon = 1.0  # Доля исследовательских действий (100%)
        self.epsilon_decay = 0.995  # Коэффициент уменьшения e
        self.epsilon_min = 0.01  # Минимальное значение, до которого может уменьшиться доля исследовательских действий
        self.learning_rate = 0.001  # скорость стохастического градиентного спуска
        self.model = self._build_model()

    def _build_model(self):  # +
        model = Sequential()
        model.add(Dense(128, activation='relu', input_dim=self.state_size))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def train(self, name):
        f = open(name)
        state_mas = np.empty((0,9), int)
        target_mas = np.empty((0,9), int)
        for line in f:
            state, action, reward, next_state, done, _ = line.split(',')
            state = state.strip()
            state = state[2:-2]
            state = state.split()
            state = [int(x) for x in state]
            state = np.reshape(state, [1, agent.state_size])
            next_state = next_state.strip()
            next_state = next_state[2:-2]
            next_state = next_state.split()
            next_state = [int(x) for x in next_state]
            next_state = np.reshape(next_state, [1, agent.state_size])
            action = int(action.strip())
            reward = float(reward.strip())
            done = done.strip()
            target = reward  # если достигнут конец
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action-1] = target
            state_mas = np.append(state_mas, state, axis=0)
            target_mas = np.append(target_mas,target_f, axis=0)
            # state_mas.append(state)
            # target_mas.append(target_f)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs")
        self.model.fit(state_mas, target_mas, batch_size=200, epochs=1000, verbose=1, callbacks=[tensorboard_callback] )
        f.close()

    def act(self, state):  # +
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])+1  # возвращает индекс максимального значения вдоль указанной оси

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)


agent = DQNAgent()
# for _ in range(100):
#     print(_)
#     agent.train('txt_XO.txt')
agent.train('txt_XO_m.txt')
agent.save(agent.output_dir + "manual_test4.hdf5")
