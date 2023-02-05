# -*- coding: utf-8 -*-
from __future__ import division
from datetime import date, datetime, timedelta
import click
import tennisExplorer
from colorama import init, Back, Fore, Style
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
playersMissingObj = objects.PlayersMissing(breaksDB)
init(autoreset = True)

@click.command()
@click.option(
    '-d', '--day',
    help = "Date to analyze break data", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)
@click.option(
    '-s', '--sex',
    help = "Sex players to analyze break data", type = str, default = "M", show_default = True
)

def getMissingPlayers(day, sex):
    sexKeywords = {'M': 'men', 'W': 'women'}
    dailyGames = tennisExplorer.getDailyGames(day, sexKeywords[sex])
    missingPlayers = {}
    errors = []

    for game in dailyGames:
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

        if player is None and game['player1'] not in missingPlayers:
            missingPlayers[game['player1']] = "db"
            error = {}
            error['type'] = "db"
            error['player'] = game['player1']
            error['ranking'] = 0
            errors.append(error)
        elif player is not None and "lastGames" not in player and game['player1'] not in missingPlayers:
            missingPlayers[game['player1']] = player['startingRanking']
            error = {}
            error['type'] = "lastGames"
            error['player'] = game['player1']
            error['ranking'] = player['startingRanking']
            errors.append(error)
        elif player is not None and game['player1'] not in missingPlayers and playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}]) is not None and "sofaScoreID" not in playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}]):
            missingPlayers[game['player1']] = "missing{}".format(player['startingRanking'])
            error = {}
            error['type'] = "playersMissing"
            error['player'] = game['player1']
            error['ranking'] = player['startingRanking']
            error['count'] = len(list(playersMissingObj.find_all([{'sex': sex}, {'playerRanking': player['startingRanking']}])))
            errors.append(error)
        elif player is not None and game['player1'] not in missingPlayers and playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}]) is not None and "sofaScoreID" in playersMissingObj.find([{'sex': sex}, {'playerRanking': player['startingRanking']}]):
            missingPlayers[game['player1']] = "missing{}".format(player['startingRanking'])
            error = {}
            error['type'] = "sofaScore"
            error['player'] = game['player1']
            error['ranking'] = player['startingRanking']
            error['count'] = len(list(playersMissingObj.find_all([{'sex': sex}, {'playerRanking': player['startingRanking']}])))
            errors.append(error)

        if opponent is None and game['player2'] not in missingPlayers:
            missingPlayers[game['player2']] = "db"
            error = {}
            error['type'] = "db"
            error['player'] = game['player2']
            error['ranking'] = 0
            errors.append(error)
        elif opponent is not None and "lastGames" not in opponent and game['player2'] not in missingPlayers:
            missingPlayers[game['player2']] = opponent['startingRanking']
            error = {}
            error['type'] = "lastGames"
            error['player'] = game['player2']
            error['ranking'] = opponent['startingRanking']
            errors.append(error)
        elif opponent is not None and game['player2'] not in missingPlayers and playersMissingObj.find([{'sex': sex}, {'playerRanking': opponent['startingRanking']}]) is not None and "sofaScoreID" not in playersMissingObj.find([{'sex': sex}, {'playerRanking': opponent['startingRanking']}]):
            missingPlayers[game['player2']] = "missing{}".format(opponent['startingRanking'])
            error = {}
            error['type'] = "playersMissing"
            error['player'] = game['player2']
            error['ranking'] = opponent['startingRanking']
            error['count'] = len(list(playersMissingObj.find_all([{'sex': sex}, {'playerRanking': opponent['startingRanking']}])))
            errors.append(error)
        elif opponent is not None and game['player2'] not in missingPlayers and playersMissingObj.find([{'sex': sex}, {'playerRanking': opponent['startingRanking']}]) is not None and "sofaScoreID" in playersMissingObj.find([{'sex': sex}, {'playerRanking': opponent['startingRanking']}]):
            missingPlayers[game['player2']] = "missing{}".format(opponent['startingRanking'])
            error = {}
            error['type'] = "sofaScore"
            error['player'] = game['player2']
            error['ranking'] = opponent['startingRanking']
            error['count'] = len(list(playersMissingObj.find_all([{'sex': sex}, {'playerRanking': opponent['startingRanking']}])))
            errors.append(error)

    errors = sorted(errors, key=lambda d: (d['type'], d['ranking']))

    for error in errors:
        if error['type'] == "db":
            print(Fore.GREEN + Style.BRIGHT + "[DATABASE] " + Fore.RESET + Style.NORMAL + "El jugador {} no està introduït a la base de dades.".format(error['player']))
        elif error['type'] == "playersMissing":
            print(Fore.YELLOW + Style.BRIGHT + "[MISSING-OPPONENTS] " + Fore.RESET + Style.NORMAL + "Al jugador {} ({}) li falten {} rivals que es troben a playersMissing.".format(error['player'], error['ranking'], error['count']))
        elif error['type'] == "lastGames":
            print(Fore.RED + Style.BRIGHT + "[LAST-GAMES] " + Fore.RESET + Style.NORMAL + "El jugador {} ({}) no té el camp lastGames definit.".format(error['player'], error['ranking']))
        else:
            if error['count'] > 1:
                print(Fore.BLUE + Style.BRIGHT + "[SOFA-SCORE] " + Fore.RESET + Style.NORMAL + "A {} rivals del jugador {} ({}) els falta l'ID de SofaScore.".format(error['count'], error['player'], error['ranking']))
            else:
                print(Fore.BLUE + Style.BRIGHT + "[SOFA-SCORE] " + Fore.WHITE + "A {} rivals del jugador {} ({}) els falta l'ID de SofaScore.".format(error['count'], error['player'], error['ranking']))

if __name__ == '__main__':
    getMissingPlayers()