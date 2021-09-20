from PyQt4 import QtGui, uic
from db_connect import db_connect

class add_contact(QtGui.QMainWindow):
    def __init__(self, email, password, contact_data=None):
        super(add_contact, self).__init__()
        uic.loadUi('ui/add_contact.ui', self)
        self.__user_email = email
        self.__user_password = password
        self.contact_id = -1
        if contact_data:
            self.edit_mode = True
            self.contact_id = contact_data[0]
            self.add_button.setText("Edit")
            self.fio_field.setText(contact_data[1])
            self.phone_field.setText(contact_data[2])
            self.date_field.setDate(contact_data[3])
            self.delete_button.clicked.connect(self.on_delete_click)
        else:
            self.delete_button.setVisible(False)
            self.edit_mode = False

        self.cancel_button.clicked.connect(self.on_cancel_click)
        self.add_button.clicked.connect(self.on_add_edit_click)

    def show_dublicate_message_box(self):
        self.alert = QtGui.QMessageBox()
        self.alert.setWindowTitle("Dublicate detected")
        self.alert.setText("You already have this contact!")
        self.alert.show()

    def on_add_edit_click(self):
        db = db_connect()
        contact_data = [self.contact_id, self.fio_field.text(),self.phone_field.text(),self.date_field.date()]
        if not self.edit_mode:
            if db.add_contact(self.__user_email, self.__user_password, contact_data):
                self.close()
            else:
                self.show_dublicate_message_box()
        else:
            if db.edit_contact(self.__user_email, self.__user_password, contact_data):
                self.close()
            else:
                self.show_dublicate_message_box()

    def on_delete_click(self):
        db = db_connect()
        db.delete_contact(self.__user_email, self.__user_password, self.contact_id)
        self.close()


    def on_cancel_click(self):
        self.close()
        