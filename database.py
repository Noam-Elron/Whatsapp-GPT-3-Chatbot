import mysql.connector
from configparser import ConfigParser
from mysql.connector import errorcode
import hashlib

config_file = ConfigParser()
config_file.read("config.ini")
#print(config_file["DATABASE_CREDENTIALS"]["user"])

def db_setup():
    try:
        mydb = mysql.connector.connect(
        host=config_file["DATABASE_CREDENTIALS"]["host"],
        user=config_file["DATABASE_CREDENTIALS"]["user"],
        password=config_file["DATABASE_CREDENTIALS"]["password"],
        database= "NoamElron$users" )
        return mydb
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)



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

def user_check(data):
    mydb = db_setup()
    print(mydb)
    cursor = mydb.cursor()
    hashed_number, phone_number = get_number_details(data)
    query = ("SELECT uuid FROM users WHERE uuid = %s;")
    cursor.execute(query, (hashed_number,))
    row = cursor.fetchone()
    cursor.close()
    return hashed_number, row

def create_user(data):
    mydb = db_setup()
    cursor = mydb.cursor()
    hashed_number, phone_number = get_number_details(data)
    query = ("INSERT INTO users (uuid, phone_number) VALUES (%s, %s);")
    cursor.execute(query, (hashed_number, phone_number))
    mydb.commit()
    cursor.close()
    return hashed_number


#print(user_check("whatsapp:+972542364358"))
