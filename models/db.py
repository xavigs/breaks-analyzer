from credentials import *
from pymongo import MongoClient
import certifi

class Database:

    def connect(self):
        #self.connection = MongoClient(MONGODB_CONNECTION, ssl_cert_reqs=ssl.CERT_NONE)
        self.connection = MongoClient(MONGODB_CONNECTION, tlsCAFile=certifi.where())
        database = self.connection['breaksDB']
        return database

    def close(self):
        self.connection.close()
