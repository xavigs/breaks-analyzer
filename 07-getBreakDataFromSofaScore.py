# -*- coding: utf-8 -*-
import click
import sofaScore
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
playersMissingObj = objects.PlayersMissing(breaksDB)

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
        players = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}])
    elif from_player > 0 and limit_player == 999999:
        players = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}, {'startingRanking': {"$gt": from_player}}])
    elif from_player > 0 and limit_player < 999999:
        players = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}, {'startingRanking': {"$gt": from_player}}, {'startingRanking': {'$lte': limit_player }}])

    for i in range(3):
        try:
            for player in players:
                playerMissingDB = playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}])

                if playerMissingDB is None:
                    rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
                    print("\n" + "-" * (rankingNameLength + 25))

                    if "flashScoreName" in player and player['flashScoreName'] != "":
                        playerName = player['flashScoreName']
                    else:
                        playerName = player['tennisExplorerName']

                    print(u"|          ({}) {}          |".format(player['startingRanking'], playerName.upper()))
                    print("-" * (rankingNameLength + 25))
                    lastGames = {'definedGames': player['definedGames'], 'games': []}
                    error = False

                    for game in player['lastGames']:
                        previousGame = {}
                        opponent = playersObj.find([{'_id': game['opponent']}])

                        if opponent is None:
                            playerMissing = {
                                'sex': sex,
                                'opponent': game['opponent'],
                                'player': player['tennisExplorerName'],
                                'playerRanking': player['startingRanking']
                            }
                            playersMissingObj.create(playerMissing)
                            error = True
                        elif "sofaScoreID" in opponent:
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
                            print("⚠️  The opponent {} does not have sofaScoreID.".format(game['opponent']))

                        previousGame['date'] = game['time']
                        previousGame['breakDone'] = game['breakDone']
                        previousGame['breakReceived'] = game['breakReceived']
                        lastGames['games'].append(previousGame)

                    if not error:
                        lastGamesBreaks = sofaScore.checkBreaksUndefinedGamesByPlayer(player['sofaScoreID'], lastGames)
                        playersObj.updateBreakData(player['_id'], lastGamesBreaks)
                        playersObj.printBreakData(player['_id'])
            break
        except:
            if i == 2:
                raise
            continue

if __name__ == '__main__':
    getBreakDataFromSofaScore()
