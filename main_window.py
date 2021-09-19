from PyQt4 import QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtGui import QTableView
from db_connect import db_connect
import datetime

class main_window(QtGui.QMainWindow):
    def __init__(self, user_email, user_password):
        super(main_window, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.__db = db_connect()
        self.__user_email = user_email
        self.__user_password = user_password
        self.update_phonebook_table()
        self.__data_model = TableModel(self.contact_list)
        # self.phone_book_table.setColumnCount(3)
        # self.phone_book_table.setHorizontalHeaderLabels(["Name", "Phone", "Date of birth"])
        # self.__update_phonebook_table()
        self.phone_book_table.setModel(self.__data_model)

    def update_phonebook_table(self):
        self.contact_list = self.__db.get_contact_list(self.__user_email,self.__user_password)
        #self.phone_book_table.setRowCount(len(self.contact_list))

        # row_number = 0
        # for contact in self.contact_list:
        #     self.phone_book_table.setItem(row_number,0,QTableWidgetItem(contact[1]))
        #     self.phone_book_table.setItem(row_number,1,QTableWidgetItem(contact[2]))
        #     self.phone_book_table.setItem(row_number,2,QTableWidgetItem(contact[3].strftime("%d/%m/%Y")))
        #     row_number += 1

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        # self.__data = []
        # self.__indexes = []
        # for record in data:
        #     self.__data.append(record[1:])
        #     self.__indexes.append(record[:1])
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