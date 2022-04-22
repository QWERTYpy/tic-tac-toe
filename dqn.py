import random
import numpy as np
from collections import deque
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.optimizer_v1 import Adam
from tensorflow.python.keras.optimizer_v1 import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import tensorflow as tf
import os

tf.compat.v1.disable_eager_execution()

# state_size = 9  # число типов информации о состоянии
# action_size = 9  # число возможных действий
# batch_size = 32  # размер пакета для обучения нашей нейронной
# n_episodes = 100  # число эпизодов (раундов игры)
# output_dir = 'model_output/'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

class DQNAgent:
    def __init__(self):  # +
        self.output_dir = 'model_output/'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.n_episodes = 500
        self.batch_size =64

        self.state_size = 9
        self.action_size = 9
        self.memory = deque(maxlen=100)  # Двусторонняя очередь для хранения воспоминаний
        self.gamma = 0.95  # Скорость затухания
        self.epsilon = 1.0  # Доля исследовательских действий (100%)
        self.epsilon_decay = 0.995  # Коэффициент уменьшения e
        self.epsilon_min = 0.01  # Минимальное значение, до которого может уменьшиться доля исследовательских действий
        self.learning_rate = 0.001  # скорость стохастического градиентного спуска
        self.model = self._build_model()

    def _build_model(self):  # +
        model = Sequential()
        model.add(Dense(64, activation='relu', input_dim=self.state_size))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        #model.add(Dense(64, activation='relu'))
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
        minibatch = random.sample(self.memory, batch_size)   # случайного отбора данных batch_size
        for state, action, reward, next_state, done in minibatch:
            target = reward  # если достигнут конец
            if not done:
            #print(next_state)
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            # print(reward,'=',target)
            # print(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            #print(target_f)
            target_f[0][action-1] = target
            #print(state, next_state, '|',action,'|',target,'|',done,'|',np.argmax(target_f[0])+1,'\n',target_f)
            self.model.fit(state, target_f, epochs=1, verbose=0)
            #print(state, target_f)
            #self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, state):  # +
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])+1  # возвращает индекс максимального значения вдоль указанной оси

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)

"""
agent = DQNAgent(state_size, action_size)

# Код в листинге реализует взаимодействие нашего агента с окружением из библиотеки OpenAI Gym

for e in range(n_episodes):
    # state = env.reset() запускает эпизод со случайным начальным состоянием st
    # state = np.reshape(state, [1, state_size]) преобразующий столбец в строку
    done = False
    time = 0
    while not done:
        # env.render() отображающее игровое поле
        action = agent.act(state)  # Состояние st (state) передается методу act() агента,
        # который возвращает действие at (action)

        # next_state, reward, done, _ = env.step(action)
        # Действие at передается методу окружения step(), который возвращает следующее состояние st+1 (next_state),
        # текущее вознаграждение rt (reward) и логический флаг done
        reward = reward if not done else -10
        '''
        Если эпизод завершился (то есть переменная done получила значение True), переменной reward (вознаграждения) 
        присваивается отрицательное значение (-10). Это вынуждает агента досрочно завершить эпизод при потере контроля 
        над балансом шеста или перемещении тележки за пределы экрана. Если эпизод еще не завершился 
        (переменная done получила значение False), значение переменной reward увеличивается на единицу 
        за каждый дополнительный шаг в игре.
        '''
        next_state = np.reshape(next_state, [1, state_size])
        # Вызывается метод reshape, чтобы преобразовать next_state в строку, подобно тому, как в начале диапазона
        # было преобразовано состояние state
        '''
        Для сохранения всех аспектов текущего шага (состояния st, действия at, вознаграждения rt, следующего 
        состояния st+1 и флага done) вызывается метод remember() агента
        '''
        agent.remember(state, action, reward, next_state, done)
        '''
        Для подготовки к следующей итерации, представляющей шаг t + 1, next_state переписывается в state
        '''
        state = next_state
        # Если эпизод завершился, выводятся итоговые показатели, достигнутые в этом эпизоде
        if done:
            print("episode: {}/{}, score: {}, e: {:.2}".format(e, n_episodes-1, time, agent.epsilon))
        time += 1  # К счетчику шагов time прибавляется 1.
        '''
        Если длина списка, представляющего память агента, превысила размер пакета, вызывается метод train()
         агента для корректировки параметров его нейронной сети воспроизведением воспоминаний об игровом процессе
        '''
    if len(agent.memory) > batch_size:
        agent.train(batch_size)
        '''
        Через каждые 50 эпизодов вызывается метод save() агента, чтобы сохранить параметры модели нейронной сети
        '''
    if e % 50 == 0:
        agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")
"""