import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import adam_v2 as Adam
import os

state_size = 9  # число типов информации о состоянии
action_size = 9  # число возможных действий
batch_size = 32  # размер пакета для обучения нашей нейронной
n_episodes = 1000  # число эпизодов (раундов игры)
output_dir = 'model_output/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Двусторонняя очередь для хранения воспоминаний
        self.gamma = 0.95  # Скорость затухания
        self.epsilon = 1.0  # Доля исследовательских действий (100%)
        self.epsilon_decay = 0.995  # Коэффициент уменьшения e
        self.epsilon_min = 0.01  # Минимальное значение, до которого может уменьшиться доля исследовательских действий
        self.learning_rate = 0.001  # скорость стохастического градиентного спуска
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=self.state_size))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
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

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward # если достигнут конец
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)

