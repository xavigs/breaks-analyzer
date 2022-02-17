# -*- coding: utf-8 -*-
import json
from colorama import init, Back, Fore, Style
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
init(autoreset = True)

jsonFile = open('sofaScoreTOP500.json')
playersData = json.load(jsonFile)

for playerIndex, playerData in enumerate(playersData['rankings'][100:500]):
    print(playerData['team']['slug'])
    print(getStringFromKeyword(playerData['team']['slug']))
    playerID = playersObj.find([{'tennisExplorerName': getStringFromKeyword(playerData['team']['slug'])}])

    if playerID is None:
        print(Fore.RED + Style.BRIGHT + "[ERROR] " + Fore.WHITE + Style.NORMAL + "Player not found in the DB")
    else:
        playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])