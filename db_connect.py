import mysql.connector
from json import load, loads
import os.path as path
from PyQt4.QtGui import QMessageBox

class db_connect():
    def __init__(self):
        path_to_json = "config/db_config.json"
        if not path.isfile(path_to_json):
            raise FileNotFoundError("'db_config.json' not found!")
        with open(path_to_json,"rb") as json_config_file:
            data = load(json_config_file)
            try:
                self.__mydb = mysql.connector.connect(
                    host=data["host"],
                    user=data["user"],
                    password=data["password"],
                    database=data["database"],
                )
                self.__cursor = self.__mydb.cursor()
            except Exception as e:
                print(e)
                self.alert = QMessageBox()
                self.alert.setWindowTitle("Can't connect to database")
                self.alert.setText("Can't connect to database\nCheck your internet connection and configuration file")
                self.alert.show()

    def user_login(self, email, password):
        self.__cursor.execute("SELECT * FROM users WHERE email='{email}' "
                              "AND password='{password}'".format(email=email,password=password))
        result = self.__cursor.fetchall()
        return bool(len(result))

    def register_user(self, email, password, date_of_birth):
        try:
            self.__cursor.execute("insert into users (email,password,date_of_birth) "
                                  "values ('{email}','{password}','{dob}')".format(email=email,password=password,dob=date_of_birth))
            self.__mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_contact_list(self, email, password):
        self.__cursor.execute("select contacts.id, fio, phone, contacts.date_of_birth "
                              "from contacts join users on contacts.user_id=users.id where users.email='{email}' and users.password='{password}'".format(email=email,password=password))
        return self.__cursor.fetchall()

    def get_birthdays_for_week(self, email, password):
        self.__cursor.execute("select id,fio,phone,date_of_birth from contacts where user_id=(select id from users where email={email} and password={password}) "
                              "and DayOfYear(date_of_birth) between DayOfYear(Now())"
                              " and DayOfYear(Now())+7".format(email=email,password=password))
        return self.__cursor.fetchall()

    def add_contact(self, email, password, contact_data):
        fio = contact_data[1]
        phone = contact_data[2]
        date_of_birth = contact_data[3]
        try:
            self.__cursor.execute("insert into contacts (user_id,fio,phone,date_of_birth) values "
                                  "((select id from users where users.email={email} and users.password={password}), "
                                  "'{fio}','{phone}',date('{date_of_birth}'))".format(email=email,password=password,
                                  fio=fio,phone=phone, date_of_birth=date_of_birth.toString("yyyy-M-d")))
            self.__mydb.commit()
            return True             
        except Exception as e:
            print(e)
            return False
        
    def edit_contact(self, email, password, contact_data):
        contact_id = contact_data[0]
        fio = contact_data[1]
        phone = contact_data[2]
        date_of_birth = contact_data[3]
        try:
            self.__cursor.execute("update contacts set user_id = (select users.id from users where "
                                  "users.email='{email}' and users.password='{password}'), fio='{fio}',"
                                  "phone='{phone}', date_of_birth='{doa}' where contacts.id='{id}'".format(email=email,password=password,fio=fio,
                                  phone=phone,doa=date_of_birth.toString("yyyy-M-d"), id=contact_id))
            self.__mydb.commit()
            return True             
        except Exception as e:
            print(e)
            return False

    def delete_contact(self, email, password, contact_id):
        try:
            self.__cursor.execute("delete from contacts where id='{id}' "
                                  "and (select count(id) from users where "
                                  "email={email} and password={password})>0".format(id=contact_id, email=email, password=password))
            self.__mydb.commit()
            return True             
        except Exception as e:
            print(e)
            return False
    