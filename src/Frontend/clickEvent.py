import Backend.Logic as log

''' Passes the click or detected move to the backend (or uses Stockfish for a tipp)'''
class ClickEvent:

    ''' sets the gui and old x and y to save them '''
    def __init__(self, gui):
        self.logic = log.Logic(gui)
        self.oldx = -1
        self.oldy = -1

    ''' passes the click informations to the backend '''
    def on_click(self, x, y):
        return self.logic.input(x, y)

    ''' passes the tipp function information from the backend '''
    def tipp(self):
        return self.logic.byStock()
