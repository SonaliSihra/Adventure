import math
import tkinter as tk  # python 3
from tkinter import font as tkfont, messagebox  # python 3
from PIL import ImageTk
from PIL import Image
from array import *

object_id = None


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='calibre', size=12, slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Rules, Game):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


def delete():
    msg = messagebox.askyesnocancel('Info', 'Do you want to quit the game ?')
    if msg == True:
        quit()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the game of ADVENTURE!\n click on NEXT to view the rules\n "
                                    "GET SET GO!!! ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="NEXT",
                            command=lambda: controller.show_frame("Rules"), fg="GREEN")
        button2 = tk.Button(self, text="Skip to game directly",
                            command=lambda: controller.show_frame("Game"), fg="GREEN")
        button3 = tk.Button(self, text="QUIT", fg="RED", command=delete)

        bard = Image.open("add.jpg")
        logo = ImageTk.PhotoImage(bard)
        label1 = tk.Label(self, image=logo)
        label1.image = logo
        label1.pack(side="bottom")

        button1.pack(side="right")
        button2.pack(side="right")
        button3.pack(side="left")


class Rules(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hey champ!! this is a game where you can compete with your friends to know how\n "
                                    "much distance you have covered only in 2 minute!! Yes, there are no hardcore\n "
                                    "rules You will be represented by the orange circle and you have to move the\n "
                                    "circle in inside the white frame to cover the vast distance as soon as "
                                    "possible.\n "
                                    "Hint=[Try to click on opposite corners to cover the most of the distance,\n "
                                    "this will increase your total score. The distance is getting calculated in\n "
                                    "backend and will be shown on console in the end.] \n All the best!!!",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="GET SET GO!!!",
                           command=lambda: controller.show_frame("Game"), fg="GREEN")

        btn_delete = tk.Button(self, text='QUIT', width=15, command=delete, fg="RED")
        btn_delete.pack()
        button.pack()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        x1 = []
        y1 = []
        distance = []

        def click(event):
            if object_id:
                coord = can.coords(object_id)
                width = coord[2] - coord[0]
                height = coord[3] - coord[1]

                can.coords(object_id, event.x, event.y, event.x + width, event.y + height)
                print("x: ", event.x, "y: ", event.y)
                if x1:
                    distance.append(math.sqrt(((x1[-1] - event.x) ** 2) + ((y1[-1] - event.y) ** 2)))
                    print('last distance jump', distance[-1])
                    print('total distance', sum(distance))
                x1.append(event.x)
                y1.append(event.y)
                # print(x1)
                # print(y1)

        def create_circle():
            global object_id

            object_id = can.create_oval(10, 10, 70, 70, fill='orange', outline='black')
            app.after(20000, lambda: app.destroy())

        can = tk.Canvas(self, bg='white', height=650, width=650)
        can.pack(side=tk.RIGHT)
        can.bind("<Button-1>", click)

        btn_circle = tk.Button(self, text='START', width=15, command=create_circle)
        btn_circle.pack()

        btn_delete = tk.Button(self, text='QUIT', width=15, command=delete)
        btn_delete.pack()


if __name__ == "__main__":
    app = Main()
    app.mainloop()
