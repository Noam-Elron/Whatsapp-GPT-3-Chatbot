import mysql.connector
from mysql.connector import errorcode
import os

class DatabaseConnection:

    def __init__(self):
        # Making the db object and the cursor private just as its good habit to not let them be "exposed" outside of the object(even though not really private and the fact that only i have access to this codebase). These are instance variables as they need class methods in order to be instantiated
        self._db_object = None
        self._cursor = None

    def __enter__(self):
        try:
            self._db_object = self.db_connect()
            self._cursor = self._db_object.cursor()
            return self
        except mysql.connector.Error as err:
           print(err)
           raise err

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is not None:
            return False
        try:
            if self._cursor is not None:
                self.close()
            return True
        except mysql.connector.Error as err:
           print(err)
           raise err

    @staticmethod
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

    def fetch_single_row(self, query, *args):
        if len(args) >= 1:
            self._cursor.execute(query, args)
        else:
            self._cursor.execute(query)

        row = self._cursor.fetchone()
        return row

    def record_exists(self, user_id, table:str):
        # Query needs opposite argument listing in order to work
        query = ("SELECT EXISTS (SELECT * FROM " + table + " WHERE uuid=%s LIMIT 1);")
        res = self.fetch_single_row(query, user_id)
        # Returned value from fetchone will is a tuple(as it returns a row) containing comma seperated values. Because of the SELECT EXISTS command only one column exists so either (1,) or (0,) are returned.
        return True if int(res[0]) == 1 else False

    def insert_data(self, query, *args):
        self._cursor.execute(query, args)
        self._db_object.commit()

    def validate_input(self, *args):
        pass


    def close(self):
        # Small helper function, kinda pointless but makes it so the interaction is just with the DB object and not with any of its variables.
        self._cursor.close()
        self._db_object.close()



