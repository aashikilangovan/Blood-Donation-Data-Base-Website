# Please make sure to run "pip install flask_mysqldb"!!!
from flask_mysqldb import MySQL
from App import app

class Database:
    def getMySQL(self):
        try:
            # Fill out the following fields before running!!!
            app.config["MYSQL_HOST"] = "localhost"
            app.config["MYSQL_USER"] = "root"
            app.config["MYSQL_PASSWORD"] = "yourpassword"
            app.config["MYSQL_DB"] = "cpsc471"

            mysql = MySQL(app)  # user this object for accessing database in multiple classes
            return mysql
        except Exception as e:
            print(e)


myData = Database()
mysql = myData.getMySQL()
