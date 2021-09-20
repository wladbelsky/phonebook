from PyQt4 import QtGui, uic
from db_connect import db_connect

class add_contact(QtGui.QMainWindow):
    def __init__(self, email, password, contact_data=None):
        super(add_contact, self).__init__()
        uic.loadUi('ui/add_contact.ui', self)
        self.__user_email = email
        self.__user_password = password
        if contact_data:
            self.edit_mode = True
            self.add_button.setText("Edit")
            self.fio_field.setText(contact_data[1])
            self.phone_field.setText(contact_data[2])
            self.date_field.setDate(contact_data[3])
        else:
            self.delete_button.setVisible(False)
            self.edit_mode = False

        self.cancel_button.clicked.connect(self.on_cancel_click)
        self.add_button.clicked.connect(self.on_add_edit_click)

    def on_add_edit_click(self):
        db = db_connect()
        contact_data = [None, self.fio_field.text(),self.phone_field.text(),self.date_field.date()]
        if not self.edit_mode:
            db.add_contact(self.__user_email, self.__user_password, contact_data)
            self.close()
        else:
            print("edit mode not implemented")

    def on_delete_click(self):
        pass

    def on_cancel_click(self):
        self.close()
        