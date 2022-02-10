# -*- coding: utf-8 -*-
from datetime import date
import re
import requests
import ast
import click
import Levenshtein as lev
from colorama import init, Back, Fore, Style
from credentials import *
from utils import *
from models import db, objects

def matchNames(gamesBet365, gameDB):
    maxRatio = 0
    indexMaxRatio = -1

    for indexGame, gameBet365 in enumerate(gamesBet365):
        homeName = gameBet365['home']['name']
        awayName = gameBet365['away']['name']
        player1FS = gameDB['FS-player1'].split(" ")
        player1TE = gameDB['TE-player1'].split(" ")
        player2FS = gameDB['FS-player2'].split(" ")
        player2TE = gameDB['TE-player2'].split(" ")
        player1Found = True
        player2Found = True

        # Exact string
        for namePart in player1FS:
            if namePart not in homeName and namePart not in awayName:
                player1Found = False
                break

        if not player1Found:
            player1Found = True

            for namePart in player1TE:
                if namePart not in homeName and namePart not in awayName:
                    player1Found = False
                    break

        if player1Found:
            for namePart in player2FS:
                if namePart not in homeName and namePart not in awayName:
                    player2Found = False
                    break

            if not player2Found:
                player2Found = True

                for namePart in player2TE:
                    if namePart not in homeName and namePart not in awayName:
                        player2Found = False
                        break

        if player1Found and player2Found:
            print("Max. ratio: 100%!!")
            return indexGame
        else:
            ratio = getGameRatio(gameBet365, gameDB)

            if ratio > maxRatio:
                maxRatio = ratio
                indexMaxRatio = indexGame
    
    print("Max. ratio: {}".format(maxRatio))
    if maxRatio > 0.7:
        return indexMaxRatio
    else:
        return -1

def getGameRatio(gameBet365, gameDB):
    player1FSRatio1 = getPlayerRatio(gameBet365['home']['name'], gameDB['FS-player1'])
    player1TERatio1 = getPlayerRatio(gameBet365['home']['name'], gameDB['TE-player1'])
    player1FSRatio2 = getPlayerRatio(gameBet365['away']['name'], gameDB['FS-player1'])
    player1TERatio2 = getPlayerRatio(gameBet365['away']['name'], gameDB['TE-player1'])
    player2FSRatio1 = getPlayerRatio(gameBet365['away']['name'], gameDB['FS-player2'])
    player2TERatio1 = getPlayerRatio(gameBet365['away']['name'], gameDB['TE-player2'])
    player2FSRatio2 = getPlayerRatio(gameBet365['home']['name'], gameDB['FS-player2'])
    player2TERatio2 = getPlayerRatio(gameBet365['home']['name'], gameDB['TE-player2'])
    player1Ratios = [player1FSRatio1, player1TERatio1, player1FSRatio2, player1TERatio2]
    player2Ratios = [player2FSRatio1, player2TERatio1, player2FSRatio2, player2TERatio2]
    player1Ratio = max(player1Ratios)
    player2Ratio = max(player2Ratios)
    return (player1Ratio + player2Ratio) / 2

def getPlayerRatio(name1, name2):
    name1Parts = re.split(' |-', name1)
    name2Parts = re.split(' |-', name2)
    numParts = len(name1Parts)
    totalRatios = 0.0

    for name1Part in name1Parts:
        name1Part = str(name1Part)
        maxRatio = 0.0

        for name2Part in name2Parts:
            name2Part = str(name2Part)

            if lev.ratio(name1Part, name2Part) > maxRatio:
                maxRatio = lev.ratio(name1Part, name2Part)

        totalRatios += maxRatio

    ratioAvg = totalRatios / numParts
    return ratioAvg

init(autoreset = True)
@click.command()
@click.option(
    '-d', '--games-day',
    help = "Game date to check", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)

def checkOdds(games_day):
    url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"
    headers = {
        'x-rapidapi-host': "betsapi2.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY,
    }
    gamesBet365 = []
    page = 1
    end = False

    while not end:
        querystring = {"sport_id":"13", "page":page}
        response = requests.request("GET", url, headers = headers, params = querystring)
        data = response.json()
        
        if "results" in data:
            if len(data['results']) > 0:
                page += 1
                gamesBet365 += data['results']
            else:
                end = True
        else:
            print("⚠️  Hourly plan has been exceeded!")
            exit()
    
    '''for gameBet365 in gamesBet365:
        print("{} vs {}".format(gameBet365['home']['name'], gameBet365['away']['name']))
    exit()'''
    '''print(len(gamesBet365))
    exit()'''
    '''print(gamesBet365)
    exit()'''
    '''printCollection(gamesBet365)
    exit()'''

    dbConnection = db.Database()
    breaksDB = dbConnection.connect()
    gamesObj = objects.Games(breaksDB)
    gamesDB = gamesObj.find_all([{'gameDay': games_day, 'profitable': True}])

    for gameDB in gamesDB:
        print(Back.CYAN + Fore.BLACK + " {} vs {} ".format(gameDB['FS-player1'], gameDB['FS-player2']))
        indexGameBet365 = matchNames(gamesBet365, gameDB)
        print(Fore.YELLOW + "Bet365 Game => {} vs {}".format(gamesBet365[indexGameBet365]['home']['name'], gamesBet365[indexGameBet365]['away']['name']))
        print(Fore.GREEN + Style.BRIGHT + "Bet365 Index: {}".format(indexGameBet365))

        if indexGameBet365 > -1:
            player1Ratio1 = getPlayerRatio(gameDB['FS-player1'], gamesBet365[indexGameBet365]['home']['name'])
            player1Ratio2 = getPlayerRatio(gameDB['TE-player1'], gamesBet365[indexGameBet365]['home']['name'])
            player1Ratio3 = getPlayerRatio(gameDB['FS-player1'], gamesBet365[indexGameBet365]['away']['name'])
            player1Ratio4 = getPlayerRatio(gameDB['TE-player1'], gamesBet365[indexGameBet365]['away']['name'])
            player1Ratios = [player1Ratio1, player1Ratio2, player1Ratio3, player1Ratio4]
            maxPlayer1Ratio = max(player1Ratios)

            if maxPlayer1Ratio == player1Ratio1 or maxPlayer1Ratio == player1Ratio2:
                playerIndex = 0
            elif maxPlayer1Ratio == player1Ratio3 or maxPlayer1Ratio == player1Ratio4:
                playerIndex = 1
            else:
                print("❌ There has been an error with the player {}.".format(gameDB['FS-player1']))
                exit()

            url = "https://betsapi2.p.rapidapi.com/v3/bet365/prematch"
            querystring = {"FI":gamesBet365[indexGameBet365]['id']}
            response = requests.request("GET", url, headers = headers, params = querystring)
            markets = ast.literal_eval(response.text)

            if "results" in markets:
                if "others" in markets['results'][0]:
                    for othersContent in markets['results'][0]['others']:
                        if "first_set_player_to_break_serve" in othersContent['sp']:
                            breakOdd = othersContent['sp']['first_set_player_to_break_serve']['odds'][playerIndex]['odds']
                            print(Fore.WHITE + Style.BRIGHT + "Break Odd: {}".format(breakOdd))
            else:
                print("⚠️  Hourly plan has been exceeded!")
                exit()

if __name__ == '__main__':
    checkOdds()