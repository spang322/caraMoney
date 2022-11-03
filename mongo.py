import pymongo
from pymongo import MongoClient


class Database:
    def __init__(self):
        self.cluster = MongoClient(
            "mongodb+srv://spang322:0zgiRc7YwLtKytEZ@cluster0.xjnorlx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["Caramel"]
        self.user_collection = self.db["User"]
        self.log_collection = self.db["Log"]
        self.deposit_collection = self.db["Deposit"]

    def add_log(self, sender_id, msg, timestamp):
        self.log_collection.insert_one({'sender_id': sender_id, 'message_text': msg, 'timestamp': timestamp})

    def add_deposit(self, user_id, last_name, dp_amount, timestamp):
        dp_list = self.deposit_collection.find({'user_id': user_id})
        dp_list = [i for i in dp_list]
        if len(dp_list) == 0:
            dp_id = 0
        else:
            dp_id = dp_list[-1]['dp_id'] + 1

        self.deposit_collection.insert_one({'dp_id': dp_id, 'user_id': user_id, 'last_name': last_name,
                                            'dp_status': 0, 'dp_amount': dp_amount, 'timestamp': timestamp})

    def update_deposit_status(self, user_id, dp_status):
        dp_id = [i for i in self.deposit_collection.find({'user_id': user_id, 'dp_status': 0})][-1]['dp_id']
        self.deposit_collection.update_one({'dp_id': dp_id, 'user_id': user_id}, {'$set': {'dp_status': dp_status}})

    def add_new(self, user_id, last_name):
        self.user_collection.insert_one({'_id': user_id, 'last_name': last_name})

    def find_user(self, last_name):
        return self.user_collection.find_one({'last_name': last_name})


Mongo = Database()
