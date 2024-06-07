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
    help = "Index player that we check breaks to", type = int, default = 999999, show_default = True
)


def checkBreaks(sex, from_player, limit_player):
    if from_player == 0 and limit_player == 999999:
        if sex == "M":
            players = playersObj.getMenWithLastGames()
        else:
            players = playersObj.getWomenWithLastGames()
    elif from_player > 0 and limit_player == 999999:
        if sex == "M":
            players = playersObj.getMenWithLastGames(from_player)
        else:
            players = playersObj.getWomenWithLastGames(from_player)
    elif from_player > 0 and limit_player < 999999:
        if sex == "M":
            players = playersObj.getMenWithLastGames(from_player, limit_player)
        else:
            players = playersObj.getWomenWithLastGames(from_player, limit_player)

    for player in players:
        if 'toModify' not in player or not player['toModify']:
            continue
        else:
            rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
            print("\n" + "-" * (rankingNameLength + 25))
            print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].encode('utf-8').upper()))
            print("-" * (rankingNameLength + 25))
            lastGames = []
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
                elif "flashScoreId" in opponent:
                    previousGame['opponent'] = opponent['flashScoreId']
                    previousGame['date'] = game['time']
                    lastGames.append(previousGame)
                else:
                    playerMissing = {
                        'sex': sex,
                        'opponent': game['opponent'],
                        'player': player['tennisExplorerName'],
                        'playerRanking': player['startingRanking']
                    }
                    playersMissingObj.create(playerMissing)
                    error = True

            if not error and player['flashScoreId'] != "" and len(lastGames):
                lastGamesBreaks = flashScore.checkBreaksLastGamesByPlayer(player['flashScoreId'], player['flashScoreName'], lastGames)
                #lastGamesBreaks = flashScore.newCheckBreaksLastGamesByPlayer(player['flashScoreId'], lastGames)
                playersObj.updateBreakData(player['_id'], lastGamesBreaks)
                playersObj.printBreakData(player['_id'])

if __name__ == '__main__':
    checkBreaks()
