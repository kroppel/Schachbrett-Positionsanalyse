class Figuren:
    def __init__(self, id, seite, x, y, value):
        self.id = id
        self.seite = seite
        self.posX = x
        self.posY = y
        self.active = True
        self.value = value

    def printAll(self, x, y):
        print("############\nFigur: ", self.id, "\n", self.posX, self.posY, x, y)

    def getPos(self):
        return self.posX, self.posY

    def getValue(self):
        return self.value

    def getID(self):
        return self.id

    def setPos(self, x, y):
        self.posX = x
        self.posY = y

    def delFig(self):
        self.active = False

    def getActive(self):
        return self.active

    def createFig(self):
        # Vergabe der IDS wie folgt (weiße Figuren unten):
        # 25 26 27 28 29 30 31 32
        # 17 18 19 20 21 22 23 24
        #
        #
        #  9 10 11 12 13 14 15 16
        #  1  2  3  4  5  6  7  8

        self.figures_black = [
            Pawn(17, "b", 1, 7, 1),
            Pawn(18, "b", 2, 7, 1),
            Pawn(19, "b", 3, 7, 1),
            Pawn(20, "b", 4, 7, 1),
            Pawn(21, "b", 5, 7, 1),
            Pawn(22, "b", 6, 7, 1),
            Pawn(23, "b", 7, 7, 1),
            Pawn(24, "b", 8, 7, 1),
            Rook(25, "b", 1, 8, 5),
            Knight(26, "b", 2, 8, 3),
            Bishop(27, "b", 3, 8, 3),
            Queen(28, "b", 4, 8, 9),
            King(29, "b", 5, 8, 0),
            Bishop(30, "b", 6, 8, 3),
            Knight(31, "b", 7, 8, 3),
            Rook(32, "b", 8, 8, 5),
        ]
        self.figures_white = [
            Rook(1, "w", 1, 1, 5),
            Knight(2, "w", 2, 1, 3),
            Bishop(3, "w", 3, 1, 3),
            Queen(4, "w", 4, 1, 9),
            King(5, "w", 5, 1, 0),
            Bishop(6, "w", 6, 1, 3),
            Knight(7, "w", 7, 1, 3),
            Rook(8, "w", 8, 1, 5),
            Pawn(9, "w", 1, 2, 1),
            Pawn(10, "w", 2, 2, 1),
            Pawn(11, "w", 3, 2, 1),
            Pawn(12, "w", 4, 2, 1),
            Pawn(13, "w", 5, 2, 1),
            Pawn(14, "w", 6, 2, 1),
            Pawn(15, "w", 7, 2, 1),
            Pawn(16, "w", 8, 2, 1),
        ]

    def getLists(self):
        return self.figures_black, self.figures_white


class King(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)

    # König kann in alle Richtungen 1ne Position weiterrücken heißt,
    # solange sich x und x old sowie y und y old um 1 unterscheiden ist ok
    def Zug(self, x, y):
        self.printAll(x, y)
        if (0 <= abs(self.posX - x) <= 1) | (0 <= abs(self.posY - y) <= 1):
            return True
        return False


class Queen(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)

    # Königin setzt sich aus Bishop or Rook zusammen
    def Zug(self, x, y):
        self.printAll(x, y)
        if (abs(self.posX - x) == (abs(self.posY - y))) | (
            ((self.posX == x) & (self.posY != y)) | ((self.posX != x) & (self.posY == y))):
            return True
        return False


class Rook(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)

    # Turm darf nur horizontal oder vertikal bewegt werden
    def Zug(self, x, y):
        self.printAll(x, y)
        if ((self.posX == x) & (self.posY != y)) | ((self.posX != x) & (self.posY == y)):
            return True
        return False


class Knight(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)

    def Zug(self, x, y):
        self.printAll(x, y)
        if ((abs(self.posX - x) == 1) & (abs(self.posY - y) == 2)) | (
                ((abs(self.posX - x)) == 2) & (abs(self.posY - y) == 1)):
            return True
        return False


class Bishop(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)

    # darf sich nur auf der Diagonalen Bewegen
    def Zug(self, x, y):
        self.printAll(x, y)
        if abs(self.posX - x) == abs(self.posY - y):
            return True
        return False


class Pawn(Figuren):
    def __init__(self, id, seite, posx, posy, value):
        super().__init__(id, seite, posx, posy, value)
        self.moved = False

    # wenn er schlagen will, muss er +1 +1, wenn nicht einfach 0 +1
    # jedoch abhängig von den Seiten wo er hin darf -->
    def Zug(self, x, y, schlagen, Seite):
        self.printAll(x, y)
        if Seite == "white":
            if schlagen & ((abs(self.posX - x)) == 1) & (self.posY - y == -1):
                self.moved = True
                return True
            elif ((not schlagen) & (not self.moved)) & ((self.posX == x) & ((self.posY - y == -2) | (self.posY - y == -1))):
                self.moved = True
                return True
            elif (not schlagen) & (self.posX == x) & (self.posY - y == -1):
                return True
        if Seite == "black":
            if schlagen & ((abs(self.posX - x)) == 1) & (self.posY - y == 1):
                self.moved = True
                return True
            elif ((not schlagen) & (not self.moved)) & ((self.posX == x) & ((self.posY - y == 2)|(self.posY - y == 1))):
                self.moved = True
                return True
            elif ((not schlagen) & (self.posX == x)) & (self.posY - y == 1):
                return True
        return False
