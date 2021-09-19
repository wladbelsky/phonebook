from PyQt4 import QtGui, uic

class register_window(QtGui.QMainWindow):
    def __init__(self):
        super(register_window, self).__init__()
        uic.loadUi('ui/register.ui', self)
        self.cancel_button.clicked.connect(self.on_cancel_click)

    def on_cancel_click(self):
        self.close()

    def on_sign_up_click(self):
        pass