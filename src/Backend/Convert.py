class Convert:
    def __init__(self):
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return

    def convPosFie(self, x, y):
        for posx in range(0, 9):
            if x <= (posx * 55):
                break
        for posy in range(0, 8):
            if y >= (385 - posy * 55):
                break
        print(posx, posy)
        return posx, posy+1

    def convFiePos(self, posX, posY):
        return (posX - 1) * 55 + 30, 415-((posY - 1) * 55)

    def convFieLet(self, posX):
        return self.letters[posX-1]

    def convLetFie(self, string):
        for i in range(0, 8):
            if string == self.letters[i]:
                return i+1

