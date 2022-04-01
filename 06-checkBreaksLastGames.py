# -*- coding: utf-8 -*-
import os
from datetime import datetime
import click
import flashScore
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


def checkBreaks(sex, from_player, limit_player):
    errors = []

    if sex == "M":
        players = playersObj.read()
    else:
        players = playersObj.getWomen()

    for player in players[from_player:limit_player]:
        rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
        print("\n" + "-" * (rankingNameLength + 25))
        print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].upper()))
        print("-" * (rankingNameLength + 25))
        lastGames = []
        error = False

        for game in player['lastGames']:
            previousGame = {}
            opponent = playersObj.find([{'_id': game['opponent']}])

            if opponent is None:
                playerMissing = {
                    'opponent': game['opponent'],
                    'player': player['tennisExplorerName'],
                    'playerRanking': player['startingRanking']
                }
                playersMissingObj.create(playerMissing)
                error = True
            elif "flashScoreId" in opponent:
                previousGame['opponent'] = opponent['flashScoreId']
                previousGame['date'] = game['time']
                lastGames.append(previousGame)
            else:
                playerMissing = {
                    'opponent': game['opponent'],
                    'player': player['tennisExplorerName'],
                    'playerRanking': player['startingRanking']
                }
                playersMissingObj.create(playerMissing)
                error = True
        
        if not error and player['flashScoreId'] != "":
            lastGamesBreaks = flashScore.checkBreaksLastGamesByPlayer(player['flashScoreId'], player['flashScoreName'], lastGames)
            #lastGamesBreaks = flashScore.newCheckBreaksLastGamesByPlayer(player['flashScoreId'], lastGames)
            playersObj.updateBreakData(player['_id'], lastGamesBreaks)
            playersObj.printBreakData(player['_id'])

if __name__ == '__main__':
    checkBreaks()