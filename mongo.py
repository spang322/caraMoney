import pymongo
from pymongo import MongoClient


class Database:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://spang322:0zgiRc7YwLtKytEZ@cluster0.xjnorlx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["Caramel"]
        self.user_collection = self.db["User"]
        self.log_collection = self.db["Log"]
        self.deposit_collection = self.db["Deposit"]

    def add_log(self, sender_id, msg, timestamp):
        self.log_collection.insert_one({'_id': sender_id, 'message_text': msg, 'timestamp': timestamp})

    def add_new(self, usr):
        self.user_collection.insert_one(usr)

    def find_user(self, last_name):
        return self.user_collection.find_one({'last_name': last_name})


Mongo = Database()
