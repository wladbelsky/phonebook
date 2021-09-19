from PyQt4 import QtGui, uic
import register_window


class login_window(QtGui.QMainWindow):
    def __init__(self):
        super(login_window, self).__init__()
        uic.loadUi('ui/login.ui', self)
        self.sign_in_button.clicked.connect(self.on_sign_in_click)
        self.exit_button.clicked.connect(self.on_exit_click)
        self.sign_up_button.clicked.connect(self.on_sing_up_click)
        self.forgot_password.mousePressEvent = self.on_password_forgot_click
        #self.show()
    
    def on_sign_in_click(self):
        #db connect
        # self.dialog = LoginWindow()
        # self.dialog.show()
        pass
    
    def on_sing_up_click(self):
        self.a = register_window.register_window()
        self.a.show()
        

    def on_password_forgot_click(self,_):
        print("forgot")

    def on_exit_click(self):
        exit()