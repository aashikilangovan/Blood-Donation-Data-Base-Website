
from App import app

import mysql.connector
from datetime import date

class Login:
    #Ctor for Login
    def __init__(self, username, password, connection):
        self.username = username
        self.password = password
        self.connection = connection


    #function to execute an SQL Query
    #Returns the Query result
    def executeQuery(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    #Cross checks if a username and password correspond with eachother
    #return boolean result
    def authenticate(self):
        userQuery = "SELECT Password FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4] #remove useless characters from front and end
        if(self.password == convert):
            return 1 #password matches with the one in table
        elif (self.user_exist() == False):
            return 0 #username does not exist
        else:
            return -1 #password does not match


    # Check if username and password combination exists
    def validate(self):
        query="SELECT * FROM Account WHERE Email='" + self.username + "' AND Password='" + self.password + "'"
        result=self.executeQuery(query)
        return result


    def isAdmin(self):
        userQuery = "SELECT admin FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[2:len(convert) - 3]
        return convert

  

    #check if user is already in the database table
    def user_exist(self):
        userQuery = "SELECT 1 FROM Account WHERE Email_Address = '"+ self.username +"';"
        result = self.executeQuery(userQuery)
        if(len(result) == 0):
            return False
        else:
            return True


    #Adds user to the table, given a username and password
    #Returns false if request was not possible (usename already exists)
    def add_login(self, name, lastname, age, birthday, gender, accountType):
        if(self.user_exist() == False):
            userQuery = "INSERT INTO Account (First_Name, Last_Name, BirthDate, Gender, Password, Age, Email_Address, admin, Blood_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            if(accountType == "Administrator"):
                accountType = True
            else:
                accountType = False
            age = self.how_old(birthday)
            val = (name, lastname, birthday, gender, self.password, age, self.username, accountType, 0)
            cursor = self.connection.cursor()
            cursor.execute(userQuery, val)
            self.connection.commit()
            return True
        else:
            return False

 
    #Sets the password. Can be used if a user wants to change their password
    def set_password(self,password):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET Password = %s WHERE Email_Address = %s"
        val = (password, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def set_lastname(self,lastname):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET Last_Name = %s WHERE Email_Address = %s"
        val = (lastname, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def set_name(self,firstname):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET First_Name = %s WHERE Email_Address = %s"
        val = (firstname, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def set_birthday(self,birthday):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET BirthDate = %s WHERE Email_Address = %s"
        val = (birthday, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def set_age(self,age):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET age = %s WHERE Email_Address = %s"
        val = (age, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def set_bloodType(self,blood_type):
        cursor = self.connection.cursor()
        userQuery = "UPDATE Account SET Blood_Type = %s WHERE Email_Address = %s"
        val = (blood_type, self.username)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def get_name(self, username):
        userQuery = "SELECT First_Name FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_last_name(self, username):
        userQuery = "SELECT Last_Name FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_birthday(self, username):
        userQuery = "SELECT BirthDate FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_birthday_words(self, username):
        userQuery = "SELECT BirthDate FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        convert = self.convert_date(convert)
        return convert

    def get_gender(self, username):   
        userQuery = "SELECT Gender FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert
   
    def get_password(self, username):   
        userQuery = "SELECT Password FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_bloodType(self, username):   
        userQuery = "SELECT Blood_Type FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[2:len(convert) - 3]
        return int(convert)

    def get_age(self, username):   
        userQuery = "SELECT Age FROM account WHERE Email_Address = '" + self.username + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[2:len(convert) - 3]
        return convert

    def how_old(self, birthday):
        daysPerYear = 365.2425
        age = int((date.today() - self.extractDate(birthday)).days/daysPerYear)
        return age

    def extractDate(self, birthday):
        year = int(birthday[0:4])
        month = int(birthday[5:7])
        day = int(birthday[8:10]) 
        return date(year, month, day)

    def update_age(self, birthday):
        age = self.how_old(birthday)
        self.set_age(age)

    def convert_date(self, date):
        real_date = self.extractDate(date)
        return real_date.strftime("%B %d %Y")

   