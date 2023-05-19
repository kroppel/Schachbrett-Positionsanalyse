import tkinter as tk
import os
from PIL import ImageTk, Image
from Frontend.clickEvent import ClickEvent
import Backend.Figuren as fig
import Backend.Convert as con
import Backend.VidIn as vi
import threading as th
import cv2
from time import sleep


class GUI:

    def __init__(self=None):
        self.abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/img/"

        self.clickEvent = ClickEvent(self)

        self.x = 0
        self.y = 0

        self.root = tk.Tk()
        self.root.title("Schachpositionsanalyse")
        self.root.geometry("1300x800")

        start_text = tk.Label(self.root)
        start_text["text"] = "Schachspiel mit Positionsanalyse"
        start_text["font"] = "Arial 30 underline"
        start_text.place(x=430, y=0, height=100, width=450)

        self.canvas = tk.Canvas(self.root, bg="black", width=440, height=440)
        self.canvas.place(x=100, y=200)

        self.canvas_trenn = tk.Canvas(self.root, bg=None, width=20, height=600)
        self.canvas_trenn.place(x=640, y=150)

        # Fenster mit Video Input
        self.canvas_vidin = tk.Canvas(self.root, bg='black', width=440, height=440)
        self.canvas_vidin.place(x=740, y=200)
        self.vid = vi.VidIn()
        th.Thread(target=lambda: self.update()).start()

        # Erstellen des Schachbretthintergrundes
        background = Image.open(self.abs_path+"Chessboard.png")
        background_img = ImageTk.PhotoImage(background)
        self.canvas.create_image(223, 223, image=background_img)

        # Erstellen der Figuren
        self.createImgs()

        # Erstellen der Buttons
        button = tk.Button(self.root, command=lambda: self.refactor())
        button["text"] = "Neues Spiel"
        button["font"] = "Century-Gothic, 16"
        button.place(x=100, y=650, height=50, width=145)

        button_back = tk.Button(self.root, command=lambda: self.goBack())
        button_back["text"] = "<"
        button_back["font"] = "Century-Gothic, 24"
        button_back.place(x=250, y=650, height=50, width=70)

        button_next = tk.Button(self.root, command=lambda: self.goNext())
        button_next["text"] = ">"
        button_next["font"] = "Century-Gothic, 24"
        button_next.place(x=325, y=650, height=50, width=70)

        button_tipps = tk.Button(self.root, command=lambda: self.refactor())
        button_tipps["text"] = "Tipps"
        button_tipps["font"] = "Century-Gothic, 18"
        button_tipps.place(x=400, y=650, height=50, width=145)

        # Erstellen des Buchstaben Randes
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(0, 8):
            tk.Label(self.root, text=letters[i], font='Century-Gothic, 20').place(x=75, y=218+i*55, height=25, width=25)
            tk.Label(self.root, text=i+1, font='Century-Gothic, 20').place(x=118+i*55, y=175, height=25, width=25)

        # Trennlinie
        self.canvas_trenn.create_line(9, 5, 9, 605, width=2)

        # Überschrift Video Input Canvas
        tk.Label(self.root, text='Camera Video Input:', font='Century-Gothic, 20').place(x=735, y=180, height=20, width=200)

        # Figuren erstellen:
        self.fig = fig.Figuren(None, None, None, None, None)
        self.fig.createFig()

        # Das Canvas an Button-1 binden
        self.canvas.bind("<Button-1>", self.callback)

        # Mainloop starten
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()

        if ret:
            frame = Image.fromarray(frame)
            frame = frame.resize((440, 440), Image.ANTIALIAS)   # muss noch umgeändert werden
            self.photo = ImageTk.PhotoImage(image=frame)
            self.canvas_vidin.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(15, self.update())

    def callback(self, e):
        self.clickEvent.on_click(e.x, e.y)

    def getfigLists(self):
        return self.fig.getLists()

    def erstelleImgofFigur(self, x, y, id):
        self.img_id[id] = self.canvas.create_image(x, y, image=self.img[id])

    def loescheImgofFigur(self, id):
        self.canvas.delete(self.img_id[id])

    def switchImgofFigur(self, x, y, id):
        self.loescheImgofFigur(id)
        posx, posy = con.Convert().convFiePos(x, y)
        self.erstelleImgofFigur(posx, posy, id)

    def createImgs(self):
        ################################################################################################################
        # Erstellen der weißen Figuren
        # Vergabe der IDS wie folgt (weiße Figuren unten):
        # 25 26 27 28 29 30 31 32
        # 17 18 19 20 21 22 23 24
        #
        #
        #  9 10 11 12 13 14 15 16
        #  1  2  3  4  5  6  7  8

        self.img = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        self.img_id = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        rook_w = (
            Image.open(self.abs_path+"rook_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[1] = ImageTk.PhotoImage(rook_w)
        self.img_id[1] = self.canvas.create_image(30, 30, image=self.img[1])

        knight_w = (
            Image.open(self.abs_path+"knight_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[2] = ImageTk.PhotoImage(knight_w)
        self.img_id[2] = self.canvas.create_image(85, 30, image=self.img[2])

        bishop_w = (
            Image.open(self.abs_path+"bishop_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[3] = ImageTk.PhotoImage(bishop_w)
        self.img_id[3] = self.canvas.create_image(140, 30, image=self.img[3])

        queen_w = (
            Image.open(self.abs_path+"queen_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[4] = ImageTk.PhotoImage(queen_w)
        self.img_id[4] = self.canvas.create_image(195, 30, image=self.img[4])

        king_w = (
            Image.open(self.abs_path+"king_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[5] = ImageTk.PhotoImage(king_w)
        self.img_id[5] = self.canvas.create_image(250, 30, image=self.img[5])

        bishop_w_2 = (
            Image.open(self.abs_path+"bishop_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[6] = ImageTk.PhotoImage(bishop_w_2)
        self.img_id[6] = self.canvas.create_image(305, 30, image=self.img[6])

        knight_w_2 = (
            Image.open(self.abs_path+"knight_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[7] = ImageTk.PhotoImage(knight_w_2)
        self.img_id[7] = self.canvas.create_image(360, 30, image=self.img[7])

        rook_w_2 = (
            Image.open(self.abs_path+"rook_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[8] = ImageTk.PhotoImage(rook_w_2)
        self.img_id[8] = self.canvas.create_image(415, 30, image=self.img[8])

        pawn_w = []
        for i in range(0, 8):
            pawn_w.insert(
                i,
                Image.open(self.abs_path+"pawn_w.png")
                .resize((55, 55), Image.ANTIALIAS)
                .convert("RGBA"),
            )
            self.img[i + 9] = ImageTk.PhotoImage(pawn_w[i])
            self.img_id[i + 9] = self.canvas.create_image(
                30 + i * 55, 85, image=self.img[i + 9]
            )

        ################################################################################################################
        # Erstellen der schwarzen Figuren
        rook_b = (
            Image.open(self.abs_path+"rook_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[25] = ImageTk.PhotoImage(rook_b)
        self.img_id[25] = self.canvas.create_image(30, 415, image=self.img[25])

        knight_b = (
            Image.open(self.abs_path + "knight_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[26] = ImageTk.PhotoImage(knight_b)
        self.img_id[26] = self.canvas.create_image(85, 415, image=self.img[26])

        bishop_b = (
            Image.open(self.abs_path+"bishop_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[27] = ImageTk.PhotoImage(bishop_b)
        self.img_id[27] = self.canvas.create_image(140, 415, image=self.img[27])


        queen_b = (
            Image.open(self.abs_path+"queen_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[28] = ImageTk.PhotoImage(queen_b)
        self.img_id[28] = self.canvas.create_image(195, 415, image=self.img[28])

        king_b = (
            Image.open(self.abs_path+"king_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[29] = ImageTk.PhotoImage(king_b)
        self.img_id[29] = self.canvas.create_image(250, 415, image=self.img[29])

        bishop_b_2 = (Image.open(self.abs_path+"bishop_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[30] = ImageTk.PhotoImage(bishop_b_2)
        self.img_id[30] = self.canvas.create_image(305, 415, image=self.img[30])

        knight_b_2 = (
            Image.open(self.abs_path+"knight_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[31] = ImageTk.PhotoImage(knight_b_2)
        self.img_id[31] = self.canvas.create_image(360, 415, image=self.img[31])

        rook_b_2 = (
            Image.open(self.abs_path+"rook_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[32] = ImageTk.PhotoImage(rook_b_2)
        self.img_id[32] = self.canvas.create_image(415, 415, image=self.img[32])

        pawn_b = []
        for i in range(0, 8):
            pawn_b.insert(
                i,
                Image.open(self.abs_path+"pawn_b.png")
                .resize((55, 55), Image.ANTIALIAS)
                .convert("RGBA"),
            )
            self.img[i + 17] = ImageTk.PhotoImage(pawn_b[i])
            self.img_id[i + 17] = self.canvas.create_image(
                30 + i * 55, 360, image=self.img[i + 17]
            )
        ################################################################################################################
