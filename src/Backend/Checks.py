import src.Backend.Convert as conv
import src.Backend.Figuren as fig


class Checks:
    def __init__(self):
        self.con = conv.Convert()
        self.saveid = None
        self.id = None
        self.Runde = 1
        return

    def checkSchach(self):
        return

    def checkSchlagen(self):
        return

    def checkRochade(self):
        return

    def checkRemis(self):
        return

    def checkEnpassant(self):
        return

    def checkSchachmatt(self):
        return

    def checkPinned(self):
        return

    def checkZug(self):
        print(self.saveid)
        if self.saveid < 16:
            # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
            if 8 > self.figure_num:
                answer = self.figures_white[self.figure_num].Zug(
                    self.posX, self.posY, False, "white", self.Runde
                )
            else:
                answer = self.figures_white[self.figure_num].Zug(self.posX, self.posY)
        else:
            if 8 > self.figure_num:
                answer = self.figures_black[self.figure_num].Zug(
                    self.posX, self.posY, False, "black", self.Runde
                )
            else:
                answer = self.figures_black[self.figure_num].Zug(self.posX, self.posY)
        return answer

    def checkLists(self):
        # gehe die Listen durch
        for i in range(0, 16):
            # wenn du eine Figure mit der gleichen Position findest
            if self.figures_black[i].getPos() == self.Position:
                self.id = self.figures_black[i].getID()
                self.figure_num = i
                print("Schwarze Figur erkannt", self.id)
                break
            if self.figures_white[i].getPos() == self.Position:
                self.id = self.figures_white[i].getID()
                self.figure_num = i
                print("Weiße Figur erkannt", self.id)
                break

    def checkFigure(self, x, y, gui):
        self.id = None
        # lade die Listen
        self.figures_black, self.figures_white = gui.getfigLists()

        # wandle zuerst die x und y koordinaten in die zugehörige Feldposition um
        self.Position = self.con.convPosFie(x, y)
        self.posX, self.posY = self.Position

        # schaue, ob auf der Position eine Figur steht
        self.checkLists()

        # wenn eine id erkannt wurde und vorher keine Figur ausgewählt war, wurde gerade eine Figur ausgewählt
        if (not self.id is None) & (self.saveid is None):
            self.erkannt = True
            # speichern der alten ID
            self.saveid = self.id
            print("Klicke auf das Zielfeld")
            return

        # wenn eine id erkannt und bereits Figur ausgewählt, dann soll neue id Figur geschlagen werden
        if (not self.id is None) & (not self.saveid is None):
            print("Schlagen muss noch implementiert werden")
            return

        # wenn keine id erkannt und bereits Figur ausgewählt, dann soll alte id Figur auf neues Feld gerückt werden
        if (self.id is None) & (not self.saveid is None):
            if self.checkZug() is True:
                if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                    self.figures_white[self.figure_num].setPos(self.posX, self.posY)
                else:  # schwarze Figur, ändern in der schwarzen Liste
                    self.figures_black[self.figure_num].setPos(self.posX, self.posY)
                print("Ziel erkannt, Figur wird gerückt")
                gui.switchImgofFigur(self.posX, self.posY, self.saveid)
                self.saveid = None
                self.Runde += 1
            else:
                print("Zug nicht möglich, wähle ein anderes Feld")
            return

        # wenn keine id erkannt und keine Figur ausgewählt
        if (self.id is None) & (self.saveid is None):
            print("Wähle eine Figur aus")
            return
