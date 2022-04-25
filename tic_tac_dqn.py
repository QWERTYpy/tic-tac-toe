import tic_tac_gui as ttg
import dqn
import numpy as np
import random


class TicTacDQN(ttg.TicTac):
    def _perebil_hod(self, actions):
        hod = self.game_field.copy()
        if hod[actions - 1]:
            return False
        hod[actions - 1] = 1
        _win = 0
        for el_win in self.win:
            for _ in el_win:
                _win += hod[_ - 1]
            if _win == 3:
                return True
            _win = 0

    def _reward(self, actions):
        """
        Функция вознаграждения
        :param actions:
        :return:
        """
        if self._perebil_hod(actions) and not self.win_xod[1]:
            return False, +2  # Если перебил ход
        if self.game_field[actions - 1]:
            self.osh += 1
            return True, -10  # Если неправильный ход
        if any(self.win_xod):
            if self.win_xod[0]:
                return True, -1  # Если проиграл
            if self.win_xod[1]:
                return True, 1  # ЕСли победил
            if self.win_xod[2]:
                return True, 1  # Если ничья

        return False, 0.5  # Если простой ход

    def education(self):
        """
        Функция обучения
        :return:
        """
        for epis in range(agent.n_episodes):
            print(self.osh)
            self.new_game()
            # Первый ход делает рандом
            state = self._random().copy()
            state = np.reshape(state, [1, agent.state_size])
            done = False
            time = 0
            while not done:
                if np.random.rand() <= agent.epsilon:
                    actions = random.randint(1, 9)
                    done, reward = self._reward(actions)
                else:
                    actions = agent.act(state)
                    done, reward = self._reward(actions)
                self.fun_moves_made(actions)
                hod_ai = self.game_field
                hod_ai = np.reshape(hod_ai, [1, agent.state_size])
                if not done:
                    next_state = self._random().copy()
                    next_state = np.reshape(next_state, [1, agent.state_size])
                    if self.win_xod[0]:
                        done = True
                        reward = -1
                    if self.win_xod[2]:
                        done = True
                        reward = 1
                    if self.win_xod[1]:
                        done = True
                else:
                    next_state = state

                agent.remember(state, actions, reward, hod_ai, done)
                state = next_state
                time += 1
                if done:
                    print("episode: {}/{}, score: {}, e: {:.2}".format(epis, agent.n_episodes - 1, time, agent.epsilon))
            #  Если длина списка, представляющего память агента, превысила размер пакета, вызывается метод train()

            if len(agent.memory) > agent.batch_size:
                #print(agent.batch_size, len(agent.memory))
                agent.train(agent.batch_size)
                '''
                Через каждые 50 эпизодов вызывается метод save() агента, чтобы сохранить параметры модели нейронной сети
                '''
            if epis % 50 == 0:
                agent.save(agent.output_dir + "weights_" + '{:04d}'.format(epis) + ".hdf5")

    def motion(self, event):
        """
        Функция определяющая позицию на игровом поле по координатам мышки
        :param event:
        :return:
        """
        if not any(self.win_xod):
            pos = 0
            x, y = event.x, event.y
            if 0 < y < 100:
                if 0 < x < 100: pos = 1
                if 100 < x < 200: pos = 2
                if 200 < x < 300: pos = 3
            if 100 < y < 200:
                if 0 < x < 100: pos = 4
                if 100 < x < 200: pos = 5
                if 200 < x < 300: pos = 6
            if 200 < y < 300:
                if 0 < x < 100: pos = 7
                if 100 < x < 200: pos = 8
                if 200 < x < 300: pos = 9
            if pos:
                self.fun_moves_made(pos)
            if self.init_type == 4 and not any(self.win_xod):
                pos = self.random_hod()
                self.fun_moves_made(pos)
            if self.init_type == 2 and not any(self.win_xod):
                state = self.game_field.copy()
                state = np.reshape(state, [1, agent.state_size])
                actions = agent.act(state)
                #print(actions)
                self.fun_moves_made(actions)

game = TicTacDQN()
if game.init_type == 3 or game.init_type == 2:
    agent = dqn.DQNAgent()

if game.init_type == 2:
    agent = dqn.DQNAgent()
    agent.load(agent.output_dir + "weights_1950.hdf5")
game.mainloop()
