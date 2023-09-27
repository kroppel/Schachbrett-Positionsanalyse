class Convert:

    ''' Inits the converter with the letters used for fields positions in chess '''
    def __init__(self):
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return

    """
        Info: Converts a Position into a Field 
        Params: Pixel coordinates 
        Return: Field Position between 1 1 to 8 8 
    """
    def convPosFie(self, x, y):
        for posx in range(0, 9):
            if x <= (posx * 55):
                break
        for posy in range(0, 8):
            if y >= (385 - posy * 55):
                break
        print(posx, posy)
        return posx, posy + 1

    """
        Info: Converts a Field into a Pixel Position
        Params: Field Position between 11 to 88 
        Return: Pixel coordinates 
    """
    def convFiePos(self, posX, posY):
        return (posX - 1) * 55 + 30, 415 - ((posY - 1) * 55)

    """
        Info: Converts a number into a letter
        Params: the number
        Return: the letter
    """
    def convFieLet(self, posX):
        return self.letters[posX - 1]

    """
        Info: Converts a letter into a number
        Params: the letter
        Return: the number
    """
    def convLetFie(self, string):
        for i in range(0, 8):
            if string == self.letters[i]:
                return i + 1
