from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from datetime import *
from App import app
# from Database import mysql
from NewsPost import *
from Login import *
from Location import *
from Appointment import *
from BloodType import *
from Email import *
import mysql.connector
HOST = "http://TheErythroSite.pythonanywhere.com"
import os
from flask import Flask
from os import path
# from flask_mail import Mail
import numpy as np

def make_connection():
    connection = mysql.connector.connect(host = '127.0.0.1', user = 'root', passwd = 'Tuttu_2001', database = 'erythrodb')
    return connection

def create_app():
    app = Flask(__name__)
    mail = Mail(app)

    app.config['BCRYPT_LOG_ROUNDS'] = 13
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['DEBUG_TB_ENABLED'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SECRET_KEY'] = 'super secret key'
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.config['SESSION_TYPE'] = 'filesystem'

        # mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

        # gmail authentication
    app.config['MAIL_USERNAME'] = 'TheErythroSite@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Cpsc471isfun!'

        # mail accounts
    app.config['MAIL_DEFAULT_SENDER'] = 'TheErythroSite@gmail.com'

    return app



app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def home():
    admin = 2
    username = "unregistered"
    return render_template("main.html", admin = admin, username = username)

@app.route('/confirmation/<admin>/<username>', methods=['GET', 'POST'])
def confirmation(admin, username):
    return render_template("confirmation.html", admin = admin, username = username)

@app.route('/message/<admin>/<username>', methods=['GET', 'POST'])
def message(admin, username):
    return render_template("sendEmail.html", admin = admin, username = username)

@app.route('/my-messages/<admin>/<username>', methods=['GET', 'POST'])
def myMessages(admin, username):
    myMessage = Email("sender", username, "subject", "message", "1", make_connection())
    
    subjects = np.array(myMessage.get_confirmational_Subjects())
    messages = np.array(myMessage.get_confirmational_Messages())

    trimmedSubjects = []
    trimmedMessages = []
    size = 0
    for x in subjects:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedSubjects.append(z)
        size = size + 1

    for x in messages:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedMessages.append(z)
      
    return render_template("myMessages.html", admin = admin, username = username, messages =trimmedMessages, subjects = trimmedSubjects, size = size)



@app.route('/administrator/<admin>/<username>', methods=['GET', 'POST'])
def administrator(admin, username):
    if request.method == "POST":
        time = request.form.get("time")
        date = request.form.get("date")
        address = request.form.get("address")
        postalcode = request.form.get("postalcode")
        city = request.form.get("city")
        country = request.form.get("country")
        newConnection = make_connection()
        myAppointment = Appointment(time, date, "0", postalcode, newConnection)
        myAppointment.add_appointment()
        myLocation = Location(postalcode, city, address, country, newConnection)
        myLocation.add_location()
    return render_template("addAppointment.html", admin = admin, username = username)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == "POST":
        newConnection = make_connection() #create connection to database

        #retrieve all the user inputs
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password1 = request.form.get("pass1")
        password2 = request.form.get("pass2")
        birthday = request.form.get("date")
        gender = request.form.get("gender")
        accountType = request.form.get("accountType")
    
        #end of input retrieval

        myLogin = Login(email, password1, newConnection) #create Login object
        age = myLogin.get_age(birthday)
        if(password1 == password2): #check if both password inputs match
            if(myLogin.add_login(name, lastname, age, birthday, gender, accountType) == True): #add account into database
                flash('Account was successfully created!')
                if(accountType == "Administrator"): #if account type is administator
                    return redirect(url_for('administrator', username = myLogin.username, admin = accountType)) #show administrator view
                else:
                    return redirect(url_for('loggedIn', username = myLogin.username, admin = accountType)) #show donor view
            else:
                flash('Account using entered email already exists',category= 'error')
        else:
            return render_template("signup.html")


    return render_template("signup.html")

@app.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    if request.method == "POST":
        newConnection = make_connection() #create connection to the database
        #retrieve user inputs
        name = request.form.get("email") 
        password = request.form.get("psw")

        myLogin = Login(name, password, newConnection) #create Login object
        if(myLogin.authenticate() == 1): #if password and username exist and match
            flash('Logged in successfully!')
            if(myLogin.isAdmin() == "0"):
                return redirect(url_for('loggedIn', username = myLogin.username, admin = '0')) #show donor view
            else:
                return redirect(url_for('administrator', username = myLogin.username, admin = '1')) #show administrator view
        else:
            flash('Email or password are invalid',category= 'error')

    return render_template("signin.html")

@app.route('/logged-in/<admin>/<username>', methods=['GET', 'POST'])
def loggedIn(admin, username):
    return render_template("loggedIn.html", admin = '0', username = username)

@app.route('/book-appointment/<admin>/<username>', methods=['GET', 'POST'])
def bookAppointment(admin, username):
    newConnection = make_connection()
    myAppointment = Appointment("temp", "temp", "temp", "temp", newConnection)        
    dates = np.array(myAppointment.get_dates())
    times = np.array(myAppointment.get_times())
    locations = np.array(myAppointment.get_locations())
    ID = np.array(myAppointment.get_IDS())
       
    myLocation = Location("temp", "temp", "temp", "temp", newConnection)
   
    trimmedDates = []
    trimmedTimes = []
    trimmedLocations = []
    trimmedAddresses = []
    trimmedCities = []
    trimmedCountries = []
    trimmedIDs = []

    i = 0
    while(i < len(ID)):
        temp = str(ID[i])
        temp = temp[1:len(temp)-1]
        i = i +1
        trimmedIDs.append(temp)
  

    
    for x in dates:
        y = str(x)
        z = y[2:len(y) -2]
        completeDate = myAppointment.convert_date(z)
        trimmedDates.append(completeDate)
      
        
    for x in times:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedTimes.append(z)

   
    for x in locations:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedLocations.append(z)
        address = myLocation.get_addresses(z)
        trimmedAddresses.append(address)

        city = myLocation.get_cities(z)
        trimmedCities.append(city)

        country = myLocation.get_countries(z)
        trimmedCountries.append(country)


    if request.method == "POST":
        identification = request.form['submit_button']
        myAppointment.set_donor(username, identification)
        sender = "Erythro Site"
        Donor = username
        Subject = "You booked an appointment"
        time = str(myAppointment.get_time(identification))
        date = str(myAppointment.get_date(identification))
        location = str(myAppointment.get_location(identification))
        body = "Your appointment is booked for " + date + " at " + time
        myEmail = Email(sender, Donor, Subject, body, 1, make_connection())
        myEmail.add_email()
        return render_template("confirmation.html", identification = int(identification), admin = admin, username = username )


    return render_template("bookAppointment.html", admin = '0', username = username, trimmedTimes= trimmedTimes, trimmedDates= trimmedDates, trimmedLocations= trimmedLocations, trimmedAddresses = trimmedAddresses, trimmedCountries = trimmedCountries, trimmedCities = trimmedCities,size = i, ID = trimmedIDs)

@app.route('/blog/<admin>/<username>', methods=['GET', 'POST'])
def showBlog(admin, username):
    newConnection = make_connection()
    title = "temp"
    body = "temp"
    a_date = "temp"
    myNewsPost = NewsPost(title, body, a_date, newConnection) 
    titles = np.array(myNewsPost.get_titles())
    dates = np.array(myNewsPost.get_dates())
    bodies = np.array(myNewsPost.get_bodies())
         
       
    trimmedTitles = []
    trimmedDates = []
    trimmedBodies = []
    
    for x in titles:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedTitles.append(z)
    for x in dates:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedDates.append(myNewsPost.convert_date(z))
        
    for x in bodies:
        y = str(x)
        z = y[2:len(y) -2]
        trimmedBodies.append(z)

    if request.method == "POST":
        title = request.form.get("title")
        title = title.upper()
        body = request.form.get("blog_post")
        now = datetime.now()
        date = now.strftime("%Y-%d-%m")
        myPost = NewsPost(title, body, date, newConnection)
        myPost.add_post()
        return redirect(url_for('showBlog', admin= admin, username= username))
       
        

        
    return render_template("blog.html", admin = admin, username = username, titles = trimmedTitles, dates = trimmedDates, bodies = trimmedBodies, size = len(trimmedBodies))


@app.route('/profile/<admin>/<username>', methods=['GET', 'POST'])
def profile(admin, username):
    key = request.args.get('admin')
    myLogin = Login(username, "temp",  make_connection() )
    name = myLogin.get_name(username)
    birthday = myLogin.get_birthday(username)
    lastname = myLogin.get_last_name(username)
    gender = myLogin.get_gender(username)
    age = myLogin.get_age(username)
    bloodType = myLogin.get_bloodType(username)

    myBlood = BloodType("temp", "temp", bloodType, make_connection())
    if(bloodType != 0):
        bloodGroup = myBlood.get_group()
        rhesus = myBlood.get_rh()
    else:
        bloodGroup = "-"
        rhesus = "-"
    myLogin.update_age(birthday)
    age = myLogin.get_age(username)
    return render_template("Account.html", admin = admin, username = username, name = name, lastname = lastname, birthday = myLogin.get_birthday_words(username), gender = gender, age = age, bloodType = bloodType, group = bloodGroup, rhesus = rhesus)

@app.route('/edit-profile/<admin>/<username>', methods=['GET', 'POST'])
def editProfile(admin, username):
    myLogin = Login(username, "temp",  make_connection() )
    name = myLogin.get_name(username)
    birthday = myLogin.get_birthday(username)
    lastname = myLogin.get_last_name(username)
    gender = myLogin.get_gender(username)
    password = myLogin.get_password(username)
    
    bloodType = myLogin.get_bloodType(username)
    myBlood = BloodType("group", "rhesus", bloodType, make_connection())
    group = myBlood.get_group()
    rhesus = myBlood.get_rh()
    if request.method == "POST":
        myLogin = Login(username, "temp",  make_connection() )
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        password = request.form.get("password")
        birthday = request.form.get("date")

        group = request.form.get("group")
        
        rhesus = request.form.get("rhesus")
        myBlood = BloodType(group, rhesus, 0, make_connection())
        identification = myBlood.get_ID()
        myLogin.set_bloodType(identification)
        myLogin.set_password(password)
        myLogin.set_name(firstname)
        myLogin.set_lastname(lastname)
        myLogin.set_birthday(birthday)
        age = myLogin.get_age(birthday)
        return redirect(url_for('profile', username = myLogin.username, admin = admin, age = age ,bloodType = identification, group = group, rhesus = rhesus)) 
    return render_template("editProfile.html", admin = admin, username = username, name = name, lastname = lastname, birthday = birthday, gender = gender, password = password, group = group, rhesus = rhesus)


# --------------------------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    app.run(debug=True)
