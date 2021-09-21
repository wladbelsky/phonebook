from PyQt4 import QtGui, uic
from register_window import register_window
from main_window import main_window
from db_connect import db_connect

class password_reset_window(QtGui.QMainWindow):
    def __init__(self):
        super(password_reset_window, self).__init__()
        uic.loadUi('ui/password_reset.ui', self)
        self.cancel_button.clicked.connect(self.on_cancel_click)
        self.reset_button.clicked.connect(self.on_reset_click)

    def on_cancel_click(self):
        self.close()

    def on_reset_click(self):
        print(self.email_field.text())
        print("can't sent email due missing email server")
    