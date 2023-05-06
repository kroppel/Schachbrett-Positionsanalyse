import Backend.Checks as ch
import Backend.Figuren as fig
from pynput import mouse


class ClickEvent:
    def __init__(self, gui):
        self.check = ch.Checks()
        self.gui = gui
        self.oldx = -1
        self.oldy = -1
        mouse_listener = mouse.Listener(on_click=self.on_click)
        mouse_listener.start()

    def on_click(self, x, y, button, pressed):
        # wenn gedrückt
        if pressed:
            # soll er sich von der gui die x und y Werte der Motion der Maus auf dem Canvas holen
            x, y = self.gui.getXY()
            # wenn sich die Werte nicht geändert haben, wurde entweder die gleiche Figur noch einmal geklickt,
            # oder außerhalb des canvas, in beiden Fällen machen wir nichts.
            # wenn jedoch eine neue Position geklickt wurde wählen wir die Figur aus
            self.check.checkFigure(x, y, self.gui)
