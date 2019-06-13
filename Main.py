import tkinter as tk  # python 3
from tkinter import font as tkfont, messagebox  # python 3
from PIL import ImageTk
from PIL import Image

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
        label = tk.Label(self, text="A complete text game, the program will let users move through rooms based on\n "
                                    "user input and get descriptions of each room. To create this, you’ll need to\n "
                                    "establish the directions in which the user can move, a way to track how far the\n "
                                    "user has moved (and therefore which room he/she is in), and to print out a\n "
                                    "description. You’ll also need to set limits for how far the user can move. In\n "
                                    "other words, create “walls” around the rooms that tell the user,\n "
                                    "“You can’t move further in this direction.”", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="GET SET GO!!!",
                           command=lambda: controller.show_frame("Game"), fg="GREEN")
        button.pack()


class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def click(event):

            if object_id is not None:
                coord = can.coords(object_id)
                width = coord[2] - coord[0]
                height = coord[3] - coord[1]

                can.coords(object_id, event.x, event.y, event.x + width, event.y + height)

        def create_circle():

            global object_id

            object_id = can.create_oval(10, 10, 70, 70, fill='orange', outline='black')

        can = tk.Canvas(self, bg='white', height=550, width=550)
        can.pack(side=tk.RIGHT)
        can.bind("<Button-1>", click)

        btn_circle = tk.Button(self, text='START', width=15, command=create_circle)
        btn_circle.pack()

        btn_delete = tk.Button(self, text='QUIT', width=15, command=delete)
        btn_delete.pack()


if __name__ == "__main__":
    app = Main()
    app.mainloop()
