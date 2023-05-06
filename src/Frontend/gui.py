import tkinter as tk
from PIL import ImageTk, Image
from src.Frontend.clickEvent import ClickEvent
import src.Backend.Figuren as fig
import src.Backend.Convert as con


class GUI:
    def callback(self, e):
        self.x = e.x
        self.y = e.y

    def __init__(self=None):
        self.root = tk.Tk()
        self.root.title("Schachpositionsanalyse")
        self.root.geometry("800x800")

        start_text = tk.Label(self.root)
        start_text["text"] = "Schachspiel\nmit\nPositionsanalyse"
        start_text["font"] = "Arial, 40"
        start_text.place(x=220, y=0, height=200, width=350)

        self.canvas = tk.Canvas(self.root, bg="black", width=440, height=440)
        self.canvas.place(x=150, y=200)

        # Erstellen des Schachbretthintergrundes
        background = tk.PhotoImage(
            file="/Users/nmbk/Development/Schachpositionsanalyse/pic/Chessboard.png"
        )
        self.canvas.create_image(223, 223, image=background)

        # Erstellen der Figuren
        self.createImgs()

        button = tk.Button(self.root, command=lambda: self.refactor())
        button["text"] = "Neues Spiel"
        button["font"] = "Century-Gothic, 16"
        button.place(x=200, y=650, height=50, width=200)

        # Figuren erstellen:
        self.fig = fig.Figuren(None, None, None, None)
        self.fig.createFig()

        # Das Canvas an Motions binden, sodass Bewegungen und die Position während des Aufenthalts
        # im Canvas aktualisiert wird
        self.canvas.bind("<Motion>", self.callback)

        # Aktivieren des Mouse Listeners
        ClickEvent(self)

        self.root.mainloop()

    def getXY(self):
        return self.x, self.y

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
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/rook_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[1] = ImageTk.PhotoImage(rook_w)
        self.img_id[1] = self.canvas.create_image(30, 30, image=self.img[1])

        knight_w = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/knight_w.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[2] = ImageTk.PhotoImage(knight_w)
        self.img_id[2] = self.canvas.create_image(85, 30, image=self.img[2])

        bishop_w = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/bishop_w.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[3] = ImageTk.PhotoImage(bishop_w)
        self.img_id[3] = self.canvas.create_image(140, 30, image=self.img[3])

        queen_w = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/queen_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[4] = ImageTk.PhotoImage(queen_w)
        self.img_id[4] = self.canvas.create_image(195, 30, image=self.img[4])

        king_w = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/king_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[5] = ImageTk.PhotoImage(king_w)
        self.img_id[5] = self.canvas.create_image(250, 30, image=self.img[5])

        bishop_w_2 = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/bishop_w.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[6] = ImageTk.PhotoImage(bishop_w_2)
        self.img_id[6] = self.canvas.create_image(305, 30, image=self.img[6])

        knight_w_2 = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/knight_w.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[7] = ImageTk.PhotoImage(knight_w_2)
        self.img_id[7] = self.canvas.create_image(360, 30, image=self.img[7])

        rook_w_2 = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/rook_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[8] = ImageTk.PhotoImage(rook_w_2)
        self.img_id[8] = self.canvas.create_image(415, 30, image=self.img[8])

        pawn_w = []
        for i in range(0, 8):
            pawn_w.insert(
                i,
                Image.open(
                    "/Users/nmbk/Development/Schachpositionsanalyse/pic/pawn_w.png"
                )
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
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/rook_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[25] = ImageTk.PhotoImage(rook_b)
        self.img_id[25] = self.canvas.create_image(30, 415, image=self.img[25])

        bishop_b = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/bishop_b.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[26] = ImageTk.PhotoImage(bishop_b)
        self.img_id[26] = self.canvas.create_image(140, 415, image=self.img[26])

        knight_b = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/knight_b.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[27] = ImageTk.PhotoImage(knight_b)
        self.img_id[27] = self.canvas.create_image(85, 415, image=self.img[27])

        queen_b = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/queen_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[28] = ImageTk.PhotoImage(queen_b)
        self.img_id[28] = self.canvas.create_image(195, 415, image=self.img[28])

        king_b = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/king_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[29] = ImageTk.PhotoImage(king_b)
        self.img_id[29] = self.canvas.create_image(250, 415, image=self.img[29])

        bishop_b_2 = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/bishop_b.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[30] = ImageTk.PhotoImage(bishop_b_2)
        self.img_id[30] = self.canvas.create_image(305, 415, image=self.img[30])

        knight_b_2 = (
            Image.open(
                "/Users/nmbk/Development/Schachpositionsanalyse/pic/knight_b.png"
            )
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[31] = ImageTk.PhotoImage(knight_b_2)
        self.img_id[31] = self.canvas.create_image(360, 415, image=self.img[31])

        rook_b_2 = (
            Image.open("/Users/nmbk/Development/Schachpositionsanalyse/pic/rook_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[32] = ImageTk.PhotoImage(rook_b_2)
        self.img_id[32] = self.canvas.create_image(415, 415, image=self.img[32])

        pawn_b = []
        for i in range(0, 8):
            pawn_b.insert(
                i,
                Image.open(
                    "/Users/nmbk/Development/Schachpositionsanalyse/pic/pawn_b.png"
                )
                .resize((55, 55), Image.ANTIALIAS)
                .convert("RGBA"),
            )
            self.img[i + 17] = ImageTk.PhotoImage(pawn_b[i])
            self.img_id[i + 17] = self.canvas.create_image(
                30 + i * 55, 360, image=self.img[i + 17]
            )
        ################################################################################################################
