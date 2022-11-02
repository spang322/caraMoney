import pymongo
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://spang322:0zgiRc7YwLtKytEZ@cluster0.xjnorlx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["Caramel"]
        self.collection = self.db["Money"]

    def add_new(self, usr):
        self.collection.insert_one()

    def find(self, last_name):
        return self.collection.find_one({'last_name': last_name})


Mongo = Database()
