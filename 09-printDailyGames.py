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
@click.option(
    '-s', '--sex',
    help = "Sex category to print", type = str, default = None, show_default = True
)

def printDailyGames(games_day, sex):
    if sex is None:
        games = gamesObj.find_all([{'gameDay': games_day}])
    else:
        games = gamesObj.find_all([{'gameDay': games_day}, {'sex': sex}])

    for game in games:
        if game['profitable']:
            numSpacesBefore1 = int(ceil((58 - len(game['FS-player1'])) / 2))
            numSpacesAfter1 = int(floor((58 - len(game['FS-player1'])) / 2))
            numSpacesBefore2 = int(ceil((62 - len(game['FS-player2'])) / 2))
            numSpacesAfter2 = int(floor((62 - len(game['FS-player2'])) / 2))
            print("\n" + Back.BLUE + " " * numSpacesBefore1 + game['FS-player1'] + " " * numSpacesAfter1 + "|" + " " * numSpacesBefore2 + game['FS-player2'] + " " * numSpacesAfter2)
            print(Back.CYAN + Fore.BLACK +  " Date" + " " * 9 + "Opponent" + " " * 25 + "Break Done | Date" + " " * 9 + "Opponent" + " " * 25 + "Break Received ")
            player = playersObj.read(game['player1ID'])
            opponent = playersObj.read(game['player2ID'])

            for indexGame in range(0, 8):
                if len(player['lastGames']) > indexGame:
                    playerGame = player['lastGames'][indexGame]
                    opponentDB = playersObj.read(playerGame['opponent'])

                    if opponentDB is None:
                        print("❌ The opponent {} is not into the database.".format(playerGame['opponent']))
                        exit()
                    else:
                        opponentName = opponentDB['tennisExplorerName']
                        numSpacesAfterPlayer1 = 37 - len(opponentName)

                        if not "breakDone" in playerGame:
                            breakDoneChar = "?"
                        else:
                            if playerGame['breakDone'] == 1:
                                breakDoneChar = "Y"
                            elif playerGame['breakDone'] == 0:
                                breakDoneChar = "N"
                            else:
                                breakDoneChar = "?"

                    print " {}   {}".format(playerGame['time'], opponentName) + " " * numSpacesAfterPlayer1 + breakDoneChar + " " * 6 + "|",
                else:
                    print(" " * 50)

                if len(opponent['lastGames']) > indexGame:
                    playerGame = opponent['lastGames'][indexGame]
                    opponentDB = playersObj.read(playerGame['opponent'])

                    if opponentDB is None:
                        print("❌ The opponent {} is not into the database.".format(playerGame['opponent']))
                        exit()
                    else:
                        opponentName = opponentDB['tennisExplorerName']
                        numSpacesAfterPlayer1 = 37 - len(opponentName)
                        
                        if not "breakReceived" in playerGame:
                            breakReceivedChar = "?"
                        else:
                            if playerGame['breakReceived'] == 1:
                                breakReceivedChar = "Y"
                            elif playerGame['breakReceived'] == 0:
                                breakReceivedChar = "N"
                            else:
                                breakReceivedChar = "?"

                    print("{}   {}".format(playerGame['time'], opponentName) + " " * numSpacesAfterPlayer1 + breakReceivedChar)
                else:
                    print(" " * 50)
            
            if game['profitable']:
                bgColor = Back.GREEN
            else:
                bgColor = Back.MAGENTA

            print(bgColor + Fore.BLACK + " TOTAL" + " " * 8 + "{}/{}".format(game['playerData']['totalBreaksDone'], game['playerData']['totalGames']) + " " * 33 + "{}%".format(game['playerData']['probability']) + " " * 5 + "| TOTAL" + " " * 8 + "{}/{}".format(game['opponentData']['totalBreaksReceived'], game['opponentData']['totalGames']) + " " * 35 + "{}%".format(game['opponentData']['probability']) + " " * 7)
    
    print("")

if __name__ == '__main__':
    printDailyGames()