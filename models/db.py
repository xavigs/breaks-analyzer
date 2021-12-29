import credentials
from pymongo import MongoClient

class Database:

    def connect(self):
        connection = MongoClient(credentials.MONGODB_CONNECTION)
        database = connection['breaksDB']
        return database
    
    def close(self):
        return False