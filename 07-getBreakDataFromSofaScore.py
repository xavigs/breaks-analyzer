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
    help = "Index player that we check breaks to", type = int, default = 200, show_default = True
)

def getBreakDataFromSofaScore(sex, from_player, limit_player):
    players = playersObj.find_all([{'sex': sex}, {'definedGames': {"$lt": 8}}, {'startingRanking': {"$gt": from_player}}, {'startingRanking': {'$lte': limit_player }}])
    
    for player in players:
        playerMissingDB = playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}])
        
        if playerMissingDB is not None:
            rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
            print("\n" + "-" * (rankingNameLength + 25))
            print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].upper()))
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
                    print("⚠️  The opponent {} does not have sofaScoreID.".format(game['opponent']))

                previousGame['date'] = game['time']
                previousGame['breakDone'] = game['breakDone']
                previousGame['breakReceived'] = game['breakReceived']
                lastGames['games'].append(previousGame)
            
            if not error:
                lastGamesBreaks = sofaScore.checkBreaksUndefinedGamesByPlayer(player['sofaScoreID'], lastGames)
                playersObj.updateBreakData(player['_id'], lastGamesBreaks)
                playersObj.printBreakData(player['_id'])

if __name__ == '__main__':
    getBreakDataFromSofaScore()