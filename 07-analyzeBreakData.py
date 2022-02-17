# -*- coding: utf-8 -*-
from __future__ import division
from datetime import date, datetime, timedelta
import click
import tennisExplorer
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
gamesObj = objects.Games(breaksDB)

@click.command()
@click.option(
    '-d', '--day',
    help = "Date to analyze break data", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)
@click.option(
    '-s', '--sex',
    help = "Sex players to analyze break data", type = str, default = "M", show_default = True
)

def analyzeBreakData(day, sex):
    sexKeywords = {'M': 'men', 'W': 'women'}
    dailyGames = tennisExplorer.getDailyGames(day, sexKeywords[sex])
    gamesToAnalyze = [] 
    gamesObj.delete([{'gameDay': day}, {'sex': sex}])

    for game in dailyGames:
        print("-> Analyzing game ({} vs {})...".format(game['player1'], game['player2']))
        player = playersObj.read(game['player1'])
        opponent = playersObj.read(game['player2'])
        playerData = {
            'totalGames': 0,
            'definedGames': 0,
            'totalBreaksDone': 0,
            'probability': 0.0
        }
        opponentData = {
            'totalGames': 0,
            'definedGames': 0,
            'totalBreaksReceived': 0,
            'probability': 0.0
        }

        if player is not None and "lastGames" in player:
            for previousGame in player['lastGames']:
                if playerData['totalGames'] == 5 and playerData['totalBreaksDone'] < 3 or playerData['totalGames'] >= 5 and previousGame['breakDone'] < 1:
                    break
                else:
                    playerData['totalGames'] += 1

                    if "breakDone" in previousGame and "breakReceived" in previousGame:
                        if previousGame['breakDone'] > -1:
                            playerData['definedGames'] += 1

                            if previousGame['breakDone'] == 1:
                                playerData['totalBreaksDone'] += 1

            if playerData['totalGames'] > 0:
                playerData['probability'] = round(playerData['totalBreaksDone'] * 100 / playerData['totalGames'], 2)
            else:
                playerData['probability'] = 0.0
            #print(playerData['probability'])

            if opponent is not None and "lastGames" in opponent:
                for previousGame in opponent['lastGames']:
                    if opponentData['totalGames'] == 5 and opponentData['totalBreaksReceived'] < 3 or opponentData['totalGames'] >= 5 and previousGame['breakReceived'] < 1:
                        break
                    else:
                        opponentData['totalGames'] += 1

                        if "breakDone" in previousGame and "breakReceived" in previousGame:
                            if previousGame['breakReceived'] > -1:
                                opponentData['definedGames'] += 1

                                if previousGame['breakReceived'] == 1:
                                    opponentData['totalBreaksReceived'] += 1

                if opponentData['totalGames'] > 0:
                    opponentData['probability'] = round(opponentData['totalBreaksReceived'] * 100 / opponentData['totalGames'], 2)
                else:
                    opponentData['probability'] = 0.0

                #print(opponentData['probability'])
                avgProbability = round((playerData['probability'] + opponentData['probability']) / 2, 2)
                #print(avgProbability)

                if playerData['totalGames'] >= 5 and opponentData['totalGames'] >= 5 and avgProbability > 70 and playerData['probability'] >= 60 and opponentData['probability'] >= 60:
                    profitable = True
                else:
                    profitable = False

                gameDocument = {'sex': sex, 'tournament': game['tournament'], 'gameDay': day, 'player1ID': player['_id'], 'FS-player1': player['flashScoreName'], 'TE-player1': player['tennisExplorerName'], 'player2ID': opponent['_id'], 'FS-player2': opponent['flashScoreName'], 'TE-player2': opponent['tennisExplorerName'], 'playerData': playerData, 'opponentData': opponentData, 'probability': avgProbability, 'profitable': profitable}
                gamesObj.create(gameDocument)

                if profitable:
                    gamesToAnalyze.append(gameDocument)

    printCollection(gamesToAnalyze)

if __name__ == '__main__':
    analyzeBreakData()