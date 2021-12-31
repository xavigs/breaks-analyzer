from pymongo import MongoClient

class MongoObject:

    def __init__(self, db):
        self.db = db

    def read(self, id=None):
        if id is None:
            documents = []
            documentsDB = self.collection.find()

            for document in documentsDB:
                documents.append(document)
            
            return documents
        else:
            return self.collection.find_one({'_id': id})
    
    def find(self, conditions):
        return self.collection.find_one({'$and': conditions})
        
    def create(self, document):
        if "id" in document:
            document['_id'] = document['id']
            del document['id']

        existingObject = self.collection.find_one({'_id': document['_id']})
        
        if existingObject is None:
            self.collection.insert_one(document)
    
    def empty(self):
        self.collection.delete_many({})

class Games(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['games']

class Players(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['players']