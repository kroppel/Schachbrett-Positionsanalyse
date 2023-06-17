import Backend.Logic as log


class ClickEvent:
    def __init__(self, gui):
        self.logic = log.Logic(gui)
        self.oldx = -1
        self.oldy = -1

    def on_click(self, x, y):
        # self.check.checkAll(x, y, self.gui)
        self.logic.input(x, y)

    def tipp(self):
        return self.logic.byStock()

