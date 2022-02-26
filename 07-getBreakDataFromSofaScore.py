# -*- coding: utf-8 -*-
import click
import sofaScore
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)

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
        rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
        print("\n" + "-" * (rankingNameLength + 25))
        print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].upper()))
        print("-" * (rankingNameLength + 25))
        lastGames = []

        for game in player['lastGames']:
            previousGame = {}
            opponent = playersObj.find([{'_id': game['opponent']}])

            if opponent is None:
                print("❌ The opponent {} is not into the database.".format(game['opponent']))
                exit()
            elif "sofaScoreID" in opponent:
                previousGame['opponent'] = opponent['sofaScoreID']
                previousGame['date'] = game['time']
                previousGame['breakDone'] = game['breakDone']
                previousGame['breakReceived'] = game['breakReceived']
                lastGames.append(previousGame)
            else:
                print("❌ The opponent {} does not have sofaScoreID.".format(game['opponent']))
                exit()
        
        lastGamesBreaks = sofaScore.checkBreaksUndefinedGamesByPlayer(player['sofaScoreID'], lastGames)
        print(lastGamesBreaks)

if __name__ == '__main__':
    getBreakDataFromSofaScore()