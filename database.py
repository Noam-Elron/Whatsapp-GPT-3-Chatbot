import mysql.connector
from mysql.connector import errorcode
import os

class Database:
    def __init__(self):
        # Making the db object and the cursor private just as its good habit to not let them be "exposed" outside of the object(even though not really private and the fact that only i have access to this codebase) 
        self._db_object = self.db_connect()
        self._cursor = self._db_object.cursor()
    
    def db_connect():
        """
        Connects to the database NoamElron$users using environmental variables for credentials.

        Returns:
            mydb (MySQLConnection object)

        Raises:
            mysql.connector.Error, multiple possible errorcodes, expects two common error codes: 
                ACCESS_DENIED_ERROR - Something is wrong user name or password
                BAD_DB_ERROR - Database doesn't exist - problem with DB name
            if not one of those two connector errors then simply raises the normal error.
        """
        try:
            mydb = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            database= "NoamElron$users" )
            return mydb
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong user name or password")
                raise err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                raise err
            else:
                raise err

    def user_check(self, user_id):
        query = ("SELECT uuid FROM users WHERE uuid = %s;")
        self._cursor.execute(query, (user_id,))
        row = self._cursor.fetchone()
        return row

    def create_user(self, user_id, phone_number):
        query = ("INSERT INTO users (uuid, phone_number, tokens) VALUES (%s, %s, 0);")
        self._cursor.execute(query, (user_id, phone_number))
        self.db.commit()
    
    def close(self):
        # Small helper function, kinda pointless but makes it so the interaction is just with the DB object and not with any of its variables.
        self._cursor.close()

