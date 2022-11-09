
from App import app
from datetime import *
import mysql.connector

class Appointment:
    def __init__(self, time, date, patient, location, connection):
        self.time = time
        self.date = date
        self.connection = connection
        self.location = location
        self.patient = patient


    #function to execute an SQL Query
    #Returns the Query result
    def executeQuery(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    def add_appointment(self):
        userQuery = "INSERT INTO appointment (date, time, location, donor) VALUES ( %s, %s, %s, %s)"
        val = (self.date, self.time, self.location, self.patient)
        cursor = self.connection.cursor()            
        cursor.execute(userQuery, val)
        self.connection.commit()

    def get_times(self):
        userQuery="SELECT time FROM appointment WHERE donor = '0';"
        cursor = self.connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_dates(self):
        userQuery="SELECT date FROM appointment WHERE donor = '0';"
        cursor = self.connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_locations(self):
        userQuery="SELECT location FROM appointment WHERE donor = '0';"
        cursor = self.connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_dates(self):
        userQuery="SELECT date FROM appointment WHERE donor = '0';"
        cursor = self.connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_IDS(self):
        userQuery="SELECT idappointment FROM appointment WHERE donor = '0';"
        cursor = self.connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def convert_date(self, date):
        real_date = self.extractDate(date)
        return real_date.strftime("%B %d %Y")

    def extractDate(self, time):
        year = int(time[0:4])
        month = int(time[5:7])
        day = int(time[8:10]) 
        return datetime(year, month, day)

    def set_donor(self, username, id):
        cursor = self.connection.cursor()
        userQuery = "UPDATE appointment SET donor = %s WHERE idappointment = %s"
        val = (username, id)
        cursor.execute(userQuery, val)
        self.connection.commit()

    def get_date(self, id):
        userQuery="SELECT date FROM appointment WHERE idappointment = %s;"
        val = ((id,))
        cursor = self.connection.cursor()
        cursor.execute(userQuery, val)
        result = cursor.fetchall()
        convert = str(result)
        convert = convert[3:len(convert )-4]
        convert = self.convert_date(convert)
        return convert

    def get_time(self, id):
        userQuery="SELECT time FROM appointment WHERE idappointment = %s;"
        val = ((id,))
        cursor = self.connection.cursor()
        cursor.execute(userQuery, val)
        result = cursor.fetchall()
        convert = str(result)
        
        convert = convert[3:len(convert )-4]
        return convert
    
    def get_location(self, id):
        userQuery="SELECT location FROM appointment WHERE idappointment = %s;"
        val = ((id,))
        cursor = self.connection.cursor()
        cursor.execute(userQuery, val)
        result = cursor.fetchall()
        convert = str(result)
        convert = convert[3:len(convert )-4]
        return convert

    def convert_date(self, date):
        real_date = self.extractDate(date)
        return real_date.strftime("%B %d %Y")

    def extractDate(self, time):
        year = int(time[0:4])
        month = int(time[5:7])
        day = int(time[8:10]) 
        return datetime(year, month, day)