import numpy as np
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
        self.n_episodes = 5000
        self.batch_size =64
        self.obuch = 0

        self.state_size = 9
        self.action_size = 9
        self.memory = deque(maxlen=50)  # Двусторонняя очередь для хранения воспоминаний
        self.gamma = 0.95  # Скорость затухания
        self.epsilon = 0.01  # Доля исследовательских действий (100%)
        self.epsilon_decay = 0.995  # Коэффициент уменьшения e
        self.epsilon_min = 0.01  # Минимальное значение, до которого может уменьшиться доля исследовательских действий
        self.learning_rate = 0.001  # скорость стохастического градиентного спуска
        self.model = self._build_model()

    def _build_model(self):  # +
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=self.state_size))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):  # +
        """

        :param state: Состояние st (state), встретившееся агенту
        :param action: Действие at (action), предпринятое агентом
        :param reward: Вознаграждение rt (reward), которое вернуло окружение в ответ на действие
        :param next_state: Следующее состояние st+1 (next_state), которое вернуло окружение
        :param done: Логический флаг done, который получает значение True, если достигнут последний временной шаг
                в эпизоде, и False в ином случае.
        :return:
        """
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):  # +-
        for state, action, reward, next_state, done in self.memory:
            target = reward  # если достигнут конец
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action-1] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, state):  # +
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])+1  # возвращает индекс максимального значения вдоль указанной оси

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)

