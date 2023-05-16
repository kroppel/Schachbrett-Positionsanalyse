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

    # überprüft die Legitimität des Zuges
    def checkZug(self, schlagen):
        if self.saveid < 16:
            # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
            if 8 < self.save_figure_num:
                answer = self.figures_white[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "white"
                )
            else:
                answer = self.figures_white[self.save_figure_num].Zug(self.posX, self.posY)
        else:
            if 8 > self.save_figure_num:
                answer = self.figures_black[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "black"
                )
            else:
                answer = self.figures_black[self.save_figure_num].Zug(self.posX, self.posY)
        return answer

    # geht die Liste durch und schaut, ob für die Position eine Figur erkannt wurde
    def checkLists(self):
        # gehe die Listen durch
        for i in range(0, 16):
            # wenn du eine Figure mit der gleichen Position findest
            if (self.figures_black[i].getPos() == self.Position) & (self.figures_black[i].getActive() is True):
                self.id = self.figures_black[i].getID()
                self.figure_num = i
                print("Schwarze Figur erkannt", self.id)
                break
            if (self.figures_white[i].getPos() == self.Position) & (self.figures_white[i].getActive() is True):
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

        # Es folgt das Unterscheiden in 3 mögliche Fälle
        ################################################################################################################
        # 1. Eine Figur wurde ausgewählt (kennzeichnend dafür: Es wurde eine ID erkannt und keine alte gespeichert)

        if (not self.id is None) & (self.saveid is None):
            # jetzt schaut er erst einmal, welche Farbe aktuell dran ist und dementsprechend rücken darf
            if((self.Runde % 2 == 1) & (self.id < 17)) | ((self.Runde%2 == 0) & (self.id > 16)):
                self.erkannt = True
                # speichern der alten ID
                self.saveid = self.id
                self.save_figure_num = self.figure_num
                print("Klicke auf das Zielfeld")
                x, y = self.con.convFiePos(self.posX, self.posY)
                self.rect = gui.canvas.create_rectangle(x-28, y-28, x+28, y+28, width=2, outline="#04d9ff")
                return
            else:
                if(self.Runde%2 == 1):
                    print("Weiß ist am Zug, nicht schwarz")
                else:
                    print("Schwarz ist am Zug nicht weiß")
                return

        ################################################################################################################
        # 2. Eine Figur wird gezogen (kz.: Eine Figur ist gespeichert aber keine neue wurde erkannt)

        if (self.id is None) & (not self.saveid is None):
            # Überprüfen, ob der Zug möglich ist
            if self.checkZug(False) is True:
                print("Ziel erkannt, Figur wird gerückt")

                # ändern der Position der gerückten Figur
                if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                    self.figures_white[self.save_figure_num].setPos(self.posX, self.posY)
                else:  # schwarze Figur, ändern in der schwarzen Liste
                    self.figures_black[self.save_figure_num].setPos(self.posX, self.posY)

                # löschen des Markers
                gui.canvas.delete(self.rect)

                # das Bild der Figur auf die neue Position setzen
                gui.switchImgofFigur(self.posX, self.posY, self.saveid)

                # ausgewählte Figur nun nicht mehr ausgewählt
                self.saveid = None
                self.save_figure_num = None

                # Zug vollendet eine neue Runde Beginnt
                self.Runde += 1

            else:
                print("Zug nicht möglich, wähle ein anderes Feld")

            return

        ################################################################################################################
        # 3. Eine andere Figur wurde ausgewählt (2 extra Fälle: gegner oder eigene Figur)
        # (kz: Es wurde eine Figur gespeichert und eine neue erkannt)

        if (not self.id is None) & (not self.saveid is None):
            # überprüfe, ob eine eigene andere Figur ausgewählt wurde, in dem Fall wären beide IDs sowohl vorherige,
            # als auch nachfolgende entweder im Bereich 1 bis 16 oder 17 bis 32
            if ((self.id < 17) & (self.saveid < 17)) | ((self.id > 16) & (self.saveid > 16)):
                print("Eigene andere Figur ", self.id)

                # löschen des alten Figur-Markers
                gui.canvas.delete(self.rect)

                # erstellen des neuen Markers
                x, y = self.con.convFiePos(self.posX, self.posY)
                self.rect = gui.canvas.create_rectangle(x - 28, y - 28, x + 28, y + 28, width=2, outline="#04d9ff")

                # die neue Figur speichern als Ausgangspunkt für den nächsten Klick
                self.saveid = self.id

                # Es folgt kein Runden inkrement, da die aktuelle Farbe noch dran ist
                return
            # ansonsten soll eine gegnerische Figur geschlagen werden
            else:
                # Schlagen unterscheidet sich bei den meisten Figuren nicht von ziehen
                if self.checkZug(True) is True:
                    print("Andere Figur schlagen",self.id, self.saveid, self.posX, self.posY)

                    # löschen des Markers
                    gui.canvas.delete(self.rect)

                    # ändern der Position der schlagenden Figur
                    if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                        self.figures_white[self.save_figure_num].setPos(self.posX, self.posY)
                    else:  # schwarze Figur, ändern in der schwarzen Liste
                        self.figures_black[self.save_figure_num].setPos(self.posX, self.posY)

                    # deaktivieren der neuen Figur
                    if self.id < 17:  # weiße Figur, ändern in der weißen Liste
                        self.figures_white[self.figure_num].delFig()
                    else:  # schwarze Figur, ändern in der schwarzen Liste
                        self.figures_black[self.figure_num].delFig()

                    # abändern des Bildes
                    gui.switchImgofFigur(self.posX, self.posY, self.saveid)
                    gui.loescheImgofFigur(self.id)

                    # Es folgt ein Runden inkrement, da nun gegnerische Farbe antwortet auf vorherigen Zug
                    self.Runde += 1

                    # Auswahl gelöscht
                    self.saveid = None
                    self.save_figure_num = None
                else:
                    print("Schlagen nicht möglich")
                return
        # ID Fehler beim Schlagen bzw der ID Bilder
        ################################################################################################################
        # 4. Es wird ein Feld geklickt, aber vorher wurde keine Figur ausgewählt (kz.: Keine gespeichert oder erkannt)

        if (self.id is None) & (self.saveid is None):
            print("Wähle eine Figur aus")
            return