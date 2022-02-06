# -*- coding: utf-8 -*-
import sys
import tennisExplorer
from utils import *
sys.path.insert(1, 'models')
import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
#dailyGames = te.getDailyGames()
dailyGames = tennisExplorer.getDailyGames("tomorrow")
gamesToAnalyze = []

for game in dailyGames:
    #print("-> Analyzing game ({} vs {})...".format(game['player1'], game['player2']))
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

            if avgProbability > 70 and playerData['probability'] >= 60 and opponentData['probability'] >= 60:
                x = 1

            gamesToAnalyze.append({'FS-player1': player['flashScoreName'], 'TE-player1': player['tennisExplorerName'], 'FS-player2': opponent['flashScoreName'], 'TE-player2': opponent['tennisExplorerName']})

printCollection(gamesToAnalyze)