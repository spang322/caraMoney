import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://spang322:0zgiRc7YwLtKytEZ@cluster0.xjnorlx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Caramel"]
collection = db["Money"]
