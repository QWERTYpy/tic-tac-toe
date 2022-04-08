import tkinter as tk  # Для создания интерфейса пользователя
import tkinter.messagebox
from PIL import Image, ImageTk


class TicTac:
    def __init__(self):
        self.image_P = Image.open("img/P.jpg")
        self.image_X = Image.open("img/X.jpg")
        self.image_O = Image.open("img/O.jpg")
        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.resizable(width=False, height=False)
        self.root.geometry('300x400+100+100')
        self.root.configure(background='#ffffff')
        self.canvas_P = tkinter.Canvas(self.root, height=300, width=300, highlightthickness=0)
        self.canvas_P.configure(background='#ffffff')
        self.image_P = self.image_P.resize((300, 300), Image.LANCZOS)
        self.photo_P = ImageTk.PhotoImage(self.image_P)
        self.image_P = self.canvas_P.create_image(0, 0, anchor='nw', image=self.photo_P)
        self.canvas_P.place(x=0, y=100)
    def im_x(self):
        self.canvas_X = tkinter.Canvas(self.root, height=70, width=70, highlightthickness=0)
        self.image_X = self.image_X.resize((70, 70), Image.LANCZOS)
        self.photo_X = ImageTk.PhotoImage(self.image_X)
        self.image_X = self.canvas_X.create_image(0, 0, anchor='nw', image=self.photo_X)

    def pr_xo(self, x, y):
        self.canvas_X.place(x=x, y=y)

    def mainloop(self):
        self.root.mainloop()
# canvas_O = tkinter.Canvas(window, height=70, width=70, highlightthickness=0)
# image_O = image_O.resize((70, 70), Image.LANCZOS)
# photo_O = ImageTk.PhotoImage(image_O)
# image_O = canvas_O.create_image(0, 0, anchor='nw', image=photo_O)

game = TicTac()
game.im_x()
game.pr_xo(100, 115)
game.mainloop()



#canvas_O.place(x=100, y=115)
# window.mainloop()
