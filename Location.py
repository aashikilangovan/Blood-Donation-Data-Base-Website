# from Database import mysql
from App import app

class Location:
    def __init__(self, PostalCode, City, Address, Country, Connection):
        self.PostalCode = PostalCode
        self.City = City
        self.Address = Address
        self.Country = Country
        self.Connection = Connection

    def executeQuery(self,query):
        cursor = self.Connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    def add_location(self):
        if(self.location_exist() == False):
            userQuery = "INSERT INTO location (postalcode, address, city, country) VALUES (%s, %s, %s, %s)"
            val = (self.PostalCode, self.Address, self.City, self.Country)
            cursor = self.Connection.cursor()            
            cursor.execute(userQuery, val)
            self.Connection.commit()
    
    def location_exist(self):
        userQuery = "SELECT 1 FROM location WHERE postalcode = '"+ self.PostalCode +"';"
        result = self.executeQuery(userQuery)
        if(len(result) == 0):
            return False
        else:
            return True

 

    def get_cities(self, PostalCode):
        userQuery = "SELECT city FROM location WHERE postalcode = '" + PostalCode + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_countries(self,PostalCode):
        userQuery = "SELECT country FROM location WHERE postalcode = '" + PostalCode + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert

    def get_addresses(self,PostalCode):
        userQuery = "SELECT address FROM location WHERE postalcode = '" + PostalCode + "';"
        result = self.executeQuery(userQuery)
        convert = str(result)
        convert = convert[3:len(convert) - 4]
        return convert
