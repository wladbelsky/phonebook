from PyQt4 import QtGui, uic
from register_window import register_window
from main_window import main_window
from db_connect import db_connect

class login_window(QtGui.QMainWindow):
    def __init__(self):
        super(login_window, self).__init__()
        uic.loadUi('ui/login.ui', self)
        self.sign_in_button.clicked.connect(self.on_sign_in_click)
        self.exit_button.clicked.connect(self.on_exit_click)
        self.sign_up_button.clicked.connect(self.on_sing_up_click)
        self.forgot_password.mousePressEvent = self.on_password_forgot_click
        self.show_password_checkbox.toggled.connect(self.on_password_checkbox_click)
        #self.show()
    
    def on_sign_in_click(self):
        db = db_connect()
        if not db.user_login(self.login_field.text(), self.pass_field.text()):
            self.alert = QtGui.QMessageBox()
            self.alert.setWindowTitle("User not found!")
            self.alert.setText("Login or Password invalid. Please try again.")
            self.alert.show()
        else:
            #login succesful
            #open main window
            print("login succesful")#TODO remove
            self.main_window = main_window(self.login_field.text(), self.pass_field.text())
            self.main_window.show()
            self.close()
            pass
    
    def on_sing_up_click(self):
        self.register = register_window()
        self.register.show()
        

    def on_password_forgot_click(self,_):
        print("forgot")

    def on_password_checkbox_click(self):
        if self.show_password_checkbox.isChecked():
            self.pass_field.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self.pass_field.setEchoMode(QtGui.QLineEdit.Password)

    def on_exit_click(self):
        exit()