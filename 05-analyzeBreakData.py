# -*- coding: utf-8 -*-
from datetime import date, timedelta
import tennisExplorer
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
gamesObj = objects.Games(breaksDB)
day = "today"
sex = "men"
dailyGames = tennisExplorer.getDailyGames(day, sex)
gamesToAnalyze = []

if day == "today":
    dayDatetime = date.today()
else:
    dayDatetime = date.today() + timedelta(days=1)

dayString = dayDatetime.strftime("%Y-%m-%d")

for game in dailyGames:
    print("-> Analyzing game ({} vs {})...".format(game['player1'], game['player2']))
    player = playersObj.read(game['player1'])
    opponent = playersObj.read(game['player2'])
    playerData = {
        'definedGames': 0,
        'totalBreaksDone': 0,
        'probability': 0
    }
    opponentData = {
        'definedGames': 0,
        'totalBreaksReceived': 0,
        'probability': 0
    }

    if "lastGames" in player:
        for previousGame in player['lastGames']:
            if playerData['definedGames'] == 5 and playerData['totalBreaksDone'] < 3 or playerData['definedGames'] >= 5 and previousGame['breakDone'] == 0:
                break
            else:
                if "breakDone" in previousGame and "breakReceived" in previousGame:
                    if previousGame['breakDone'] > -1:
                        playerData['definedGames'] += 1

                        if previousGame['breakDone'] == 1:
                            playerData['totalBreaksDone'] += 1

        if playerData['definedGames'] > 0:
            playerData['probability'] = playerData['totalBreaksDone'] * 100 / playerData['definedGames']
        else:
            playerData['probability'] = 0
        #print(playerData['probability'])

        if "lastGames" in opponent:
            for previousGame in opponent['lastGames']:
                if opponentData['definedGames'] == 5 and opponentData['totalBreaksReceived'] < 3 or opponentData['definedGames'] >= 5 and previousGame['breakReceived'] == 0:
                    break
                else:
                    if "breakDone" in previousGame and "breakReceived" in previousGame:
                        if previousGame['breakDone'] > -1:
                            opponentData['definedGames'] += 1

                            if previousGame['breakReceived'] == 1:
                                opponentData['totalBreaksReceived'] += 1

            if opponentData['definedGames'] > 0:
                opponentData['probability'] = opponentData['totalBreaksReceived'] * 100 / opponentData['definedGames']
            else:
                opponentData['probability'] = 0

            #print(opponentData['probability'])
            avgProbability = (playerData['probability'] + opponentData['probability']) / 2
            #print(avgProbability)

            if playerData['definedGames'] >= 5 and opponentData['definedGames'] >= 5 and avgProbability > 70 and playerData['probability'] >= 60 and opponentData['probability'] >= 60:
                profitable = True
            else:
                profitable = False

            gameDocument = {'gameDay': dayString, 'player1ID': player['_id'], 'FS-player1': player['flashScoreName'], 'TE-player1': player['tennisExplorerName'], 'player2ID': opponent['_id'], 'FS-player2': opponent['flashScoreName'], 'TE-player2': opponent['tennisExplorerName'], 'playerData': playerData, 'opponentData': opponentData, 'probability': avgProbability, 'profitable': profitable}
            gamesObj.create(gameDocument)

            if profitable:
                gamesToAnalyze.append(gameDocument)

printCollection(gamesToAnalyze)