# -*- coding: utf-8 -*-
from __future__ import division
from datetime import date
from math import ceil, floor
import click
from colorama import init, Back, Fore
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
gamesObj = objects.Games(breaksDB)
playersObj = objects.Players(breaksDB)
init(autoreset = True)

@click.command()
@click.option(
    '-d', '--games-day',
    help = "Game date to print", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)

def printDailyGames(games_day):
    games = gamesObj.find_all([{'gameDay': games_day}])

    for game in games:
        numSpacesBefore1 = int(ceil((58 - len(game['FS-player1'])) / 2))
        numSpacesAfter1 = int(floor((58 - len(game['FS-player1'])) / 2))
        numSpacesBefore2 = int(ceil((62 - len(game['FS-player2'])) / 2))
        numSpacesAfter2 = int(floor((62 - len(game['FS-player2'])) / 2))
        print("\n" + Back.BLUE + " " * numSpacesBefore1 + game['FS-player1'] + " " * numSpacesAfter1 + "|" + " " * numSpacesBefore2 + game['FS-player2'] + " " * numSpacesAfter2)
        print(Back.CYAN + Fore.BLACK +  " Date" + " " * 9 + "Opponent" + " " * 25 + "Break Done | Date" + " " * 9 + "Opponent" + " " * 25 + "Break Received ")
        player = playersObj.read(game['player1ID'])
        opponent = playersObj.read(game['player2ID'])

        for indexGame, playerGame in enumerate(player['lastGames']):
            opponent1Name = playersObj.read(playerGame['opponent'])['flashScoreName']
            numSpacesAfterPlayer1 = 37 - len(opponent1Name)
            opponentGame = opponent['lastGames'][indexGame]
            opponent2Name = playersObj.read(opponentGame['opponent'])['flashScoreName']
            numSpacesAfterPlayer2 = 39 - len(opponent2Name)

            if playerGame['breakDone'] == 1:
                breakDoneChar = "Y"
            elif playerGame['breakDone'] == 0:
                breakDoneChar = "N"
            else:
                breakDoneChar = "?"

            if opponentGame['breakReceived'] == 1:
                breakReceivedChar = "Y"
            elif opponentGame['breakReceived'] == 0:
                breakReceivedChar = "N"
            else:
                breakReceivedChar = "?"

            print(" {}   {}".format(playerGame['time'], opponent1Name) + " " * numSpacesAfterPlayer1 + breakDoneChar + " " * 6 + "| {}   {}".format(opponentGame['time'], opponent2Name) + " " * numSpacesAfterPlayer2 + breakReceivedChar)
        
        if game['profitable']:
            bgColor = Back.GREEN
        else:
            bgColor = Back.MAGENTA

        print(bgColor + Fore.BLACK + " TOTAL" + " " * 8 + "{}/{}".format(game['playerData']['totalBreaksDone'], game['playerData']['definedGames']) + " " * 33 + "{}%".format(game['playerData']['probability']) + " " * 5 + "| TOTAL" + " " * 8 + "{}/{}".format(game['opponentData']['totalBreaksReceived'], game['opponentData']['definedGames']) + " " * 35 + "{}%".format(game['opponentData']['probability']) + " " * 7)
    
    print()

if __name__ == '__main__':
    printDailyGames()