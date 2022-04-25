import tkinter as tk  # Для создания интерфейса пользователя
import tkinter.messagebox
from PIL import Image, ImageTk
import random
import numpy as np
import dqn


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
        self.osh = 0
        self.win_xod = [0, 0, 0]  # Победа Х,О,Н
        self.game_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0- Пусто, 1-Х, -1-О
        # Информация из интрефейса управлния (пока отсутсвуют)
        self.init_type = 2  # 1 -> человек - человек, 2 -> человек - компьютер, 3 -> рандом - компьютер, 4 -> рандом - ч
        self.init_xo = True  # 1 - X, 0 - 0 кто первый

        self.flag_xo = self.init_xo  # True - X, False - 0 кто первый
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
        for _ in self.element:
            _.destroy()
        self.element = []
        self.flag_xo = self.init_xo
        self.label_end['text'] = ''
        self.label_end_win['text'] = ''
        self.win_xod = [0, 0, 0]
        self.game_field = [0, 0, 0, 0, 0, 0, 0, 0, 0]






    def canva_create(self):
        """
        Функция создает канву для последующего размещения на ней игровго элемента
        :return:
        """
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



    def _random(self):
        """
        Функция реализующая рандомный ход
        :return:
        """
        pos = self.random_hod()
        self.fun_moves_made(pos)
        return self.game_field

    def random_hod(self):
        """
        Функция выбирающая корректный рандомный ход
        :return:
        """
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
        if not self.game_field[pos-1]:
            if self.flag_xo:
                self.hod('X', pos)
                self.game_field[pos-1] = 1
                self.flag_xo = False
            else:
                self.hod('O', pos)
                self.game_field[pos-1] = -1
                self.flag_xo = True
            self.root.update()
        if self.search_end_game():
            self.end_game()

    def search_end_game(self):
        """
        Функция определяющая победу
        :return:
        """
        _win = 0
        for el_win in self.win:
            for _ in el_win:
                _win += self.game_field[_-1]
            if _win**2 == 9:
                if _win > 0:
                    self.win_xod = [1, 0, 0]
                if _win < 0:
                    self.win_xod = [0, 1, 0]
                return True
            _win = 0
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


