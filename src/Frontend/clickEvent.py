import Backend.Checks as ch


class ClickEvent:
    def __init__(self, gui):
        self.check = ch.Checks()
        self.gui = gui
        self.oldx = -1
        self.oldy = -1

    def on_click(self, x, y):
        self.check.checkAll(x, y, self.gui)

    def passThrough (self, Position, newPosition, id):
        return self.check.returnID(Position, newPosition, id)