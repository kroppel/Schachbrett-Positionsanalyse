class Figuren:
    def __init__(self, id, seite, x, y):
        self.id = id
        self.seite = seite
        self.posX = x
        self.posY = y
        self.active = True

    def getPos(self):
        return self.posX, self.posY

    def getID(self):
        return self.id

    def setPos(self, x, y):
        self.posX = x
        self.posY = y

    def delFig(self):
        self.active = False

    def createFig(self):
        # Vergabe der IDS wie folgt (weiße Figuren unten):
        # 25 26 27 28 29 30 31 32
        # 17 18 19 20 21 22 23 24
        #
        #
        #  9 10 11 12 13 14 15 16
        #  1  2  3  4  5  6  7  8

        self.figures_black = [
            Pawn(17, "b", 1, 7),
            Pawn(18, "b", 2, 7),
            Pawn(19, "b", 3, 7),
            Pawn(20, "b", 4, 7),
            Pawn(21, "b", 5, 7),
            Pawn(22, "b", 6, 7),
            Pawn(23, "b", 7, 7),
            Pawn(24, "b", 8, 7),
            Rook(25, "b", 1, 8),
            Knight(26, "b", 2, 8),
            Bishop(27, "b", 3, 8),
            Queen(28, "b", 4, 8),
            King(29, "b", 5, 8),
            Bishop(30, "b", 6, 8),
            Knight(31, "b", 7, 8),
            Rook(32, "b", 8, 8),
        ]
        self.figures_white = [
            Rook(1, "w", 1, 1),
            Knight(2, "w", 2, 1),
            Bishop(3, "w", 3, 1),
            Queen(4, "w", 4, 1),
            King(5, "w", 5, 1),
            Bishop(6, "w", 6, 1),
            Knight(7, "w", 7, 1),
            Rook(8, "w", 8, 1),
            Pawn(9, "w", 1, 2),
            Pawn(10, "w", 2, 2),
            Pawn(11, "w", 3, 2),
            Pawn(12, "w", 4, 2),
            Pawn(13, "w", 5, 2),
            Pawn(14, "w", 6, 2),
            Pawn(15, "w", 7, 2),
            Pawn(16, "w", 8, 2),
        ]

    def getLists(self):
        return self.figures_black, self.figures_white


class King(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    # König kann in alle Richtungen 1ne  Position weiterrücken
    # heißt solange sich x und x old sowie y und y old um 1 unterscheiden ist ok
    def Zug(self, x, y):
        if 0 <= abs(self.posX - x) <= 1 | 0 <= abs(self.posY - y) <= 1:
            return True
        return False


class Queen(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    # Königin setzt sich aus Bishop or Rook zusammen
    def Zug(self, x, y):
        if (abs(self.x - x) == abs(self.y - y)) | (
            (self.x == x & self.y != y) | (self.x != x & self.y == y)
        ):
            return True
        return False


class Rook(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    # Turm darf nur horizontal oder vertikal bewegt werden
    def Zug(self, x, y):
        if (self.x == x & self.y != y) | (self.x != x & self.y == y):
            return True
        return False


class Knight(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    def Zug(self, x, y):
        if (abs(self.x - x) == 1 & abs(self.y - y) == 2) | (
            abs(self.x - x) == 2 & abs(self.y - y) == 1
        ):
            return True
        return False


class Bishop(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    # darf sich nur auf der Diagonalen Bewegen
    def Zug(self, x, y):
        if abs(self.posX - x) == abs(self.y - y):
            return True
        return False


class Pawn(Figuren):
    def __init__(self, id, seite, posx, posy):
        super().__init__(id, seite, posx, posy)

    # wenn er schlagen will, muss er +1 +1, wenn nicht einfach 0 +1
    # jedoch abhängig von den Seiten wo er hin darf -->
    def Zug(self, x, y, schlagen, Seite, Runde):
        if Seite == "white":
            if schlagen & (abs(self.posX - x) == 1 & self.posY - y == -1):
                return True
            elif (not schlagen) & Runde <= 2 & self.posX == x & self.posY - y == -2:
                return True
            elif (not schlagen) & self.posX == x & self.posY - y == -1:
                return True
        if Seite == "black":
            if schlagen & (abs(self.posX - x) == 1 & self.posY - y == 1):
                return True
            elif ((not schlagen) & Runde <= 2) & (
                (self.posX == x) & (self.posY - y == 2)
            ):
                return True
            elif (not schlagen) & self.posX == x & self.posY - y == 1:
                return True
        return False
