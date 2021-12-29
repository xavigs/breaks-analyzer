from pymongo import MongoClient

class Games:

    def __init__(self, db):
        self.db = db
        self.collection = self.db['games']

    def read(self, id=None):
        if id is None:
            games = []
            gamesDB = self.collection.find()

            for game in gamesDB:
                games.append(game)
            
            return games
        else:
            return self.collection.find_one({'_id': id})
        
    def write(self, document):
        if "id" in document:
            document['_id'] = document['id']
            del document['id']
            
        self.collection.insert_one(document)