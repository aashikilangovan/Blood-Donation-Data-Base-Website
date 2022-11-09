# from Database import mysql
from App import app
import mysql.connector

#initialize class
class BloodType:
    #set engg type data member (String)
    def __init__(self, Group, Rh, ID, connection):
        self.ID = ID
        self.Group = Group
        self.Rh = Rh
        self.connection = connection

    def executeQuery(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    def get_group(self):
        if(self.ID == 1 or self.ID == 2):
            return "A"
        elif(self.ID == 3 or self.ID == 4):
            return "B"
        elif(self.ID == 5 or self.ID== 6):
            return "O"
        elif(self.ID == 7 or self.ID == 8):
            return "AB"

    def get_rh(self):
        if(self.ID == 1 or self.ID == 4 or self.ID ==5 or self.ID ==8):
            return "Positive"
        else:
            return "Negative"

    def get_ID(self):
        if(self.Group == "A" and self.Rh == "Positive"):
            return 1
        elif (self.Group == "A" and self.Rh == "Negative"):
            return 2
        elif (self.Group == "B" and self.Rh == "Positive"):
            return 4
        elif (self.Group == "B" and self.Rh == "Negative"):
            return 3
        elif (self.Group == "AB" and self.Rh == "Positive"):
            return 8
        elif (self.Group == "AB" and self.Rh == "Negative"):
            return 7
        elif (self.Group == "O" and self.Rh == "Positive"):
            return 5
        elif (self.Group == "O" and self.Rh == "Negative"):
            return 6