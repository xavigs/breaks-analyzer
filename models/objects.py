# -*- coding: utf-8 -*-
from pymongo import MongoClient
import unicodedata
from utils import *

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

    def find_all(self, conditions=None):
        if conditions is None:
            return self.collection.find()
        else:
            return self.collection.find({'$and': conditions})

    def find(self, conditions):
        return self.collection.find_one({'$and': conditions})

    def create(self, document):
        if "id" in document:
            document['_id'] = document['id']
            del document['id']

        if "_id" in document:
            existingObject = self.collection.find_one({'_id': document['_id']})
        else:
            existingObject = None

        if existingObject is None:
            self.collection.insert_one(document)

    def update(self, modifiedFields, conditions):
        document = self.collection.find_one({"$and": conditions})
        self.collection.update_one({'_id': document['_id']}, {'$set': modifiedFields})

    def delete(self, conditions):
        return self.collection.delete_many({'$and': conditions})

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

    def getMen(self):
        return self.find_all([{'sex': 'M'}]).sort([("startingRanking", 1)])

    def getWomen(self):
        return self.find_all([{'sex': 'W'}]).sort([("startingRanking", 1)])

    def getMenWithSofaScoreID(self, from_player = 0, limit_player = 999999):
        return self.find_all([{'sex': 'M'}, {'startingRanking': {'$gt': from_player}}, {'startingRanking': {'$lte': limit_player}}, {'sofaScoreID': {'$exists': True}}]).sort([("startingRanking", 1)])

    def getWomenWithSofaScoreID(self, from_player = 0, limit_player = 999999):
        return self.find_all([{'sex': 'W'}, {'startingRanking': {'$gt': from_player}}, {'startingRanking': {'$lte': limit_player}}, {'sofaScoreID': {'$exists': True}}]).sort([("startingRanking", 1)])

    def getMenWithLastGames(self, from_player = 0, limit_player = 999999):
        return self.find_all([{'sex': 'M'}, {'startingRanking': {'$gt': from_player}}, {'startingRanking': {'$lte': limit_player}}, {'lastGames': {'$exists': True}}]).sort([("startingRanking", 1)])

    def getWomenWithLastGames(self, from_player = 0, limit_player = 999999):
        return self.find_all([{'sex': 'W'}, {'startingRanking': {'$gt': from_player}}, {'startingRanking': {'$lte': limit_player}}, {'lastGames': {'$exists': True}}]).sort([("startingRanking", 1)])

    def update(self, modifiedFields, conditions):
        player = self.find(conditions)
        update = False

        if "flashScoreName" in modifiedFields:
            if modifiedFields['flashScoreName'] == player['tennisExplorerName'] or modifiedFields['flashScoreName'].lower() == player['tennisExplorerName'].lower():
                update = True
            else:
                origText = ("-", "'", "Soonwoo", "Augustin", "Miljan", "Khumoyun", "Mathieu", "Damian", "Alejandro", "Slobodchikov", "Martinavarro", "Lukas", "Denis", "Nikita", "Jurabek", "Laurynas", "Volodymyr", "Uzhylovskyi", "Kiyamov", "Dzhanashiya", "Alexander", "Yasha", "Kosuke", "Wei Qiang", "Joan", "Prashanth", "Domenico", "Choudhary", "Tukhula", "Sander", "Jeffrey", "A.", "Shonigmatjon", "Shofayziyev", "Worovin", "Stamatios", "Oliver", "Vliegen", "Daria", "Victoria", "Liudmila", "Lesia", "Aleksandra", "Katerina", "Allie", "Tatjana", "Sofia", "Yvonne", "Peangtarn", "Plipuech", "Ilona", "Thaisa", "Zarycka", "Jasmin", "Yeonwoo", "Chiara", "Garbiela", "Tiffany", "Jundakate", "Karpovich", "Sawatdee", "Qyinlomo", "Moeller", "Ghedjemis", "Rayan", "Maksim", "Hong kit", "Yecong", "Isarow", "Tagushi", "Minh Tuan", "Al Azmeh", "Leevi", "Coco", "Ekaterina", "Nadiya", "Nicole", "Young Suh", "Jr.", "Melissa")
                newText = (" ", "", "Soon Woo", "Agustin", "Milan", "Khumoun", "Matthieu", "Damien", "Alex", "Slobodshikov", "Martinavarr", "Lucas", "Denys", "Mykyta", "Djurabeck", "Laurinas", "Vladimir", "Uzhylovsky", "Kiuamov", "Dzhanashia", "Sander", "Yankel", "Kousuke", "Weiqiang", "Joao", "Prasanth", "Mirko", "Chaudary", "Tuki", "A.", "Chuan En", "Aleksandar", "Nigmat", "Shofayziev", "Woravin", "Stamatis", "Olivier", "Minarik", "Darya", "Viktoria", "Ludmilla", "Lesya", "Alexandra", "Kateryna", "Alexandra", "Tatiana", "Sophia", "Ivonne", "Peangthan", "Pliphuech", "Ylona", "Thasa", "Zarytska", "Jazmin", "Yeon Woo", "Chi Chi", "Gabriela", "Tina Nadine", "Jandakate", "Mogilnitskaya", "Sawasdee", "Oyinlomo", "Moller", "Roumane", "Rayane", "Maxim", "Hong Kit Jack", "Ye Cong", "Isaro", "Taguchi", "Minhtuan", "Alazmeh", "Levi", "Cori", "Tatiana", "Nadya", "Nikol", "Youngsuh", "", "Melisa")
                flashScoreName = modifiedFields['flashScoreName']
                tennisExplorerName = unicodedata.normalize('NFKD', player['tennisExplorerName']).encode('ascii', 'ignore')

                for index in range(0, len(origText)):
                    flashScoreName = flashScoreName.replace(origText[index], newText[index])
                    tennisExplorerName = tennisExplorerName.replace(origText[index], newText[index])

                '''print(flashScoreName)
                print(tennisExplorerName)
                exit()'''

                if flashScoreName == tennisExplorerName or tennisExplorerName in flashScoreName or flashScoreName in tennisExplorerName or flashScoreName.lower() == tennisExplorerName.lower():
                    update = True
                else:
                    flashScoreNameParts = flashScoreName.split(" ")
                    tennisExplorerNameParts = tennisExplorerName.split(" ")

                    if len(flashScoreNameParts) == 3 and flashScoreNameParts[0] + " " + flashScoreNameParts[2] == tennisExplorerName:
                        update = True
                    elif len(flashScoreNameParts) == 2 and flashScoreNameParts[1] + " " + flashScoreNameParts[0] == tennisExplorerName:
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
                    elif len(tennisExplorerNameParts) == 4 and tennisExplorerNameParts[0] + " " + tennisExplorerNameParts[1] + " " + tennisExplorerNameParts[3] == flashScoreName:
                        update = True
                    elif len(flashScoreNameParts) == 3 and flashScoreNameParts[2] + " " + flashScoreNameParts[0] + " " + flashScoreNameParts[1] == tennisExplorerName:
                        update = True
                    elif len(tennisExplorerNameParts) == 4 and tennisExplorerNameParts[2] + " " + tennisExplorerNameParts[0] + " " + tennisExplorerNameParts[1] == flashScoreName:
                        update = True
                    elif len(tennisExplorerNameParts) == 5 and tennisExplorerNameParts[4] + " " + tennisExplorerNameParts[3] == flashScoreName:
                        update = True

            if update:
                MongoObject.update(self, modifiedFields, conditions)
                return True
            else:
                print("# The player " + modifiedFields['flashScoreName'] + " (" + str(conditions[0]['startingRanking']) + ") has not updated")
                return False
        else:
            MongoObject.update(self, modifiedFields, conditions)

    def updateBreakData(self, playerID, lastGamesBreaks):
        #printCollection(lastGamesBreaks)
        player = self.read(playerID)
        conditions = [{'_id': playerID}]
        modifiedFields = {'definedGames': lastGamesBreaks['definedGames'], 'lastGames': player['lastGames']}
        indexToSubstract = 0
        #printCollection(modifiedFields)

        for lastGameBreaks in lastGamesBreaks['games']:
            if "toDelete" in lastGameBreaks:
                del modifiedFields['lastGames'][lastGameBreaks['index'] - indexToSubstract]
                indexToSubstract += 1
            else:
                if modifiedFields['lastGames'][lastGameBreaks['index'] - indexToSubstract]['breakDone'] == -1:
                    modifiedFields['lastGames'][lastGameBreaks['index'] - indexToSubstract]['breakDone'] = lastGameBreaks['breakDone']

                if modifiedFields['lastGames'][lastGameBreaks['index'] - indexToSubstract]['breakReceived'] == -1:
                    modifiedFields['lastGames'][lastGameBreaks['index'] - indexToSubstract]['breakReceived'] = lastGameBreaks['breakReceived']

        self.update(modifiedFields, conditions)

    def printBreakData(self, playerID):
        player = self.read(playerID)
        if player['definedGames'] < 8:
            print("\t⚠ Defined games: {}".format(player['definedGames']))
        else:
            print("\t✅ Defined games: {}".format(player['definedGames']))

        for game in player['lastGames']:
            numSpaces = 21 - len(game['opponent'])
            print("\t📌 Opponent: {}".format(game['opponent']) + " " * numSpaces + "| Break done: {} • Break received: {}".format(game['breakDone'], game['breakReceived']))

class PlayersMissing(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['playersMissing']

class Tournaments(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['tournaments']

class Systems(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['systems']

class PicksTelegram(MongoObject):

    def __init__(self, db):
        MongoObject.__init__(self, db)
        self.collection = self.db['picksTelegram']
