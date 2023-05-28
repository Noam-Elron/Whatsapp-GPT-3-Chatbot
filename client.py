from utils import get_number_details, within_timelimit
import datetime

class Client:
    def __init__(self, db_connection, whatsapp_number):
        self.db = db_connection
        self.user_id, self.phone_number = get_number_details(whatsapp_number)

    def login(self):
        if self.user_id is None:
            raise Exception("No user id given")
        if not self.db.record_exists(self.user_id, "users"):
            query = ("INSERT INTO users (uuid, phone_number, tokens) VALUES (%s, %s, 0);")
            self.db.insert_data(query, self.user_id, self.phone_number)
            self.db.close()
            return False

        return True

    def check_last_message(self):
        query = ("SELECT message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 1;")
        message, timestamp = self.db.fetch_single_row(query)
        message = "None" if not within_timelimit(timestamp, hours=1) else message
        return message



    def insert_message(self, message):
        query = ("INSERT INTO messages (uuid, message, timestamp) VALUES (%s, %s, %s);")
        self.db.insert_data(query, self.user_id, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def insert_response(self, response):
        query = ("INSERT INTO responses (id, response) VALUES ((SELECT MAX(id) FROM messages), %s);")
        self.db.insert_data(query, response)

