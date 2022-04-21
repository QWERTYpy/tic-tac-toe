import tkinter as tk  # Для создания интерфейса пользователя
import tkinter.messagebox
from PIL import Image, ImageTk
import random
import dqn
import numpy as np


class TicTac:
    def __init__(self):
        """
        Проводим инициализацию игрового поля
        """
        self.image_P = Image.open("img/P.jpg")
        self.image_X = Image.open("img/X.jpg")
        self.image_O = Image.open("img/O.jpg")


        self.position = [[15, 115], [115, 115], [215, 115],
                    [15, 215], [115, 215], [215, 215],
                    [15, 315], [115, 315], [215, 315]]
        self.element = []  # Список из объектов канвы с X и O

        self.win = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                    [1, 5, 9],
                    [3, 5, 7],
                    [1, 4, 7],
                    [2, 5, 8],
                    [3, 6, 9]]

        self.win_xod = [0, 0, 0]  # Победа Х,О,Н
        self.game_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0- Пусто, 1-Х, -1-О
        # Информация из интрефейса управлния (пока отсутсвуют)
        self.init_type = 3  # 1 -> человек - человек, 2 -> человек - компьютер, 3 -> рандом - компьютер, 4 -> рандом - ч
        self.init_xo = True  # 1 - X, 0 - 0 кто первый

        self.flag_xo = self.init_xo  # True - X, False - 0 кто первый

        #self.moves_made = [self.init_xo]  # Создаем список со сделанными ходами. Первый элемент - выбор Х или О

        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.resizable(width=False, height=False)
        self.root.geometry('300x400+100+100')  # Создаем окно
        self.root.configure(background='#ffffff')
        self.canvas_P = tkinter.Canvas(self.root, height=300, width=300, highlightthickness=0)
        self.canvas_P.configure(background='#ffffff')
        self.image_P = self.image_P.resize((300, 300), Image.LANCZOS)
        self.photo_P = ImageTk.PhotoImage(self.image_P)
        self.image_P = self.canvas_P.create_image(0, 0, anchor='nw', image=self.photo_P)  # Создаем поле для игры
        self.canvas_P.place(x=0, y=100)
        if self.init_type != 3:
            self.canvas_P.bind('<Button-1>', self.motion)
        self.image_X = self.image_X.resize((70, 70), Image.LANCZOS)
        self.photo_X = ImageTk.PhotoImage(self.image_X)
        self.image_O = self.image_O.resize((70, 70), Image.LANCZOS)
        self.photo_O = ImageTk.PhotoImage(self.image_O)
        # self.label_coord = tk.Label(self.root, text=f'{moves_made}')
        # self.label_coord.place(x=10, y=10)

        self.label_player1 = tk.Label(self.root, text=f'Игрок 1 :')
        self.label_player1.place(x=10, y=10)
        self.label_player1.configure(background='#ffffff')

        self.label_player1_count = tk.Label(self.root, text=f'0')
        self.label_player1_count.place(x=80, y=10)
        self.label_player1_count.configure(background='#ffffff')

        self.label_player2 = tk.Label(self.root, text=f'Игрок 2 :')
        self.label_player2.place(x=10, y=40)
        self.label_player2.configure(background='#ffffff')

        self.label_player2_count = tk.Label(self.root, text=f'0')
        self.label_player2_count.place(x=80, y=40)
        self.label_player2_count.configure(background='#ffffff')

        self.label_draw = tk.Label(self.root, text=f'Ничья :')
        self.label_draw.place(x=10, y=70)
        self.label_draw.configure(background='#ffffff')

        self.label_draw_count = tk.Label(self.root, text=f'0')
        self.label_draw_count.place(x=80, y=70)
        self.label_draw_count.configure(background='#ffffff')

        self.mainmenu = tkinter.Menu(self.root)
        self.root.config(menu=self.mainmenu)
        self.mainmenu.add_command(label="Новая игра", command=self.new_game)

        if self.init_type == 3:
            self.mainmenu.add_command(label="Обучение", command=self.education)

        self.label_end = tk.Label(self.root, text='')
        self.label_end.place(x=140, y=40)
        self.label_end.configure(background='#ffffff')

        self.label_end_win = tk.Label(self.root, text='')
        self.label_end_win.place(x=220, y=40)
        self.label_end_win.configure(background='#ffffff')


    def player1_count(self):
        """
        Функция увеличивает количество побед игрока 1
        :return:
        """
        self.label_player1_count['text'] = int(self.label_player1_count['text']) + 1

    def player2_count(self):
        """
        Функция увеличивает количество побед игрока 2
        :return:
        """
        self.label_player2_count['text'] = int(self.label_player2_count['text']) + 1

    def draw_count(self):
        """
        Функция увеличивает количество ничьих

        :return:
        """
        self.label_draw_count['text'] = int(self.label_draw_count['text']) + 1

    def new_game(self):
        """
        Функция обнуляет игровое поле для новой игры

        :return:
        """

        # self.label_player1_count['text'] = 0
        # self.label_player2_count['text'] = 0
        #self.label_draw_count['text'] = 0
        for _ in self.element:
            _.destroy()
        self.element = []
        #self.moves_made = [1]
        self.flag_xo = self.init_xo
        self.label_end['text'] = ''
        self.label_end_win['text'] = ''
        self.win_xod = [0, 0, 0]
        self.game_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def _reward(self, actions):
        if self.game_field[actions-1]:
            return True, True, -1
        self.fun_moves_made(actions)
        if any(self.win_xod):
            if self.win_xod[0] or self.win_xod[2]:
                return False, True, -1
            if self.win_xod[1]:
                return True, True, 1

        return False, False, 0.5

    def _random(self):
        pos = self.random_hod()
        self.fun_moves_made(pos)
        return self.game_field

    def education(self):

        for e in range(agent.n_episodes):
            print('1')
            self.new_game()
            # Первый ход делает рандом
            state = self._random().copy()
            state = np.reshape(state, [1, agent.state_size])
            done = False
            time = 0
            while not done:
                #print('r', state)
                if np.random.rand() <= agent.epsilon:
                    actions = self.random_hod()
                    dubl, done, reward = self._reward(actions)
                    # print(state)
                    # print(agent.model.predict(state))
                    # print(agent.act(state))
                    # print('q')
                else:
                    actions = agent.act(state)
                    dubl, done, reward = self._reward(actions)
                #print(actions)
                if not dubl:
                    next_state = self._random().copy()
                    next_state = np.reshape(next_state, [1, agent.state_size])
                else:
                    next_state = state
                if self.win_xod[0] or self.win_xod[2]:
                    done = True
                    reward = -0.5
                #print(state, actions, reward, next_state, done)
                #print(len(agent.memory))
                agent.remember(state, actions, reward, next_state, done)
                #print(agent.memory)
                state = next_state
                time += 1
                if done:
                    print("episode: {}/{}, score: {}, e: {:.2}".format(e, agent.n_episodes - 1, time, agent.epsilon))
                #time += 1
            #  Если длина списка, представляющего память агента, превысила размер пакета, вызывается метод train()
            if len(agent.memory) > agent.batch_size:
                agent.train(agent.batch_size)
                '''
                Через каждые 50 эпизодов вызывается метод save() агента, чтобы сохранить параметры модели нейронной сети
                '''
            if e % 50 == 0:
                agent.save(agent.output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")

    def canva_create(self):
        """
        Функция создает канву для последующего размещения на ней игровго элемента
        :return:
        """
        #   self.image_X = self.canvas_X.create_image(0, 0, anchor='nw', image=self.photo_X)
        return tkinter.Canvas(self.root, height=70, width=70, highlightthickness=0)

    def canva_add_x(self, canva):
        """
        Функция размещает на канве X
        :param canva:
        :return:
        """
        canva.create_image(0, 0, anchor='nw', image=self.photo_X)

    def canva_add_o(self, canva):
        """
        Функция размещает на канве O
        :param canva:
        :return:
        """
        canva.create_image(0, 0, anchor='nw', image=self.photo_O)

    def print_canva(self, canva, x, y):
        """
        Функция устанавливает игровой элемент в нужную позицию
        :param canva:
        :param x:
        :param y:
        :return:
        """
        canva.place(x=x, y=y)

    def mainloop(self):
        """
        Запуск
        :return:
        """
        self.root.mainloop()

    def hod(self, elem, pos_xy):
        """
        Функция реализующая ход на игровом поле
        :param elem: Х или О
        :param pos_xy:  номер ячейки 1,2,3,4,5,6,7,8,9
        :return:
        """
        pos_x, pos_y = self.position[pos_xy - 1]  # Получаем координаты для размещения на канве нового эелемента
        self.element.append(self.canva_create())  # Создаем указатель на канву
        ind = len(self.element) - 1  # Получаем адрес указателя
        if elem == 'X':
            self.canva_add_x(self.element[ind])
        else:
            self.canva_add_o(self.element[ind])
        self.print_canva(self.element[ind], pos_x, pos_y)  # Размещаем элемент на канве

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
                print(actions)
                self.fun_moves_made(actions)



    def random_hod(self):
        while True:
            pos = random.randint(1, 9)
            if not self.game_field[pos-1]:
                return pos



    def fun_moves_made(self, pos):
        """
        Функция реализующая сам ход
        :param pos: 1,2,3,4,5,6,7,8,9
        :return:
        """
        # global moves_made

        # moves_made = [x for x, _ in self.moves_made[1:]]
        #if pos not in moves_made:
        if not self.game_field[pos-1]:
            #if self.moves_made[0] == 1:
            if self.flag_xo:
                self.hod('X', pos)
                #self.moves_made.append([pos, 'X'])
                self.game_field[pos-1] = 1
                #self.moves_made[0] = 0
                self.flag_xo = False
            else:
                self.hod('O', pos)
                #self.moves_made.append([pos, 'O'])
                self.game_field[pos-1] = -1
                #self.moves_made[0] = 1
                self.flag_xo = True
            self.root.update()
            # Проверка после совершенного хода на победу или ничью
        # if self.search_win_game('O') and not self.win_xod[2]:
        #     self.end_game('O')
        #     return True
        # if self.search_win_game('X') and not self.win_xod[2]:
        #     self.end_game('X')
        #     return True
        if self.search_end_game():
            self.end_game()
        # if self.win_xod[2]:
        #     self.end_game('=')
            #return True

    #def search_win_game(self, elem)
    def search_end_game(self):
        """
        Функция определяющая победу
        :return:
        """
        _win = 0
        for el_win in self.win:
            #if ([el_win[0], elem] in self.moves_made) and ([el_win[1], elem] in self.moves_made) and ([el_win[2], elem] in self.moves_made):
            for _ in el_win:
                _win += self.game_field[_-1]
            if _win**2 == 9:
                #if elem == 'X':
                if _win > 0:
                    self.win_xod = [1, 0, 0]
                #if elem == 'O':
                if _win < 0:
                    self.win_xod = [0, 1, 0]
                return True
            _win = 0
        #if len(self.moves_made) == 10:
        if all(self.game_field):
            self.win_xod = [0, 0, 1]
            return True
        return False

    def end_game(self):
        if any(self.win_xod[:2]):
            self.label_end['text'] = 'ПОБЕДИЛ :'
            if self.win_xod[0]:
                self.label_end_win['text'] = 'X'
            if self.win_xod[1]:
                self.label_end_win['text'] = 'O'
        if self.win_xod[2]:
            self.label_end['text'] = 'НИЧЬЯ'

        if self.win_xod[0]:
            self.player1_count()
        if self.win_xod[1]:
            self.player2_count()
        if self.win_xod[2]:
            self.draw_count()


game = TicTac()
if game.init_type == 3 or game.init_type == 2:
    agent = dqn.DQNAgent()

if game.init_type == 2:
    agent = dqn.DQNAgent()
    agent.load(agent.output_dir + "weights_0450.hdf5")
game.mainloop()
