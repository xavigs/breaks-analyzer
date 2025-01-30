# -*- coding: utf-8 -*-
import os
import socket
from datetime import datetime, timedelta
import click
import sofaScore
import itfTennis
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
playersMissingObj = objects.PlayersMissing(breaksDB)
gamesObj = objects.Games(breaksDB)

@click.command()
@click.option(
    '-s', '--sex',
    help = "Sex players to check breaks", type = str, default = "M", show_default = True
)
@click.option(
    '-f', '--from-player',
    help = "Index player that we check breaks from", type = int, default = 0, show_default = True
)
@click.option(
    '-l', '--limit-player',
    help = "Index player that we check breaks to", type = int, default = 999999, show_default = True
)

def getBreakDataFromSofaScore(sex, from_player, limit_player):
    if from_player == 0 and limit_player == 999999:
        playersDB = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}])
    elif from_player > 0 and limit_player == 999999:
        playersDB = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}, {'startingRanking': {"$gt": from_player}}])
    elif from_player > 0 and limit_player < 999999:
        playersDB = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}, {'startingRanking': {"$gt": from_player}}, {'startingRanking': {'$lte': limit_player }}])

    players = [playerDB for playerDB in playersDB]

    for player in players:
        if 'toModify' not in player or not player['toModify']:
            continue
        else:
            playerMissingDB = playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}])

            if playerMissingDB is None:
                rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
                print("\n" + "-" * (rankingNameLength + 25))

                if 'flashScoreName' in player and player['flashScoreName'] != "":
                    playerName = player['flashScoreName']
                else:
                    playerName = player['tennisExplorerName']

                print(u"|          ({}) {}          |".format(player['startingRanking'], playerName.upper()).encode('utf-8'))
                print('-' * (rankingNameLength + 25))
                lastGames = {'definedGames': player['definedGames'], 'games': []}

                for game in player['lastGames']:
                    error = False
                    previousGame = {}
                    opponent = playersObj.find([{'_id': game['opponent']}])

                    if opponent is None:
                        playerMissing = {
                            'sex': sex,
                            'opponent': game['opponent'],
                            'player': player['tennisExplorerName'],
                            'playerRanking': player['startingRanking'],
                        }
                        playersMissingObj.create(playerMissing)
                        error = True
                    elif 'sofaScoreID' in opponent:
                        previousGame['opponent'] = opponent['sofaScoreID']
                    else:
                        playerMissing = {
                            'sex': sex,
                            'opponent': game['opponent'],
                            'player': player['tennisExplorerName'],
                            'playerRanking': player['startingRanking'],
                            'sofaScoreID': opponent['startingRanking']
                        }
                        playersMissingObj.create(playerMissing)
                        print('⚠️  The opponent {} does not have sofaScoreID'.format(game['opponent']))
                        error = True

                    previousGame['date'] = game['time']
                    previousGame['breakDone'] = game['breakDone']
                    previousGame['breakReceived'] = game['breakReceived']
                    previousGame['error'] = error
                    lastGames['games'].append(previousGame)

                lastGamesBreaks = sofaScore.checkBreaksUndefinedGamesByPlayer(player['sofaScoreID'], lastGames)
                playersObj.updateBreakData(player['_id'], lastGamesBreaks)

                # Get ITF Breaks Data
                playerDB = playersObj.find([{'_id': player['_id']}])
                lastGames = {'definedGames': player['definedGames'], 'games': []}

                for gameIndex, gameData in enumerate(playerDB['lastGames']):
                    previousGame = {'index': gameIndex, 'breakDone': gameData['breakDone'], 'breakReceived': gameData['breakReceived']}
                    opponent = playersObj.find([{'_id': gameData['opponent']}])

                    if opponent is not None and (gameData['breakDone'] == -1 or gameData['breakReceived'] == -1):
                        # Breaks not defined yet; verify if the game is ITF
                        print('ITF: {} - {}'.format(gameData['time'], gameData['opponent']))
                        gameDB = gamesObj.find([{'gameDay': gameData['time'], 'player1ID': player['_id'], 'player2ID': gameData['opponent']}])

                        if gameDB is None:
                            gameDB = gamesObj.find([{'gameDay': gameData['time'], 'player2ID': player['_id'], 'player1ID': gameData['opponent']}])
                        
                        if gameDB is None:
                            nextYear = int(gameData['time'][:4]) + 1
                            gameData['time'] = '{}-{}'.format(nextYear, gameData['time'][5:10])
                            gameDB = gamesObj.find([{'gameDay': gameData['time'], 'player1ID': player['_id'], 'player2ID': gameData['opponent']}])
                        
                        if gameDB is None:
                            gameDB = gamesObj.find([{'gameDay': gameData['time'], 'player2ID': player['_id'], 'player1ID': gameData['opponent']}])

                        if gameDB is not None and '-itf-' in gameDB['tournament']:
                            breakStats = itfTennis.findBreakStats(gameDB, player['tennisExplorerName'], player['flashScoreName'])

                            if 'player' in breakStats and 'opponent' in breakStats:
                                print('Breaks stats found!')
                                if breakStats['player'] > 0:
                                    previousGame['breakDone'] = 1
                                else:
                                    previousGame['breakDone'] = 0

                                if breakStats['opponent'] > 0:
                                    previousGame['breakReceived'] = 1
                                else:
                                    previousGame['breakReceived'] = 0

                                lastGames['definedGames'] += 1
                            else:
                                print('Breaks stats not found')

                    lastGames['games'].append(previousGame)

                playersObj.updateBreakData(player['_id'], lastGames)
                playersObj.printBreakData(player['_id'])

    currentTime = datetime.now().strftime('%H:%M')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    machineName = socket.gethostname()
    currentPath = os.path.dirname(os.path.abspath(__file__))
    print('Current path: {}'.format(currentPath))

    if machineName == 'juxtelab-pc':
        pythonPath = 'python'
    else:
        pythonPath = '/root/.virtualenvs/breaks/bin/python'

    if currentTime < '12:00':
        script = '{} {}/08-analyzeBreakData.py > /tmp/breaks-8M.log 2>&1'.format(pythonPath, currentPath)
        
    else:
        script = '{} {}/08-analyzeBreakData.py -d {} > /tmp/breaks-8M.log 2>&1'.format(pythonPath, currentPath, tomorrow)
    
    print('Executing script {}...'.format(script))
    os.system(script)

if __name__ == '__main__':
    getBreakDataFromSofaScore()
