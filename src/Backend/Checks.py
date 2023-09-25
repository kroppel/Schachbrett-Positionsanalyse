import Backend.Convert as conv
import Backend.Figuren as fig


class Checks:
    def __init__(self):
        self.con = conv.Convert()
        self.saveid = None
        self.id = None
        self.Runde = 1
        self.beendet = False
        return

    def idToPos(self, id):  # gibt die einer Figur zugehörige aktuelle Position wieder
        if id < 17:
            return self.figures_white[id - 1].getPos()
        else:
            return self.figures_black[id - 17].getPos()

    def checkRochade(self):
        return

    def checkEnpassant(self):
        return

    def getFigure(self, id):
        if id > 17:
            return self.figures_black[id - 17].retSelf()
        else:
            return self.figures_white[id].retSelf()

    ########################################################################################################################
    def checkGedeckt(self, pos):
        # wenn eine Figur oder ein Feld von einer gegnerischen Figur gedeckt wird, kann der König sie nicht schlagen bzw
        # dort hinziehen, um zu schauen, ob eine Figur gedeckt wird, muss man alle Figuren der gleich Farbe durchgehen
        # und schauen, ob ihr nächster Zug auf der Position enden könnte.

        # print(self.saveid, pos[0], pos[1])

        # wenn schwarzer König, dann kontrollieren wir die Weißen, ob das Feld gedeckt wird
        if self.saveid == 29:
            # print("Schwarzer König wird geprüft")
            for i in range(0, 16):
                # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
                if 7 < i:
                    answer, arr = self.figures_white[i].Zug(
                        pos[0], pos[1], True, "white"
                    )
                else:
                    answer, arr = self.figures_white[i].Zug(pos[0], pos[1])
                # überprüfen der Antwort und des Arrays dazwischen
                if (
                    answer
                    & self.checkRoomBetween(arr)
                    & self.figures_white[i].getActive()
                ):
                    break
                else:
                    answer = False
        elif self.saveid == 5:
            # print("Weißer König wird geprüft")
            for i in range(0, 16):
                if 8 > i:
                    answer, arr = self.figures_black[i].Zug(
                        pos[0], pos[1], True, "black"
                    )
                else:
                    answer, arr = self.figures_black[i].Zug(pos[0], pos[1])
                    # überprüfen der Antwort und des Arrays dazwischen
                if (
                    answer
                    & self.checkRoomBetween(arr)
                    & self.figures_black[i].getActive()
                ):
                    break
                else:
                    answer = False
        else:
            print("Error checkGedeckt")

        # print("Prüfung ergab ", answer)

        # überprüfung fertig
        return answer

    ########################################################################################################################
    # überprüft auf Schach
    def checkSchach(self, gui):
        # print("Check Schach")
        # überprüfen beide Könige, ob sie "gedeckt" werden von einer gegnerischen Figur
        w_könig_pos = self.idToPos(5)
        self.saveid = 5
        if self.checkGedeckt(w_könig_pos):
            print("Weißer König im Schach")
            gui.ErrorOn()
            gui.changeOutput("Weißer König im Schach")
            if self.checkMate(w_könig_pos):
                gui.changeOutput("Weiß Matt, Spiel vorbei, Schwarz hat gewonnen !!")
        else:
            s_könig_pos = self.idToPos(29)
            self.saveid = 29
            if self.checkGedeckt(s_könig_pos):
                print("Schwarzer König im Schach")
                gui.ErrorOn()
                gui.changeOutput("Schwarzer König im Schach")
                if self.checkMate(s_könig_pos):
                    gui.changeOutput("Schwarz Matt, Spiel vorbei, Weiß hat gewonnen !!")

        self.saveid = None

    def checkRemis(self):
        return

    # überprüft, ob Schachsetzende Figur geschlagen werden kann
    def checkSchlagen(self, pos):
        # wenn schwarzer König, dann gehen wir alle schwarzen durch, ob sie die weiße Bedrohung schlagen können
        if self.saveid == 29:
            for i in range(0, 16):
                # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
                if i != 12:
                    if 8 > i:
                        answer, arr = self.figures_black[i].Zug(
                            pos[0], pos[1], True, "white"
                        )
                    else:
                        answer, arr = self.figures_black[i].Zug(pos[0], pos[1])
                    # überprüfen der Antwort und des Arrays dazwischen
                    if (
                        answer
                        & self.checkRoomBetween(arr)
                        & self.figures_black[i].getActive()
                    ):
                        break
                    else:
                        answer = False
        elif self.saveid == 5:
            for i in range(0, 16):
                if i != 4:
                    if 7 < i:
                        answer, arr = self.figures_white[i].Zug(
                            pos[0], pos[1], True, "black"
                        )
                    else:
                        answer, arr = self.figures_white[i].Zug(pos[0], pos[1])
                        # überprüfen der Antwort und des Arrays dazwischen
                    if (
                        answer
                        & self.checkRoomBetween(arr)
                        & self.figures_white[i].getActive()
                    ):
                        break
                    else:
                        answer = False
        return answer

    # überprüft auf Matt
    def checkMate(self, pos):
        # ist genau dann Matt, wenn im Schach und keine Ausweichzüge möglich, ersteres ist durch den Aufruf gegeben
        # daher Array aller umliegender Felder um den König
        x = pos[0]
        y = pos[1]
        arr = [
            [x, y + 1],  # oben
            [x, y - 1],  # unten
            [x - 1, y],  # links
            [x + 1, y],  # rechts
            [x - 1, y + 1],  # oben links
            [x + 1, y + 1],  # oben rechts
            [x - 1, y - 1],  # unten links
            [x + 1, y - 1],  # unten rechts
        ]
        # print(arr)
        bool = False
        # gehe drumherum Raum durch
        for i in range(1, len(arr) - 1):
            # checke bei jeder Position, ob eine Figur darauf steht:
            pos = (arr[i][0], arr[i][1])
            # print(arr[i])
            if not (
                self.checkLists(pos, False)
            ):  # wenn er eine Findet, bei der keine darauf steht
                # dann schaut er, ob diese Position gedeckt wird
                if not self.checkGedeckt(
                    pos
                ):  # wenn sie nicht gedeckt wird, gibt es noch einen Zug für den König
                    # wenn sie gedeckt wird und er keinen anderen Zug hat müssen wir noch überprüfen,
                    # ob eine unserer Figuren die Schach setzende Figur schlagen kann
                    if not self.checkSchlagen(pos):
                        bool = True
                        break
        return bool

    # überprüft, ob bei Bewegen man sich selber Schach setzt
    def checkPinned(self, id, figure_num):
        # führt einen Move mit der Figur aus, speichert jedoch, wo die Figur zuletzt stand.
        # Wenn check Schach aktiv, dann ist die Figur gepinnt
        save_pos = self.idToPos(id)
        # es wird einfach irgendein Zug gemacht alle Figuren können
        # sich einfach eins nach unten oder oben Bewegen, außer dem Bishop

        # wenn weißter bishop
        if (id == 3) | (id == 6):
            answer, arr = self.figures_white[figure_num].Zug(
                save_pos[0] + 1, save_pos[1] + 1
            )
            if not answer:
                answer, arr = self.figures_white[figure_num].Zug(
                    save_pos[0] - 1, save_pos[1] - 1
                )
            # theoretisch müsste es hier immer true sein
            if answer:
                if self.checkSchach():
                    print("Figur ist gepinnt und darf nicht gerückt werden")
                    return True
            else:
                print("Error checkPinned")
        # wenn schwarzer Bishop
        elif (id == 27) | (id == 30):
            answer, arr = self.figures_black[figure_num].Zug(
                save_pos[0] + 1, save_pos[1] + 1
            )
            if not answer:
                answer, arr = self.figures_white[figure_num].Zug(
                    save_pos[0] - 1, save_pos[1] - 1
                )
            # theoretisch müsste es hier immer true sein
            if answer:
                if self.checkSchach():
                    print("Figur ist gepinnt und darf nicht gerückt werden")
                    return True
            else:
                print("Error checkPinned")
        # wenn weißes oder schwarzes Pferd
        return False

    # überprüft den Zwischenraum
    def checkRoomBetween(self, arr):
        # print(arr)
        bool = True
        # gehe zwischen Raum durch
        for i in range(1, len(arr) - 1):
            # checke bei jeder Position, ob eine Figur darauf steht:
            pos = (arr[i][0], arr[i][1])
            # print(arr[i])
            if self.checkLists(pos, False):
                bool = False
                break
        return bool

    ########################################################################################################################
    # überprüft die Legitimität des Zuges
    def checkZug(self, schlagen):
        bauer = 0
        if self.saveid < 17:
            # wenn größer 8 dann sind es Bauern die zwei Werte mehr benötigen
            if 7 < self.save_figure_num:
                answer, arr = self.figures_white[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "white"
                )
                bauer = 1
            else:
                answer, arr = self.figures_white[self.save_figure_num].Zug(
                    self.posX, self.posY
                )
        else:
            if 8 > self.save_figure_num:
                answer, arr = self.figures_black[self.save_figure_num].Zug(
                    self.posX, self.posY, schlagen, "black"
                )
                bauer = 2
            else:
                answer, arr = self.figures_black[self.save_figure_num].Zug(
                    self.posX, self.posY
                )

        # gibt erst einen bool wert zurück, dann gibt es 3 Optionen:
        # 1. wenn answer = False, dann soll auch hier sofort false ausgegeben werden
        if not answer:
            return False
        # 2. Wenn answer = True, dann gibt es ein array was mitgegeben wird,
        # 2.1 Wenn dieses array leer ist, dann handelt es sich um den König, den Bauern oder das Pferd,
        # welche nur 1 Feld Züge machen können oder über Figuren Springen dürfen
        elif answer & (len(arr) == 0):
            # handelt es sich nun um den König, muss geschaut werden, ob die gegnerische Figur aktuell gedeckt wird.
            if (self.saveid == 5) or (self.saveid == 29):
                if self.checkGedeckt((self.posX, self.posY)):
                    print(
                        "Es handelt sich um den König, die gegnerische Figur wird gedeckt, "
                        "oder man steht sonst im Schach"
                    )
                    return False
            return True
        # 2.2 Ansonsten handelt es sich um einen größeren Zug, bei dem Figuren dazwischen stehen könnten
        # bis auf die erste und letze Stelle soll dieses überprüft werden, ob es ein Feld gibt, auf dem eine Figur steht
        else:
            # print(arr)
            bool = self.checkRoomBetween(arr)
            # nur wenn keine Figur erkannt wurde muss die spezielle Variable, die für den Bauern eingebaut wurde,
            # damit man unterscheiden kann, ob er 2 Felder springen darf, aktiviert werden
            if bool and (bauer != 0):
                if bauer == 1:
                    self.figures_white[self.save_figure_num].moved()
                else:
                    self.figures_black[self.save_figure_num].moved()
            return bool

    ########################################################################################################################
    # gibt für das Backtracking die ID zurück und ändert die Position
    def returnID(self, Position, newPos, id):
        # erst soll er nach der Aktiven Figur suchen
        if id is not None:
            for i in range(0, 16):
                # wir kennen die ID der Figur die laut dead Figure zuletzt getötet wurde
                if self.figures_black[i].getID() == id:
                    # print("changed toggle of: ", id)
                    self.figures_black[i].toggleActive()
                    return None
                if self.figures_white[i].getID() == id:
                    # print("changed toggle of: ", id)
                    self.figures_white[i].toggleActive()
                    return None
        else:
            for i in range(0, 16):
                # wenn du eine Figure mit der gleichen Position findest
                if (self.figures_black[i].getPos() == Position) & (
                    self.figures_black[i].getActive() is True
                ):
                    id = self.figures_black[i].getID()
                    self.figures_black[i].setPos(newPos[0], newPos[1])
                    return id
                if (self.figures_white[i].getPos() == Position) & (
                    self.figures_white[i].getActive() is True
                ):
                    id = self.figures_white[i].getID()
                    self.figures_white[i].setPos(newPos[0], newPos[1])
                    return id
        return None

    ########################################################################################################################
    # geht die Liste durch und schaut, ob für die Position eine Figur erkannt wurde
    def checkLists(self, Position, Bool):
        # gehe die Listen durch
        for i in range(0, 16):
            # wenn du eine Figure mit der gleichen Position findest
            if (self.figures_black[i].getPos() == Position) & (
                self.figures_black[i].getActive() is True
            ):
                if Bool:
                    self.id = self.figures_black[i].getID()
                    self.figure_num = i
                    # print("Schwarze Figur erkannt", self.id)
                # else:
                # print("Figur erkannt")
                return True
            if (self.figures_white[i].getPos() == Position) & (
                self.figures_white[i].getActive() is True
            ):
                if Bool:
                    self.id = self.figures_white[i].getID()
                    self.figure_num = i
                    # print("Weiße Figur erkannt", self.id)
                # else:
                # print("Figur erkannt")
                return True
        return False

    ########################################################################################################################
    # bekommt den neusten Zug und führt sämtliche Berechnungen und Fälle aus
    def checkAll(self, x, y, gui):
        if self.beendet:
            gui.changeOutput(
                "Das Spiel ist beendet, keine weiteren Zug-Eingaben möglich"
            )
        else:
            self.id = None
            # lade die Listen
            self.figures_black, self.figures_white = gui.getfigLists()

            # wandle zuerst die x und y koordinaten in die zugehörige Feldposition um
            self.Position = self.con.convPosFie(x, y)
            self.posX, self.posY = self.Position

            # schaue, ob auf der Position eine Figur steht
            self.checkLists(self.Position, True)

            # Ausgabe des Status
            print("\nStatus:")

            # Es folgt das Unterscheiden in 3 mögliche Fälle
            ################################################################################################################
            # 1. Eine Figur wurde ausgewählt (kennzeichnend dafür: Es wurde eine ID erkannt und keine alte gespeichert)

            if (not self.id is None) & (self.saveid is None):
                # jetzt schaut er erst einmal, welche Farbe aktuell dran ist und dementsprechend rücken darf
                if ((self.Runde % 2 == 1) & (self.id < 17)) | (
                    (self.Runde % 2 == 0) & (self.id > 16)
                ):
                    # Feedback
                    gui.ErrorOff()
                    gui.changeOutput("Klicke auf das Zielfeld")
                    print("Figur erkannt: ", self.id)

                    # Einstellungen
                    self.erkannt = True
                    # speichern der alten ID
                    self.saveid = self.id
                    self.save_figure_num = self.figure_num
                    x, y = self.con.convFiePos(self.posX, self.posY)
                    self.rect = gui.canvas.create_rectangle(
                        x - 28, y - 28, x + 28, y + 28, width=2, outline="#04d9ff"
                    )
                    return
                else:
                    # überprüft, ob falsche Person versucht zu rücken
                    if self.Runde % 2 == 1:
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
                # print(self.saveid)
                if self.checkZug(False) is True:
                    # Feedback
                    print("Zug erkannt: ", self.posX, self.posY)
                    gui.changeOutput("Zug erkannt, Figur wird gerückt")
                    gui.ErrorOff()

                    # ändern der Position der gerückten Figur
                    if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                        posvor = self.figures_white[self.save_figure_num].getPos()
                        self.figures_white[self.save_figure_num].setPos(
                            self.posX, self.posY
                        )
                    else:  # schwarze Figur, ändern in der schwarzen Liste
                        posvor = self.figures_black[self.save_figure_num].getPos()
                        self.figures_black[self.save_figure_num].setPos(
                            self.posX, self.posY
                        )

                    # löschen des Markers
                    gui.canvas.delete(self.rect)

                    # das Bild der Figur auf die neue Position setzen
                    gui.switchImgofFigur(self.posX, self.posY, self.saveid)

                    # auf Schach überprüfen:
                    self.checkSchach(gui)

                    # ausgewählte Figur nun nicht mehr ausgewählt
                    self.saveid = None
                    self.save_figure_num = None

                    # gültigen Zug in Listbox eintragen
                    gui.insertItemInList(
                        posvor[0], posvor[1], self.posX, self.posY, None
                    )

                    # Zug vollendet eine neue Runde Beginnt
                    self.Runde += 1

                else:
                    print("Zug nicht möglich")
                    gui.changeOutput("Zug nicht möglich, wähle ein anderes Feld")
                    gui.ErrorOn()

                return

            ################################################################################################################
            # 3. Eine andere Figur wurde ausgewählt (2 extra Fälle: gegner oder eigene Figur)
            # (kz: Es wurde eine Figur gespeichert und eine neue erkannt)

            if (not self.id is None) & (not self.saveid is None):
                # überprüfe, ob eine eigene andere Figur ausgewählt wurde, in dem Fall wären beide IDs sowohl vorherige,
                # als auch nachfolgende entweder im Bereich 1 bis 16 oder 17 bis 32
                if ((self.id < 17) & (self.saveid < 17)) | (
                    (self.id > 16) & (self.saveid > 16)
                ):
                    gui.changeOutput("Eigene andere Figur")
                    print("Eigene andere Figur erkannt")

                    # löschen des alten Figur-Markers
                    gui.canvas.delete(self.rect)

                    # erstellen des neuen Markers
                    x, y = self.con.convFiePos(self.posX, self.posY)
                    self.rect = gui.canvas.create_rectangle(
                        x - 28, y - 28, x + 28, y + 28, width=2, outline="#04d9ff"
                    )

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
                        print("Andere Figur wurde geschlagen")

                        # löschen des Markers
                        gui.canvas.delete(self.rect)

                        # ändern der Position der schlagenden Figur
                        if self.saveid < 17:  # weiße Figur, ändern in der weißen Liste
                            posvor = self.figures_white[self.save_figure_num].getPos()
                            self.figures_white[self.save_figure_num].setPos(
                                self.posX, self.posY
                            )
                        else:  # schwarze Figur, ändern in der schwarzen Liste
                            posvor = self.figures_black[self.save_figure_num].getPos()
                            self.figures_black[self.save_figure_num].setPos(
                                self.posX, self.posY
                            )

                        # deaktivieren(verkleinern der neuen Figur
                        if self.id < 17:  # weiße Figur, ändern in der weißen Liste
                            self.figures_white[self.figure_num].delFig()
                        else:  # schwarze Figur, ändern in der schwarzen Liste
                            self.figures_black[self.figure_num].delFig()

                        # abändern des Bildes
                        gui.switchImgofFigur(self.posX, self.posY, self.saveid)
                        gui.loescheImgofFigur(self.id)

                        # gültigen Zug in Listbox eintragen
                        gui.insertItemInList(
                            posvor[0], posvor[1], self.posX, self.posY, self.id
                        )
                        # Es folgt ein Runden inkrement, da nun gegnerische Farbe antwortet auf vorherigen Zug
                        self.Runde += 1

                        # auf Schach überprüfen
                        self.checkSchach(gui)

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
