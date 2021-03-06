from PyQt4 import QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtGui import QTableView
from db_connect import db_connect
from add_contact import add_contact
import datetime

class main_window(QtGui.QMainWindow):
    def __init__(self, user_email, user_password):
        super(main_window, self).__init__()
        uic.loadUi('ui/main.ui', self)
        #self.__db = db_connect()
        self.__user_email = user_email
        self.__user_password = user_password
        self.update_phonebook_table()
        self.refresh_alphabet_director()
        self.__data_model = TableModel(self.contact_list)
        self.phone_book_table.setModel(self.__data_model)
        self.actionAdd.triggered.connect(self.add_contact)
        self.actionEdit_selected.triggered.connect(self.edit_contact)
        self.actionDelete.triggered.connect(self.remove_contact)
        self.actionRefresh.triggered.connect(self.refresh_list)
        self.alphabet_director.itemClicked.connect(self.on_alphabet_director_item_selected)
        self.birthday_notify()

    def on_alphabet_director_item_selected(self, item):
        for index, contact in enumerate(self.contact_list):
            if contact[1][0].upper() == item.text():
                self.phone_book_table.selectRow(index)
                break


    def birthday_notify(self):
        self.alert = QtGui.QMessageBox()
        self.alert.setWindowTitle("Birthdays notification")
        notification_text = "Here is list of upcoming birthdays for 7 days:\n"
        db = db_connect()
        birthday_list = db.get_birthdays_for_week(self.__user_email, self.__user_password)
        for contact in birthday_list:
            contact_text = "{fio},\t{phone},\t{dob}\n".format(fio=contact[1],phone=contact[2],dob=contact[3].strftime("%d-%m-%Y"))
            notification_text = notification_text + contact_text
        self.alert.setText(notification_text)
        self.alert.show()

    def show_nothing_selected_message_box(self):
        self.alert = QtGui.QMessageBox()
        self.alert.setWindowTitle("Nothing selected")
        self.alert.setText("Please select item to operate with.")
        self.alert.show()

    def add_contact(self):
        self.add_dialog = add_contact(self.__user_email, self.__user_password)
        self.add_dialog.show()
        self.add_dialog.closeEvent = self.refresh_list

    def edit_contact(self):
        indexes = self.phone_book_table.selectionModel().selectedRows()
        if len(indexes):
            self.edit_dialog = add_contact(self.__user_email, self.__user_password, self.contact_list[indexes[0].row()])
            self.edit_dialog.show()
            self.edit_dialog.closeEvent = self.refresh_list
        else:
            self.show_nothing_selected_message_box()

    def remove_contact(self):
        indexes = self.phone_book_table.selectionModel().selectedRows()
        if len(indexes):
            db = db_connect()
            db.delete_contact(self.__user_email, self.__user_password, self.contact_list[indexes[0].row()][0])
            self.refresh_list()
        else:
            self.show_nothing_selected_message_box()

    def update_phonebook_table(self):
        self.contact_list = db_connect().get_contact_list(self.__user_email,self.__user_password)

    def refresh_list(self,_=None):
        self.update_phonebook_table()
        self.__data_model.setData(self.contact_list)
        self.refresh_alphabet_director()
        print("list updated")
    
    def refresh_alphabet_director(self):
        letters = []
        for contact in self.contact_list:
            if contact[1][0].upper() not in letters:
                letters.append(contact[1][0].upper())
        self.alphabet_director.clear()
        self.alphabet_director.addItems(letters)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.__data = data
        self.headers = ["Name", "Phone", "Date of birth"]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self.__data[index.row()][index.column()+1]
            if isinstance(value, datetime.date):
                # Render time to YYY-MM-DD.
                return value.strftime("%d-%m-%Y")
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def rowCount(self, index):
        return len(self.__data)

    def columnCount(self, index):
        return len(self.__data[0])-1

    def setData(self,data):
        self.beginResetModel()
        self.__data = data
        self.endResetModel()

