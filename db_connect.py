import mysql.connector

class db_connect():
    def __init__(self):#TODO: load from file
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user="api",
            password="mariadb",
            database="phonebook",
        )
        self.__cursor = self.__mydb.cursor()


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
        except:
            return False

    def get_contact_list(self, email, password):
        self.__cursor.execute("select contacts.id, fio, phone, contacts.date_of_birth "
                              "from contacts join users on contacts.user_id=users.id where users.email='{email}' and users.password='{password}'".format(email=email,password=password))
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
        pass

    def delete_contact(self, email, password, contact_id):
        pass