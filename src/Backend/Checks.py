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

    def checkSchach(self):
        # Wir machen Folgendes: Wir gehen jeweils alle Figuren der gegnerischen Seite durch und checken beim Beenden des
        # gegnerischen Zuges, ob es ein legitimer Zug wäre, wenn sie als Nächstes auf das Feld des Königs ziehen,
        # wenn es für alle Figuren False zurück gibt, ist er nicht im Schach, ansonsten schon.

        # Weiß ist am Zug
        if (self.Runde % 2) == 1:
            # aktuelle Position des Weißen Königs ermitteln
            posX, posY = self.figures_white[4].getPos()
            # Prüfen alle Schwarzen auf Pos von weißem König
            for i in range(0, len(self.figures_black)):
                if 8 > i:
                    answer, arr = self.figures_black[i].Zug(posX, posY, True, "black")
                else:
                    answer, arr = self.figures_black[i].Zug(posX, posY)
                if answer:
                    Schach = True
                    break
                else:
                    Schach = False

        # Schwarz ist am Zug
        if (self.Runde % 2) == 0:
            # aktuelle Position des Weißen Königs ermitteln
            posX, posY = self.figures_white[4].getPos()
            # Prüfen alle Schwarzen auf Pos von weißem König
            for i in range(0, len(self.figures_white)):
                if 8 < i:
                    answer, arr = self.figures_white[i].Zug(posX, posY, True, "white")
                else:
                    answer, arr = self.figures_white[i].Zug(posX, posY)
                if answer:
                    Schach = True
                    break
                else:
                    Schach = False
        return Schach

    def checkPinned(self):
        return

    # überprüft die Legitimität des Zuges
    def checkZug(self, schlagen):
        bauer = 0
        if self.saveid < 16:
            # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
            if 7 < self.save_figure_num:
                answer, arr = self.figures_white[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "white"
                )
                bauer = 1
            else:
                answer, arr = self.figures_white[self.save_figure_num].Zug(self.posX, self.posY)
        else:
            if 8 > self.save_figure_num:
                answer, arr = self.figures_black[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "black"
                )
                bauer = 2
            else:
                answer, arr = self.figures_black[self.save_figure_num].Zug(self.posX, self.posY)

        # gibt erst einen bool wert zurück, dann gibt es 3 Optionen:
        # 1. wenn answer = False, dann soll auch hier sofort false ausgegeben werden
        if not answer:
            return False
        # 2. Wenn answer = True, dann gibt es ein array was mitgegeben wird,
        # 2.1 Wenn dieses array leer ist, dann handelt es sich um den König, den Bauern oder das Pferd, welche nur 1 Feld Züge
        # machen können oder über Figuren Springen dürfen, dann ist die Rückgabe True
        elif answer & (len(arr) == 0):
            return True
        # 2.2 Ansonsten handelt es sich um einen größeren Zug, bei dem Figuren dazwischen stehen könnten
        # bis auf die erste und letze Stelle soll dieses überprüft werden, ob es ein Feld gibt, auf dem eine Figur steht
        else:
            print(arr)
            bool = True
            # gehe das ganze Array durch,
            for i in range(1, len(arr)):
                # checke bei jeder Position, ob eine Figur darauf steht:
                pos = (arr[i][0], arr[i][1])
                print(arr[i])
                if (self.checkLists(pos, False)):
                    bool = False
                    break
            # nur wenn keine Figur erkannt wurde muss die spezielle Variable, die für den Bauern eingebaut wurde,
            # damit man unterscheiden kann, ob er 2 Felder springen darf, aktiviert werden
            if bool and (bauer != 0):
                if bauer == 1:
                    self.figures_white[self.save_figure_num].moved()
                else:
                    self.figures_black[self.save_figure_num].moved()
            return bool

    # gibt für das Backtracking die ID zurück und ändert die Position
    def returnID(self, Position, newPos):
        for i in range(0, 16):
            # wenn du eine Figure mit der gleichen Position findest
            if (self.figures_black[i].getPos() == Position) & (self.figures_black[i].getActive() is True):
                id = self.figures_black[i].getID()
                self.figures_black[i].setPos(newPos[0], newPos[1])
                return id
            if (self.figures_white[i].getPos() == Position) & (self.figures_white[i].getActive() is True):
                id = self.figures_white[i].getID()
                self.figures_white[i].setPos(newPos[0], newPos[1])
                return id
        return None


    # geht die Liste durch und schaut, ob für die Position eine Figur erkannt wurde
    def checkLists(self, Position, Bool):
        # gehe die Listen durch
        for i in range(0, 16):
            # wenn du eine Figure mit der gleichen Position findest
            if (self.figures_black[i].getPos() == Position) & (self.figures_black[i].getActive() is True):
                if Bool:
                    self.id = self.figures_black[i].getID()
                    self.figure_num = i
                    print("Schwarze Figur erkannt", self.id)
                else:
                    print("Figur erkannt")
                return True
            if (self.figures_white[i].getPos() == Position) & (self.figures_white[i].getActive() is True):
                if Bool:
                    self.id = self.figures_white[i].getID()
                    self.figure_num = i
                    print("Weiße Figur erkannt", self.id)
                else:
                    print("Figur erkannt")
                return True
        return False

    def checkFigure(self, x, y, gui):
        self.id = None
        # lade die Listen
        self.figures_black, self.figures_white = gui.getfigLists()

        # wandle zuerst die x und y koordinaten in die zugehörige Feldposition um
        self.Position = self.con.convPosFie(x, y)
        self.posX, self.posY = self.Position

        # schaue, ob auf der Position eine Figur steht
        self.checkLists(self.Position, True)

        # Es folgt das Unterscheiden in 3 mögliche Fälle
        ################################################################################################################
        # 1. Eine Figur wurde ausgewählt (kennzeichnend dafür: Es wurde eine ID erkannt und keine alte gespeichert)

        if (not self.id is None) & (self.saveid is None):
            # jetzt schaut er erst einmal, welche Farbe aktuell dran ist und dementsprechend rücken darf
            if((self.Runde % 2 == 1) & (self.id < 17)) | ((self.Runde%2 == 0) & (self.id > 16)):
                gui.ErrorOff()
                gui.changeOutput("Klicke auf das Zielfeld")
                self.erkannt = True
                # speichern der alten ID
                self.saveid = self.id
                self.save_figure_num = self.figure_num
                x, y = self.con.convFiePos(self.posX, self.posY)
                self.rect = gui.canvas.create_rectangle(x-28, y-28, x+28, y+28, width=2, outline="#04d9ff")
                return
            else:
                if(self.Runde%2 == 1):
                    gui.changeOutput("Weiß ist am Zug, nicht schwarz")
                    gui.ErrorOn()
                else:
                    gui.changeOutput("Schwarz ist am Zug, nicht weiß")
                    gui.ErrorOn()
                return

        ################################################################################################################
        # 2. Eine Figur wird gezogen (kz.: Eine Figur ist gespeichert aber keine neue wurde erkannt)

        if (self.id is None) & (not self.saveid is None):
            # Überprüfen, ob der Zug möglich ist
            print(self.saveid)
            if self.checkZug(False) is True:
                gui.changeOutput("Zug erkannt, Figur wird gerückt")
                gui.ErrorOff()

                # ändern der Position der gerückten Figur
                if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                    posvor = self.figures_white[self.save_figure_num].getPos()
                    self.figures_white[self.save_figure_num].setPos(self.posX, self.posY)
                else:  # schwarze Figur, ändern in der schwarzen Liste
                    posvor = self.figures_black[self.save_figure_num].getPos()
                    self.figures_black[self.save_figure_num].setPos(self.posX, self.posY)

                # löschen des Markers
                gui.canvas.delete(self.rect)

                # das Bild der Figur auf die neue Position setzen
                gui.switchImgofFigur(self.posX, self.posY, self.saveid)

                # ausgewählte Figur nun nicht mehr ausgewählt
                self.saveid = None
                self.save_figure_num = None

                # gültigen Zug in Listbox eintragen
                gui.insertItemInList(posvor[0], posvor[1], self.posX, self.posY)

                # Zug vollendet eine neue Runde Beginnt
                self.Runde += 1

            else:
                gui.changeOutput("Zug nicht möglich, wähle ein anderes Feld")
                gui.ErrorOn()

            return

        ################################################################################################################
        # 3. Eine andere Figur wurde ausgewählt (2 extra Fälle: gegner oder eigene Figur)
        # (kz: Es wurde eine Figur gespeichert und eine neue erkannt)

        if (not self.id is None) & (not self.saveid is None):
            # überprüfe, ob eine eigene andere Figur ausgewählt wurde, in dem Fall wären beide IDs sowohl vorherige,
            # als auch nachfolgende entweder im Bereich 1 bis 16 oder 17 bis 32
            if ((self.id < 17) & (self.saveid < 17)) | ((self.id > 16) & (self.saveid > 16)):
                gui.changeOutput("Eigene andere Figur")

                # löschen des alten Figur-Markers
                gui.canvas.delete(self.rect)

                # erstellen des neuen Markers
                x, y = self.con.convFiePos(self.posX, self.posY)
                self.rect = gui.canvas.create_rectangle(x - 28, y - 28, x + 28, y + 28, width=2, outline="#04d9ff")

                # die neue Figur speichern als Ausgangspunkt für den nächsten Klick
                self.saveid = self.id
                self.save_figure_num = self.figure_num

                # Es folgt kein Runden inkrement, da die aktuelle Farbe noch dran ist
                return
            # ansonsten soll eine gegnerische Figur geschlagen werden
            else:
                # Schlagen unterscheidet sich bei den meisten Figuren nicht von ziehen
                if self.checkZug(True) is True:
                    # print("Andere Figur schlagen",self.id, self.saveid, self.posX, self.posY)
                    gui.changeOutput("Andere Figur geschlagen")

                    # löschen des Markers
                    gui.canvas.delete(self.rect)

                    # ändern der Position der schlagenden Figur
                    if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                        self.figures_white[self.save_figure_num].setPos(self.posX, self.posY)
                    else:  # schwarze Figur, ändern in der schwarzen Liste
                        self.figures_black[self.save_figure_num].setPos(self.posX, self.posY)

                    # deaktivieren(verkleinern der neuen Figur
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
                    gui.changeOutput("Schlagen nicht möglich")
                return
        # ID Fehler beim Schlagen bzw der ID Bilder
        ################################################################################################################
        # 4. Es wird ein Feld geklickt, aber vorher wurde keine Figur ausgewählt (kz.: Keine gespeichert oder erkannt)

        if (self.id is None) & (self.saveid is None):
            gui.changeOutput("Wähle eine Figur aus")
            return
