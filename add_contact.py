from PyQt4 import QtGui, uic
from db_connect import db_connect

class add_contact(QtGui.QMainWindow):
    def __init__(self, contact_data=None):
        super(add_contact, self).__init__()
        uic.loadUi('ui/add_contact.ui', self)
        if contact_data:
            self.add_button.setText("Edit")
            self.fio_field.setText(contact_data[1])
            self.phone_field.setText(contact_data[2])
            self.date_field.setDate(contact_data[3])
        else:
            self.delete_button.setVisible(False)
        self.cancel_button.clicked.connect(self.on_cancel_click)

    def on_cancel_click(self):
        self.close()
        