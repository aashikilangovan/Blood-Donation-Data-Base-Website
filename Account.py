# from Database import mysql
from App import app


class Account:
    def __init__(self, FirstName, LastName, Birthdate, Gender, Password, Email):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Birthdate = Birthdate
        self.Gender = Gender
        self.Password = Password
        self.Email = Email
