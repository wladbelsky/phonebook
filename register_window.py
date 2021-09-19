from PyQt4 import QtGui, uic
from db_connect import db_connect

class register_window(QtGui.QMainWindow):
    def __init__(self):
        super(register_window, self).__init__()
        uic.loadUi('ui/register.ui', self)
        self.cancel_button.clicked.connect(self.on_cancel_click)
        self.sign_in_button.clicked.connect(self.on_sign_up_click)

    def on_cancel_click(self):
        self.close()

    def on_sign_up_click(self):
        email = self.email_field.text()
        password1 = self.password1_field.text()
        password2 = self.password2_field.text()
        date_of_birth = self.date_field.date().toString("yyyy-M-d")
        self.alert = QtGui.QMessageBox()
        if password1 != password2:
            self.alert.setWindowTitle("Passwords not match")
            self.alert.setText("Passwords not match. Please try again.")
        elif not email or not password1 or not password2 or not date_of_birth:
            self.alert.setWindowTitle("Missing info")
            self.alert.setText("One of the fields is not filled")
        else:
            db = db_connect()
            if db.register_user(email, password1, date_of_birth):
                self.alert.setWindowTitle("Registration successful")
                self.alert.setText("Registration successful. You can now sign in.")
                self.close()
            else:
                self.alert.setWindowTitle("Registration unsuccessful")
                self.alert.setText("User with this email already exists.") 
        self.alert.show()

