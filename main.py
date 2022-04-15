import tkinter as tk  # Для создания интерфейса пользователя
import tkinter.messagebox
from PIL import Image, ImageTk


class TicTac:
    def __init__(self):
        """
        Проводим инициализацию игрового поля
        """
        self.image_P = Image.open("img/P.jpg")
        self.image_X = Image.open("img/X.jpg")
        self.image_O = Image.open("img/O.jpg")

        self.moves_made = [1]
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

        self.win_xod = [0, 0, 0]

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
        self.moves_made = [1]
        self.label_end['text'] = ''
        self.label_end_win['text'] = ''
        self.win_xod = [0, 0, 0]

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

    # canvas_O = tkinter.Canvas(window, height=70, width=70, highlightthickness=0)
    # image_O = image_O.resize((70, 70), Image.LANCZOS)
    # photo_O = ImageTk.PhotoImage(image_O)
    # image_O = canvas_O.create_image(0, 0, anchor='nw', image=photo_O)
    def hod(self, elem, pos_xy):
        """
        Функция реализующая ход на игровом поле
        :param elem: Х или О
        :param pos_xy:  номер ячейки 1,2,3,4,5,6,7,8,9
        :return:
        """
        pos_x, pos_y = self.position[pos_xy - 1]
        self.element.append(self.canva_create())
        ind = len(self.element) - 1
        if elem == 'X':
            self.canva_add_x(self.element[ind])
        else:
            self.canva_add_o(self.element[ind])
        self.print_canva(self.element[ind], pos_x, pos_y)


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

    def fun_moves_made(self, pos):
        """
        Функция реализующая сам ход
        :param pos:
        :return:
        """
        # global moves_made

        moves_made = [x for x, _ in self.moves_made[1:]]
        if pos not in moves_made:
            if self.moves_made[0] == 1:
                self.hod('X', pos)
                self.moves_made.append([pos, 'X'])
                self.moves_made[0] = 0
            else:
                self.hod('O', pos)
                self.moves_made.append([pos, 'O'])
                self.moves_made[0] = 1
            self.root.update()
        if self.search_win_game('O') and not self.win_xod[2]:
            self.end_game('O')
        if self.search_win_game('X') and not self.win_xod[2]:
            self.end_game('X')
        if self.win_xod[2]:
            self.end_game('=')

    def search_win_game(self, elem):
        """
        Функция определяющая победу
        :return:
        """
        if len(self.moves_made) == 10:
            self.win_xod = [0, 0, 1]
            return True
        for el_win in self.win:
            if ([el_win[0], elem] in self.moves_made) and ([el_win[1], elem] in self.moves_made) and ([el_win[2], elem] in self.moves_made):
                if elem == 'X':
                    self.win_xod = [1, 0, 0]
                if elem == 'O':
                    self.win_xod = [0, 1, 0]
                return True
        return False

    def end_game(self, elem):
        if any(self.win_xod[:2]):
            self.label_end['text'] = 'ПОБЕДИЛ :'
            self.label_end_win['text'] = elem
        if self.win_xod[2]:
            self.label_end['text'] = 'НИЧЬЯ'

        if self.win_xod[0]:
            self.player1_count()
        if self.win_xod[1]:
            self.player2_count()
        if self.win_xod[2]:
            self.draw_count()



    # def create_line(self):
    #     canvas_line = tkinter.Canvas(self.root, height=300, width=300, highlightthickness=0)
    #     #canvas_line.create_line(0,0,300,300)
    #     image = tk.PhotoImage(file='img/1.png')
    #     canvas_line.create_image(0,0,image=image, anchor=tk.NW)
    #     canvas_line.place(x=0, y=100)
        #self.element[0].create_line(0,0,70,70)



game = TicTac()



# game.hod('O',1)
# game.hod('X',5)
# canva_x1 = game.canva_create()
# game.canva_add_x(canva_x1)
# game.print_canva(canva_x1,15, 115)

# canva_x2 = game.canva_create()
# game.canva_add_o(canva_x2)
# game.print_canva(canva_x2,115, 115)


game.mainloop()

# canvas_O.place(x=100, y=115)
# window.mainloop()
