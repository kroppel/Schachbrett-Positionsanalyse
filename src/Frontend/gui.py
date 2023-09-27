import tkinter as tk
import os
import time
import chess as ch
from PIL import ImageTk, Image
from Frontend.clickEvent import ClickEvent
import Backend.Figuren as fig
import Backend.Convert as con
import Backend.VidIn as vi
import threading as th
import numpy as np
import cv2
from time import sleep

''' Class GUI represents the Front End with the visual components and some basic functionality '''
class GUI:

    """ Initializing the GUI a windows with buttons, text, listbox and canvas elements,
     along with all the initial values for the start of the game. """
    def __init__(self=None):
        self.abs_path = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/img/"
        )

        self.clickEvent = ClickEvent(self)
        self.option = True

        self.goBackBool = False
        self.count = 0

        self.arrow = None

        self.rect = None

        self.Figures = []

        self.x = 0
        self.y = 0

        self.root = tk.Tk()
        self.root.title("Schachpositionsanalyse")
        self.root.geometry("1470x950")

        start_text = tk.Label(self.root)
        start_text["text"] = "Schachspiel mit Positionsanalyse"
        start_text["font"] = "Arial 30 underline"
        start_text.place(x=430, y=0, height=100, width=450)

        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            width=438,
            height=438,
            highlightthickness=2,
            highlightbackground="#04d9ff",
        )
        self.canvas.place(x=100, y=200)

        self.output_text = tk.Label(self.root)
        self.output_text.config(
            text="Output", font="Arial, 18", borderwidth=2, relief="ridge"
        )
        self.output_text.place(x=100, y=720, height=80, width=450)

        # Liste von Zügen
        self.my_listbox = tk.Listbox(self.root, height=26, activestyle="dotbox")
        self.my_listbox.place(x=580, y=200)
        self.my_listbox.insert(tk.END, "Züge:")
        self.listend = 0
        self.listakt = 0

        self.canvas_trenn = tk.Canvas(self.root, bg=None, width=20, height=600)
        self.canvas_trenn.place(x=790, y=150)

        # Fenster mit Video Input
        self.vid = vi.VidIn(self)
        self.canvas_vidin = tk.Canvas(self.root, bg="black", width=437, height=437)

        self.vidb = tk.Canvas(self.root, bg="black", width=200, height=200)
        self.vidb.place(x=880, y=450)

        self.vidw = tk.Canvas(self.root, bg="black", width=200, height=200)
        self.vidw.place(x=880, y=200)

        self.slider1 = tk.Scale(self.root, from_=0, to=255, command=self.switchw)
        self.slider1.set(135)
        self.slider1.place(x=1100, y=200)

        self.slider2 = tk.Scale(self.root, from_=0, to=255, command=self.switchb)
        self.slider2.set(65)
        self.slider2.place(x=1100, y=450)

        th.Thread(target=lambda: self.start()).start()

        # Erstellen des Schachbretthintergrundes
        background = Image.open(self.abs_path + "Chessboard.png")
        background_img = ImageTk.PhotoImage(background)
        self.canvas.create_image(222, 222, image=background_img)

        # Erstellen der Figuren
        self.createImgs()

        # Erstellen der Buttons
        button = tk.Button(self.root, command=lambda: self.newGame())
        button["text"] = "Neues Spiel"
        button["font"] = "Century-Gothic, 16"
        button.place(x=100, y=650, height=50, width=145)

        button_back = tk.Button(self.root, command=lambda: self.goBack())
        button_back["text"] = "<"
        button_back["font"] = "Century-Gothic, 24"
        button_back.place(x=250, y=650, height=50, width=70)

        button_next = tk.Button(self.root, command=lambda: self.goForward())
        button_next["text"] = ">"
        button_next["font"] = "Century-Gothic, 24"
        button_next.place(x=325, y=650, height=50, width=70)

        self.button_option = tk.Button(self.root, command=lambda: self.switchoption())
        self.button_option["text"] = "Apply"
        self.button_option["font"] = "Century-Gothic, 18"
        self.button_option.place(x=890, y=700, height=50, width=145)

        button_tipps = tk.Button(self.root, command=lambda: self.tipp())
        button_tipps["text"] = "Tipps"
        button_tipps["font"] = "Century-Gothic, 18"
        button_tipps.place(x=400, y=650, height=50, width=145)

        # Erstellen des Buchstaben Randes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for i in range(0, 8):
            tk.Label(self.root, text=8 - i, font="Century-Gothic, 20").place(
                x=75, y=218 + i * 55, height=25, width=25
            )
            tk.Label(self.root, text=letters[i], font="Century-Gothic, 20").place(
                x=118 + i * 55, y=175, height=25, width=25
            )

        # Trennlinie
        self.canvas_trenn.create_line(9, 5, 9, 605, width=2)

        # Überschrift Video Input Canvas
        tk.Label(
            self.root, text="Camera Video Input:", font="Century-Gothic, 20"
        ).place(x=885, y=180, height=20, width=200)

        # Figuren erstellen:
        self.fig = fig.Figuren(None, None, None, None, None)
        self.fig.createFig()

        # Das Canvas an Button-1 binden
        self.canvas.bind("<Button-1>", self.callback)

        # Mainloop starten
        self.root.mainloop()

    ###################################################################################################################
    # Button Functions

    """
        Info: Activates Stockfish in the backend, passes the board and receives the result. 
        Param: None
        Return: draws an arrow and outputs the result and time needed in the Info Textfield at the bottom 
    """
    def tipp(self):
        self.deleteArrow()
        t1 = int(time.time() * 1000)
        result = str(self.clickEvent.tipp())
        t2 = int(time.time() * 1000)
        self.changeOutput(result + " (" + str(t2 - t1) + " ms)")

        # result to Coordinates:
        x1, y1 = con.Convert().convFiePos(
            con.Convert().convLetFie(result[0]), int(result[1])
        )
        x2, y2 = con.Convert().convFiePos(
            con.Convert().convLetFie(result[2]), int(result[3])
        )

        # draw the arrow
        self.drawArrow(x1, y1, x2, y2)

    """
        Info: Resets the game state, place all pieces in their standard positions and reset the backend,
        including the chess library and the initial piece recognition configuration. Clears the move list. 
        Params: None
        Return: New Game
    """

    def newGame(self):
        self.clickEvent = ClickEvent(self)
        # löschen aller aktiven images
        for i in range(1, 9):
            for j in range(1, 9):
                self.canvas.delete(self.img_id[i * 10 + j])
                self.img_id[i * 10 + j] = None

        self.createImgs()
        self.goBackBool = False
        self.count = 0

        self.deleteArrow()
        self.Figures = []
        self.my_listbox.delete(1, tk.END)
        self.listend = 0
        self.listakt = 0
        self.ErrorOff()
        self.changeOutput("Neues Spiel")
        self.canvas.delete(self.rect)
        self.vid.restart(self)

    # switcht zwischen großer Ausgabe des Produktes und Optionen um die Farbmasken Einstellunge zu ändern

    ''' Switches between the full camera input display and the options menu 
    that allows the user to adjust the color masks. '''
    def switchoption(self):
        if self.option:
            self.option = False
            self.vidn()
            self.button_option["text"] = "Option"
            self.vid.switchoption()

        else:
            self.option = True
            self.vido()
            self.button_option["text"] = "Apply"
            self.vid.switchoption()

    ''' Deletes the option elements and shows the full camera input '''
    def vidn(self):
        self.canvas_vidin.place(x=890, y=200)
        self.vidb.place_forget()
        self.vidw.place_forget()
        self.slider1.place_forget()
        self.slider2.place_forget()

    ''' Deletes the camera input element and shows the option elements '''
    def vido(self):
        self.canvas_vidin.place_forget()
        self.vidb.place(x=880, y=450)
        self.vidw.place(x=880, y=200)
        self.slider1.place(x=1100, y=200)
        self.slider2.place(x=1100, y=450)

    """
        Info: Gets the slider Input and changes the color mask to the new selected values. 
        (w for white, b for black Mask)
        Params: e = value of slider
        Return: None
    """
    def switchw(self, e):
        self.vid.lower_white = np.array([0, 40, int(e)])

    def switchb(self, e):
        self.vid.upper_black = np.array([255, 255, int(e)])

    ########################################################################################################################
    # VisualFeedback

    """
        Info: Changes the Output of the text field at the bottom of the left side under the board. 
        Params: The new String that will be displayed. 
        Return: None
    """
    def changeOutput(self, string):
        self.output_text.config(text=string)

    ''' Enables the visual feedback a red line arround the board. Triggered by check or illegal moves'''
    def ErrorOn(self):
        self.canvas.config(highlightbackground="red")

    ''' Clears the red line --> disables visual feedback when error is resolved '''
    def ErrorOff(self):
        self.canvas.config(highlightbackground="#04d9ff")

    """
        Info: Draws an arrow representing the calculated result fo Stockfishs optimal move. 
        Params: Start and end point of the arrow 
        Return: None
    """
    def drawArrow(self, x1, y1, x2, y2):
        self.arrow = self.canvas.create_line(
            x1, y1, x2, y2, arrow=tk.LAST, fill="green", width=4
        )

    ''' Deletes the drawn arrow after the player moved a piece '''
    def deleteArrow(self):
        if not self.arrow is None:
            self.canvas.delete(self.arrow)

    ####################################################################################################################

    ''' Checks the video input stream for new frames every 15 milliseconds.  '''
    def start(self):
        while True:
            self.root.after(15, self.update())

    ''' Displays new frames in the canvas made for the video input stream. '''
    def update(self):
        ret, frame1, frame2 = self.vid.getFrame()

        if ret:
            frame1 = Image.fromarray(frame1)
            if self.option and (not frame2 is None):
                frame1 = frame1.resize(
                    (200, 200), Image.ANTIALIAS
                )  # muss noch umgeändert werden
                self.photo1 = ImageTk.PhotoImage(image=frame1)
                frame2 = Image.fromarray(frame2)
                frame2 = frame2.resize(
                    (200, 200), Image.ANTIALIAS
                )  # muss noch umgeändert werden
                self.photo2 = ImageTk.PhotoImage(image=frame2)
                self.vidw.create_image(0, 0, image=self.photo1, anchor=tk.NW)
                self.vidb.create_image(0, 0, image=self.photo2, anchor=tk.NW)
            else:
                frame1 = frame1.resize(
                    (440, 440), Image.ANTIALIAS
                )  # muss noch umgeändert werden
                self.photo1 = ImageTk.PhotoImage(image=frame1)
                self.canvas_vidin.create_image(0, 0, image=self.photo1, anchor=tk.NW)

    """
        Info: Passes the coordinates of the event mouse click - only on the chessboard - to the backend.
        Params: e = the coordinates of the clicked pixel. 
        Return: None
    """
    def callback(self, e):
        if not self.goBackBool:
            self.clickEvent.on_click(e.x, e.y)
        else:
            print("Fehler")

    """
        Info: Passes the field position of a detected move to the backend. 
        Params: Coords of field on chessboard. 
        Return: Quick feedback that action performed well 
    """
    def callback_move_detection(self, p):
        p = con.Convert().convFiePos(p[1] + 1, 8 - p[0])
        return self.clickEvent.on_click(p[0], p[1])

    '''returns the figure List --> old custom-coded logic --> not in use anymore'''
    def getfigLists(self):
        return self.fig.getLists()

    ####################################################################################################################
    # Functionalities for the list and for navigating forward and backward through chess moves.
    # It is implemented purely graphically. No input is accepted as long as you are not at the current state.

    """
        Info: Inserts a string encoded based on the move into the li-fo list at the right side of the board. 
        Figures get saved in an extra array so we have information which piece got deleted or moved. 
        
        Params: start = pos of figure before, target = pos of figure after, figure1 = moved figure, 
        figure2 = saved only if piece is captured 
        
        Return: none
    """
    def insertItemInList(self, start, target, figure1, figure2):
        print("Inserted Pieces", figure1, figure2)
        if start == "cg":
            # speichern der Figur Typen
            self.Figures.append(figure1)
            if figure1 == "K":
                self.Figures.append("R")
            elif figure1 == "k":
                self.Figures.append("r")
            self.count += 2
            # Moves festlegen
            string = (start, target[0], target[1])
        elif ((figure1 == "p") | (figure1 == "P")) & (
            (target[1] == "8") | (target[1] == "1")
        ):  # pawnPromotion
            print("PawnPromo")
            # speichern der Figur Typen
            self.Figures.append(figure1)
            self.Figures.append(figure2)
            self.count += 2
            # Moves festlegen
            string = ("pp", start[0], start[1], "-->", target[0], target[1])

        else:
            # geben die id der geschlagenen Figur mit, damit er sie beim Zurückgehen wieder erstellen kann
            self.Figures.append(figure1)
            if not (figure2 == "None"):
                self.Figures.append(figure2)
                self.count += 2
                string = (start[0], start[1], "-->", target[0], target[1], "!")
            else:
                self.count += 1
                string = (start[0], start[1], "-->", target[0], target[1], ".")

        print("Count", self.count)

        self.my_listbox.insert(tk.END, string)
        self.listend += 1
        self.listakt += 1
        self.my_listbox.yview(tk.END)

    """
        Info: Returns the element at the end of the list (so first inserted).
        Params: i = index of list element
        Return: return element at the 
    """
    def getListend(self, i):
        return self.my_listbox.get(i)

    ''' Undo the last move to review past moves. 
    This is achieved by decoding the last inserted string and reversing the move encoded within it. 
    Gets the involved pieces by an extra array.
    The game is paused, and new inputs are temporarily disabled, which will result in an error if attempted. 
    Once the current state is restored, gameplay can resume.'''
    def goBack(self):
        print(self.count)
        # holen uns die Koordinaten vom aktuellen index
        string = self.my_listbox.get(self.listakt)

        self.deleteArrow()

        print("String to handle: ", string)

        if string != "Züge:":
            if string[0] == "cg":
                self.castling(string[1] + string[2], False)
                self.count -= 2
            elif string[0] == "pp":
                x1 = con.Convert().convLetFie(string[1])
                y1 = int(string[2])
                x2 = con.Convert().convLetFie(string[4])
                y2 = int(string[5])

                pos1 = con.Convert().convFiePos(x1, y1)
                pos2 = con.Convert().convFiePos(x2, y2)

                self.count -= 1
                piece2 = self.Figures[self.count]

                self.count -= 1
                piece1 = self.Figures[self.count]
                img1 = self.getImg(piece1)

                print(piece1, piece2)

                if not (piece2 == "None"):
                    img2 = self.getImg(piece2)
                    self.img_id[y2 * 10 + x2] = self.canvas.create_image(
                        pos2[0], pos2[1], image=self.img[img2]
                    )

                self.canvas.delete(self.img_id[y1 * 10 + x1])
                self.canvas.delete(self.img_id[y2 * 10 + x2])

                # piece2 ist der geschlagene und steht daher auf x2 y2, piece1 der schlagende auf x1 y1
                self.img_id[y1 * 10 + x1] = self.canvas.create_image(
                    pos1[0], pos1[1], image=self.img[img1]
                )
            else:
                # gehe zurück
                x1 = con.Convert().convLetFie(string[0])
                y1 = int(string[1])
                x2 = con.Convert().convLetFie(string[3])
                y2 = int(string[4])
                geschlagen = string[5]
                print(x1, y1, x2, y2, geschlagen)

                # ziehen uns die Informationen raus
                pos1 = con.Convert().convFiePos(x1, y1)
                self.count -= 1
                piece1 = self.Figures[self.count]
                img1 = self.getImg(piece1)

                self.canvas.delete(self.img_id[y2 * 10 + x2])
                self.canvas.delete(self.img_id[y1 * 10 + x1])

                # wenn ein Ausrufezeichen hinter dem String steht, wurde eine Figur geschlagen
                if geschlagen == "!":
                    print("Ausrufe")
                    pos2 = con.Convert().convFiePos(x2, y2)
                    self.count -= 1
                    piece2 = self.Figures[self.count]
                    img2 = self.getImg(piece2)

                    # piece2 ist der geschlagene und steht daher auf x2 y2, piece1 der schlagende auf x1 y1
                    self.img_id[y1 * 10 + x1] = self.canvas.create_image(
                        pos1[0], pos1[1], image=self.img[img2]
                    )
                    self.img_id[y2 * 10 + x2] = self.canvas.create_image(
                        pos2[0], pos2[1], image=self.img[img1]
                    )
                else:
                    self.img_id[y1 * 10 + x1] = self.canvas.create_image(
                        pos1[0], pos1[1], image=self.img[img1]
                    )
                    print("switch")

            self.goBackBool = True
            self.listakt -= 1
            self.ErrorOn()
            self.changeOutput("Nicht aktueller Spielstand")

        else:
            self.changeOutput("Zurück nicht möglich")

    ''' Redo the next move until current state is restored.'''
    def goForward(self):
        print(self.count)
        if self.listakt == self.listend:
            self.changeOutput("Vor nicht möglich")
            self.goBackBool = False
        else:
            self.listakt += 1
            string = self.my_listbox.get(self.listakt)

            if string[0] == "cg":
                self.castling(string[1] + string[2], True)
                self.count += 2
            elif string[0] == "pp":
                pos1 = [con.Convert().convLetFie(string[1]), int(string[2])]
                pos2 = [con.Convert().convLetFie(string[4]), int(string[5])]
                print("pp", pos1, pos2)
                self.pawnPromo(pos1, pos2, True)
                self.count += 2
            else:
                # gehe vor
                x1 = con.Convert().convLetFie(string[0])
                y1 = int(string[1])
                x2 = con.Convert().convLetFie(string[3])
                y2 = int(string[4])
                geschlagen = string[5]
                print(x1, y1, x2, y2, geschlagen)

                # ziehen uns die Informationen raus
                pos1 = con.Convert().convFiePos(x2, y2)
                self.canvas.delete(self.img_id[y1 * 10 + x1])
                self.canvas.delete(self.img_id[y2 * 10 + x2])

                piece1 = self.Figures[self.count]
                img1 = self.getImg(piece1)

                # wenn ein Ausrufezeichen hinter dem String steht, wurde eine Figur geschlagen
                if geschlagen == "!":
                    self.count += 2
                else:
                    self.count += 1

                self.img_id[(y2 * 10 + x2)] = self.canvas.create_image(
                    pos1[0], pos1[1], image=self.img[img1]
                )

            if self.listakt == self.listend:
                self.goBackBool = False
                self.changeOutput("Aktueller Spielstand erreicht")
                self.ErrorOff()


    ###################################################################################################################
    # Implementation of the new logic

    """
        Info: A figure got chosen by player and no error occurred. "
        Params: pos = chosen figure pos 
        Return: none
    """
    def legalPick(self, pos):
        # Field to Pixel Position
        x, y = con.Convert().convFiePos(pos[0], pos[1])

        # surround it blue
        self.ErrorOff()
        self.changeOutput("Figur erkannt, wähle das Ziel")
        if not (self.rect is None):
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            x - 28, y - 28, x + 28, y + 28, width=2, outline="#04d9ff"
        )
        return

    ''' Visual feedback when user clicks on an opponents piece (and has not selected his own before). '''
    def illegalColor(self):
        self.ErrorOn()
        self.changeOutput("Diese Farbe ist gerade nicht am Zug")

    ''' Visual feedback when user clicks an empty field. '''
    def illegalPick(self):
        self.ErrorOn()
        self.changeOutput("Keine Figur auf dem Feld")
        return

    """
        Info: If move was legal the piece gets moved, so img is deleted on old pos and created on new one. 
        Params: savedPos == old position of figure, pos == target of move, piece = get image by arr id
        Return: none
    """
    def legalMove(self, savedPos, pos, piece):
        self.canvas.delete(self.rect)
        self.ErrorOff()
        self.changeOutput("Zug durchgeführt")

        xsavedPos = savedPos[1] * 10 + savedPos[0]

        xpos = pos[1] * 10 + pos[0]
        print(xsavedPos, xpos)

        # Pixel for Positions
        pposX, pposY = con.Convert().convFiePos(pos[0], pos[1])

        self.canvas.delete(self.img_id[xsavedPos])
        self.canvas.delete(self.img_id[xpos])

        i = self.getImg(piece)
        self.img_id[xpos] = self.canvas.create_image(pposX, pposY, image=self.img[i])
        print(str(self.img_id[xpos]))
        return

    """
        Info: Switches the Image Position of the Rook and King based on which side and rook the castling is made.
        Params: pos == position of the rook, bool = white or black side
        Return: none
    """
    def castling(self, pos, bool):
        print("Castling", pos)
        if not self.goBackBool:
            self.canvas.delete(self.rect)
            self.ErrorOff()
            self.changeOutput("Zug durchgeführt")
        if pos[1] == "1":  # weißer König
            if bool:
                self.canvas.delete(self.img_id[15])
            if pos[0] == "g":  # move nach rechts
                if bool:
                    self.canvas.delete(self.img_id[18])
                    # img erstellen
                    self.img_id[17] = self.canvas.create_image(
                        360, 415, image=self.img[4]
                    )
                    self.img_id[16] = self.canvas.create_image(
                        305, 415, image=self.img[0]
                    )
                # unterscheiden in castling for oder zurück animation
                else:
                    self.canvas.delete(self.img_id[16])
                    self.canvas.delete(self.img_id[17])
                    self.img_id[18] = self.canvas.create_image(
                        415, 415, image=self.img[0]
                    )
                    self.img_id[15] = self.canvas.create_image(
                        250, 415, image=self.img[4]
                    )
            elif pos[0] == "c":  # move nach links
                if bool:
                    self.canvas.delete(self.img_id[11])
                    self.img_id[13] = self.canvas.create_image(
                        140, 415, image=self.img[4]
                    )
                    self.img_id[14] = self.canvas.create_image(
                        195, 415, image=self.img[0]
                    )
                else:
                    self.canvas.delete(self.img_id[13])
                    self.canvas.delete(self.img_id[14])
                    self.img_id[11] = self.canvas.create_image(
                        30, 415, image=self.img[0]
                    )
                    self.img_id[15] = self.canvas.create_image(
                        250, 415, image=self.img[4]
                    )
        elif pos[1] == "8":  # schwarzer König
            if bool:
                self.canvas.delete(self.img_id[85])
            if pos[0] == "g":
                if bool:
                    self.canvas.delete(self.img_id[88])
                    self.img_id[87] = self.canvas.create_image(
                        360, 30, image=self.img[10]
                    )
                    self.img_id[86] = self.canvas.create_image(
                        305, 30, image=self.img[6]
                    )
                else:
                    self.canvas.delete(self.img_id[87])
                    self.canvas.delete(self.img_id[86])
                    self.img_id[88] = self.canvas.create_image(
                        415, 30, image=self.img[6]
                    )
                    self.img_id[85] = self.canvas.create_image(
                        250, 30, image=self.img[10]
                    )
            elif pos[0] == "c":
                if bool:
                    self.canvas.delete(self.img_id[81])
                    self.img_id[83] = self.canvas.create_image(
                        140, 30, image=self.img[10]
                    )
                    self.img_id[84] = self.canvas.create_image(
                        195, 30, image=self.img[6]
                    )
                else:
                    self.canvas.delete((self.img_id[83]))
                    self.canvas.delete((self.img_id[84]))
                    self.img_id[81] = self.canvas.create_image(
                        30, 30, image=self.img[6]
                    )
                    self.img_id[85] = self.canvas.create_image(
                        250, 30, image=self.img[10]
                    )

    """
        Info: Deletes the image of the pawn and displays the image of a queen on the position of pawn promotion. 
        Params: pos = old pawn position, spos = new queen position, bool = black or white side
        Return: None
    """
    def pawnPromo(self, spos, pos, bool):
        if not self.goBackBool:
            self.canvas.delete(self.rect)
            self.ErrorOff()
            self.changeOutput("Zug durchgeführt")
        print(spos[0], spos[1], pos[0], pos[1])

        xppos, yppos = con.Convert().convFiePos(pos[0], pos[1])
        xspos, yspos = con.Convert().convFiePos(spos[0], spos[1])

        self.canvas.delete(self.img_id[pos[1] * 10 + pos[0]])
        self.canvas.delete(self.img_id[spos[1] * 10 + spos[0]])
        if bool:
            if pos[1] == 8:
                self.img_id[pos[1] * 10 + pos[0]] = self.canvas.create_image(
                    xppos, yppos, image=self.img[3]
                )
            else:
                self.img_id[pos[1] * 10 + pos[0]] = self.canvas.create_image(
                    xppos, yppos, image=self.img[9]
                )
        else:
            if pos[1] == 8:
                self.img_id[pos[1] * 10 + pos[0]] = self.canvas.create_image(
                    xppos, yppos, image=self.img[5]
                )
                self.img_id[spos[1] * 10 + spos[0]] = self.canvas.create_image(
                    xspos, yspos, image=self.img[9]
                )
            else:
                print("else")
                self.img_id[pos[1] * 10 + pos[0]] = self.canvas.create_image(
                    xppos, yppos, image=self.img[11]
                )
                self.img_id[spos[1] * 10 + spos[0]] = self.canvas.create_image(
                    xspos, yspos, image=self.img[9]
                )

    """
        Info: Returns the saved array-image-number of a piece so the right one will get displayed. 
        Params: The piece type.
        Return: Array number of image. 
    """
    def getImg(self, piece):
        match str(piece):
            case "R":
                return 0
            case "N":
                return 1
            case "B":
                return 2
            case "Q":
                return 3
            case "K":
                return 4
            case "P":
                return 5
            case "r":
                return 6
            case "n":
                return 7
            case "b":
                return 8
            case "q":
                return 9
            case "k":
                return 10
            case "p":
                return 11
        print("Error getImg")

    ''' Visual Feedback when the move is illegal. '''
    def illegalMove(self):
        self.ErrorOn()
        self.changeOutput("Zug nicht Möglich")
        return

    ''' Visual Feedback when the king is in check. '''
    def check(self, string):
        self.ErrorOn()
        self.changeOutput(string)
        return

    ''' Visual feedback when checkmate is detected. '''
    def checkMate(self):
        self.ErrorOn()
        self.changeOutput("Schachmatt, Spiel vorbei")
        return

    ''' Visual feedback when a draw is detected. '''
    def staleMate(self):
        self.ErrorOn()
        self.changeOutput("Remis, Spiel vorbei")
        return

    ''' Create all chess pieces on the board;
    they are addressed by their array position, so [1 1] == A1 as a position on the board. '''
    def createImgs(self):
        self.img = [
            None,  # RookW     0
            None,  # KnightW   1
            None,  # BishopW   2
            None,  # QueenW    3
            None,  # KingW     4
            None,  # PawnW     5
            None,  # RookB     6
            None,  # KnightB   7
            None,  # BishopB   8
            None,  # QueenB    9
            None,  # KingB     10
            None,  # PawnB     11
        ]

        # Speicher Initialisieren Felder von 11 bis 18 bis 81 bis 88
        self.img_id = []
        for i in range(0, 89):
            self.img_id.append(None)
        print(len(self.img_id))

        ################################################################################################################
        # Erstellen der weißen Figuren
        rook_w = (
            Image.open(self.abs_path + "rook_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[0] = ImageTk.PhotoImage(rook_w)
        self.img_id[11] = self.canvas.create_image(30, 415, image=self.img[0])
        self.img_id[18] = self.canvas.create_image(415, 415, image=self.img[0])

        knight_w = (
            Image.open(self.abs_path + "knight_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[1] = ImageTk.PhotoImage(knight_w)
        self.img_id[12] = self.canvas.create_image(85, 415, image=self.img[1])
        self.img_id[17] = self.canvas.create_image(360, 415, image=self.img[1])

        bishop_w = (
            Image.open(self.abs_path + "bishop_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[2] = ImageTk.PhotoImage(bishop_w)
        self.img_id[13] = self.canvas.create_image(140, 415, image=self.img[2])
        self.img_id[16] = self.canvas.create_image(305, 415, image=self.img[2])

        queen_w = (
            Image.open(self.abs_path + "queen_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[3] = ImageTk.PhotoImage(queen_w)
        self.img_id[14] = self.canvas.create_image(195, 415, image=self.img[3])

        king_w = (
            Image.open(self.abs_path + "king_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[4] = ImageTk.PhotoImage(king_w)
        self.img_id[15] = self.canvas.create_image(250, 415, image=self.img[4])

        pawn_w = (
            Image.open(self.abs_path + "pawn_w.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[5] = ImageTk.PhotoImage(pawn_w)
        for i in range(0, 8):
            self.img_id[i + 21] = self.canvas.create_image(
                30 + i * 55, 360, image=self.img[5]
            )
        ################################################################################################################
        # Erstellen der schwarzen Figuren
        rook_b = (
            Image.open(self.abs_path + "rook_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[6] = ImageTk.PhotoImage(rook_b)
        self.img_id[81] = self.canvas.create_image(30, 30, image=self.img[6])
        self.img_id[88] = self.canvas.create_image(415, 30, image=self.img[6])

        knight_b = (
            Image.open(self.abs_path + "knight_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[7] = ImageTk.PhotoImage(knight_b)
        self.img_id[82] = self.canvas.create_image(85, 30, image=self.img[7])
        self.img_id[87] = self.canvas.create_image(360, 30, image=self.img[7])

        bishop_b = (
            Image.open(self.abs_path + "bishop_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[8] = ImageTk.PhotoImage(bishop_b)
        self.img_id[83] = self.canvas.create_image(140, 30, image=self.img[8])
        self.img_id[86] = self.canvas.create_image(305, 30, image=self.img[8])

        queen_b = (
            Image.open(self.abs_path + "queen_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[9] = ImageTk.PhotoImage(queen_b)
        self.img_id[84] = self.canvas.create_image(195, 30, image=self.img[9])

        king_b = (
            Image.open(self.abs_path + "king_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[10] = ImageTk.PhotoImage(king_b)
        self.img_id[85] = self.canvas.create_image(250, 30, image=self.img[10])

        pawn_b = (
            Image.open(self.abs_path + "pawn_b.png")
            .resize((55, 55), Image.ANTIALIAS)
            .convert("RGBA")
        )
        self.img[11] = ImageTk.PhotoImage(pawn_b)
        for i in range(0, 8):
            self.img_id[i + 71] = self.canvas.create_image(
                30 + i * 55, 85, image=self.img[11]
            )
