# -*- coding: utf-8 -*-
from pymongo import MongoClient
import unicodedata

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
    
    def update(self, modifiedFields, conditions):
        document = self.collection.find_one({"$and": conditions})
        self.collection.update_one({'_id': document['_id']}, {'$set': modifiedFields})
    
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

    def update(self, modifiedFields, conditions):
        player = self.find(conditions)
        update = False
        
        if modifiedFields['flashScoreName'] == player['tennisExplorerName'] or modifiedFields['flashScoreName'].lower() == player['tennisExplorerName'].lower():
            update = True
        else:
            origText = ("-", "'", "Soonwoo", "Augustin", "Miljan", "Khumoyun", "Mathieu", "Damian", "Alejandro", "Slobodchikov", "Martinavarro", "Lukas", "Denis", "Nikita", "Jurabek", "Laurynas", "Volodymyr", "Uzhylovskyi", "Kiyamov", "Dzhanashiya", "Alexander", "Yasha", "Kosuke", "Wei Qiang", "Joan", "Prashanth", "Domenico", "Choudhary", "Tukhula", "Sander", "Jeffrey", "A.", "Shonigmatjon", "Shofayziyev", "Worovin", "Stamatios", "Oliver", "Vliegen", "Daria", "Victoria", "Liudmila", "Lesia", "Aleksandra", "Katerina", "Allie", "Tatjana", "Sofia", "Yvonne", "Peangtarn", "Plipuech", "Ilona", "Thaisa", "Zarycka", "Jasmin", "Yeonwoo", "Chiara", "Garbiela", "Tiffany", "Jundakate", "Karpovich", "Sawatdee", "Qyinlomo")
            newText = (" ", "", "Soon Woo", "Agustin", "Milan", "Khumoun", "Matthieu", "Damien", "Alex", "Slobodshikov", "Martinavarr", "Lucas", "Denys", "Mykyta", "Djurabeck", "Laurinas", "Vladimir", "Uzhylovsky", "Kiuamov", "Dzhanashia", "Sander", "Yankel", "Kousuke", "Weiqiang", "Joao", "Prasanth", "Mirko", "Chaudary", "Tuki", "A.", "Chuan En", "Aleksandar", "Nigmat", "Shofayziev", "Woravin", "Stamatis", "Olivier", "Minarik", "Darya", "Viktoria", "Ludmilla", "Lesya", "Alexandra", "Kateryna", "Alexandra", "Tatiana", "Sophia", "Ivonne", "Peangthan", "Pliphuech", "Ylona", "Thasa", "Zarytska", "Jazmin", "Yeon Woo", "Chi Chi", "Gabriela", "Tina Nadine", "Jandakate", "Mogilnitskaya", "Sawasdee", "Oyinlomo")
            flashScoreName = modifiedFields['flashScoreName']
            tennisExplorerName = unicodedata.normalize('NFKD', player['tennisExplorerName']).encode('ascii', 'ignore')

            for index in range(0, len(origText)):
                flashScoreName = flashScoreName.replace(origText[index], newText[index])
                tennisExplorerName = tennisExplorerName.replace(origText[index], newText[index])

            if flashScoreName == tennisExplorerName or tennisExplorerName in flashScoreName or flashScoreName in tennisExplorerName or flashScoreName.lower() == tennisExplorerName.lower():
                update = True
            else:
                flashScoreNameParts = flashScoreName.split(" ")
                tennisExplorerNameParts = tennisExplorerName.split(" ")

                if len(flashScoreNameParts) == 3 and flashScoreNameParts[0] + " " + flashScoreNameParts[2] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 4 and flashScoreNameParts[0] + " " + flashScoreNameParts[2] + " " + flashScoreNameParts[3] == tennisExplorerName:
                    update = True
                elif len(tennisExplorerNameParts) == 4 and tennisExplorerNameParts[0] + " " + tennisExplorerNameParts[2] + " " + tennisExplorerNameParts[3] == flashScoreName:
                    update = True
                elif len(flashScoreNameParts) == 3 and flashScoreNameParts[1] + " " + flashScoreNameParts[2] + " " + flashScoreNameParts[0] == tennisExplorerName:
                    update = True
                elif len(tennisExplorerNameParts) == 4 and tennisExplorerNameParts[0] + " " + tennisExplorerNameParts[3] == flashScoreName:
                    update = True
                elif len(flashScoreNameParts) == 4 and flashScoreNameParts[2] + " " + flashScoreNameParts[0] + " " + flashScoreNameParts[3] == tennisExplorerName:
                    update = True
                elif len(tennisExplorerNameParts) == 3 and tennisExplorerNameParts[0] + " " + tennisExplorerNameParts[2] == flashScoreName:
                    update = True
                elif len(flashScoreNameParts) == 4 and flashScoreNameParts[0] + " " + flashScoreNameParts[2] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 4 and flashScoreNameParts[0] + " " + flashScoreNameParts[3] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 3 and flashScoreNameParts[1] + " " + flashScoreNameParts[0] + " " + flashScoreNameParts[2] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 4 and flashScoreNameParts[3] + " " + flashScoreNameParts[0] + " " + flashScoreNameParts[1] + " " + flashScoreNameParts[2] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 5 and flashScoreNameParts[1] + " " + flashScoreNameParts[0] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 3 and flashScoreNameParts[0] + " " + flashScoreNameParts[2] + " " + flashScoreNameParts[1] == tennisExplorerName:
                    update = True
                elif len(flashScoreNameParts) == 5 and flashScoreNameParts[3] + " " + flashScoreNameParts[4] + " " + flashScoreNameParts[0] + " " + flashScoreNameParts[1] + " " + flashScoreNameParts[2] == tennisExplorerName:
                    update = True
        
        if update:
            MongoObject.update(self, modifiedFields, conditions)
        else:
            print("# The player " + modifiedFields['flashScoreName'] + " (" + str(conditions[0]['startingRanking']) + ") has not updated")
            exit()