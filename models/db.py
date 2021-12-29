import credentials
from pymongo import MongoClient

class Database:

    def connect(self):
        self.connection = MongoClient(credentials.MONGODB_CONNECTION)
        database = self.connection['breaksDB']
        return database
    
    def close(self):
        self.connection.close()