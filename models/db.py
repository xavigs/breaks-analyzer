from credentials import *
from pymongo import MongoClient

class Database:

    def connect(self):
        self.connection = MongoClient(MONGODB_CONNECTION)
        database = self.connection['breaksDB']
        return database
    
    def close(self):
        self.connection.close()