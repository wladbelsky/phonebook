import mysql.connector

class db_connect():
    def __init__(self):
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user="api",
            password="mariadb",
            database="phonebook",
        )
        self.__cursor = self.__mydb.cursor()


    def user_login(self, email, password):
        self.__cursor.execute("SELECT * FROM users WHERE email='{email}' AND password='{password}'".format(email=email,password=password))
        result = self.__cursor.fetchall()
        return bool(len(result))

    def register_user(self, email, password, date_of_birth):
        try:
            self.__cursor.execute("insert into users (email,password,date_of_birth) values ('{email}','{password}','{dob}')".format(email=email,password=password,dob=date_of_birth))
            self.__mydb.commit()
            return True
        except:
            return False
        # return bool(self.cursor.())

    def get_contact_list(self, email, password):
        self.__cursor.execute("select contacts.id, fio, phone, contacts.date_of_birth from contacts join users on contacts.user_id=users.id where users.email='{email}' and users.password='{password}'".format(email=email,password=password))
        return self.__cursor.fetchall()
        