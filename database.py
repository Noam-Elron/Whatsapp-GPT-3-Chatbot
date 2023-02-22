import mysql.connector
from mysql.connector import errorcode
import hashlib
import os


def db_connect():
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
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

class User:
    def __init__(self, full_number_request):
        self.id, self.phone_number = get_number_details(full_number_request)

    def user_check(self, cursor, phone_number):
        query = ("SELECT uuid FROM users WHERE uuid = %s;")
        cursor.execute(query, (self.id,))
        row = cursor.fetchone()
        return row

    def create_user(self, db, cursor):
        query = ("INSERT INTO users (uuid, phone_number, tokens) VALUES (%s, %s, 0);")
        cursor.execute(query, (self.id, self.phone_number))
        db.commit()
        

def ret_db_objects():
    db = db_connect()
    cursor = db.cursor()
    return db, cursor
    
def hash_string(data):
    hashed = hashlib.md5(data.encode(encoding="UTF-8"))
    hashed = hashed.digest()
    return hashed

def get_number_details(data):
    # User phone number is stored in the webhooks "From" ImmutableMultiDict Key, Value pair. Returned data VALUE is in the format 'whatsapp:+972542364358' as such we'll get the phone number by splitting upon the colon. ( + still remains)
    phone_number = data.split(":")
    # After the split we take the second value as that will contain the phone number.
    #phone_number = data
    phone_number = phone_number[1]
    # Create hash using md5 hash function
    hashed_number = hash_string(phone_number)
    return hashed_number, phone_number






#print(user_check("whatsapp:+972542364358"))
