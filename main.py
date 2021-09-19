#entry point
import sys
from PyQt4 import QtGui, uic
from login_window import login_window
import mysql.connector

class db_connect():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="api",
            password="mariadb",
            database="phonebook",
        )
        self.cursor = self.mydb.cursor()


    def user_login(self, login, password):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        for row in result:
            print(row)
        pass
        


db = db_connect()
db.user_login("","")
app = QtGui.QApplication(sys.argv)
window = login_window()
window.show()
app.exec_()
