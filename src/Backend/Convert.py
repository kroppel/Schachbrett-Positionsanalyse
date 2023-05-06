class Convert:
    def __init__(self):
        return

    def convPosFie(self, x, y):
        for posx in range(0, 9):
            if x <= posx * 55:
                print(posx)
                break
        for posy in range(0, 9):
            if y <= posy * 55:
                print(posy)
                break
        return posx, posy

    def convFiePos(self, posX, posY):
        return (posX - 1) * 55 + 30, (posY - 1) * 55 + 30
