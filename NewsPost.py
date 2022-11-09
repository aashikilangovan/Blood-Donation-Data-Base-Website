from Database import mysql
from App import app
from datetime import *

#initialize class
class NewsPost:
    #set engg type data member (String)
    def __init__(self, Title, Body, Date, Connection):
        self.Date = Date
        self.Body = Body
        self.Title = Title
        self.Connection = Connection
        
    def add_post(self):
        userQuery = "INSERT INTO news_post (title, body, date) VALUES ( %s, %s, %s)"
        val = (self.Title, self.Body, self.Date)
        cursor = self.Connection.cursor()            
        cursor.execute(userQuery, val)
        self.Connection.commit()

    def get_posts(self):
        userQuery="SELECT * FROM news_post;"
        cursor = self.Connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_titles(self):
        userQuery="SELECT title FROM news_post;"
        cursor = self.Connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_bodies(self):
        userQuery="SELECT body FROM news_post;"
        cursor = self.Connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def get_dates(self):
        userQuery="SELECT date FROM news_post;"
        cursor = self.Connection.cursor()            
        cursor.execute(userQuery)
        result = cursor.fetchall()
        return result

    def convert_date(self, date):
        real_date = self.extractDate(date)
        return real_date.strftime("%B %d %Y")

    def extractDate(self, time):
        year = int(time[0:4])
        day = int(time[5:7])
        month = int(time[8:10]) 
        return datetime(year, month, day)