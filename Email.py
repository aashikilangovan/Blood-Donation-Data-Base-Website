from flask import Flask


import mysql.connector

class Email:
    def __init__(self,Sender, Donor, Subject, Message, isConfirmation, Connection):
        self.Sender = Sender
        self.Donor = Donor
        self.Subject = Subject
        self.Message = Message
        self.isConfirmation = isConfirmation
        self.Connection = Connection

  

    def add_email(self):
        if(self.isConfirmation == 1): #is a confirmational email
            userQuery = "INSERT INTO confirmation_email (sender, recipient, subject, message) VALUES ( %s, %s, %s, %s)"
            val = (str(self.Sender) ,str(self.Donor), str(self.Subject), str(self.Message))
            cursor = self.Connection.cursor()
            cursor.execute(userQuery, val)
            self.Connection.commit()

        else: #is a confirmational email
            userQuery = "INSERT INTO informational_email (sender, recipient, subject, message) VALUES ( %s, %s, %s, %s)"
            val = (str(self.Sender) ,str(self.Donor), str(self.Subject), str(self.Message))
            cursor = self.Connection.cursor()
            cursor.execute(userQuery, val)
            self.Connection.commit() 

    def get_confirmational_emails(self):
            userQuery="SELECT * FROM confirmation_email WHERE recipient = '" + str(self.Donor) + "';"
            cursor = self.Connection.cursor()            
            cursor.execute(userQuery)
            result = cursor.fetchall()
            return result

    def get_confirmational_Subjects(self):
            userQuery="SELECT subject FROM confirmation_email WHERE recipient = '" + str(self.Donor) + "';"
            cursor = self.Connection.cursor()            
            cursor.execute(userQuery)
            result = cursor.fetchall()
            return result

    def get_confirmational_Messages(self):
            userQuery="SELECT message FROM confirmation_email WHERE recipient = '" + str(self.Donor) + "';"
            cursor = self.Connection.cursor()            
            cursor.execute(userQuery)
            result = cursor.fetchall()
            return result