from datetime import date
import requests
import ast
import click
import Levenshtein as lev
from credentials import *
from utils import *
from models import db, objects

def matchNames(gamesBet365, gameDB):
    maxRatio = 0
    indexMaxRatio = -1

    for indexGame, gameBet365 in enumerate(gamesBet365):
        homeName = gameBet365['home']['name']
        awayName = gameBet365['away']['name']
        #print("{} vs {}".format(homeName, awayName))
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
            return indexGame
        else:
            ratio = getGameRatio(gameBet365, gameDB)

            if ratio > maxRatio:
                maxRatio = ratio
                indexMaxRatio = indexGame
    
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
    player1Ratio = max(player1FSRatio1, player1TERatio1, player1FSRatio2, player1TERatio2)
    player2Ratio = max(player2FSRatio1, player2TERatio1, player2FSRatio2, player2TERatio2)
    return (player1Ratio + player2Ratio) / 2

def getPlayerRatio(name1, name2):
    name1Parts = name1.split(" ")
    name2Parts = name2.split(" ")
    numParts = len(name1Parts)
    totalRatios = 0.0

    for name1Part in name1Parts:
        maxRatio = 0.0

        for name2Part in name2Parts:
            if lev.ratio(name1Part, name2Part) > maxRatio:
                maxRatio = lev.ratio(name1Part, name2Part)

        totalRatios += maxRatio

    ratioAvg = totalRatios / numParts
    return ratioAvg

@click.command()
@click.option(
    '-d', '--games-day',
    help = "Game date to check", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)

def checkOdds(games_day):
    url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"
    querystring = {"sport_id":"13"}
    headers = {
        'x-rapidapi-host': "betsapi2.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers = headers, params = querystring)
    data = response.json()
    gamesBet365 = data['results']
    '''printCollection(gamesBet365)
    exit()'''

    dbConnection = db.Database()
    breaksDB = dbConnection.connect()
    gamesObj = objects.Games(breaksDB)
    gamesDB = gamesObj.find_all([{'gameDay': games_day, 'profitable': True}])

    for gameDB in gamesDB:
        indexGameBet365 = matchNames(gamesBet365, gameDB)
        print(gameDB)
        print(indexGameBet365)

    exit()

    for fixture in data['results']:
        print(".:: {} vs {} ::.\n".format(fixture['home']['name'], fixture['away']['name']))
        url = "https://betsapi2.p.rapidapi.com/v3/bet365/prematch"
        querystring = {"FI":fixture['id']}
        headers = {
            'x-rapidapi-host': "betsapi2.p.rapidapi.com",
            'x-rapidapi-key': RAPIDAPI_KEY
            }
        response = requests.request("GET", url, headers = headers, params = querystring)
        markets = ast.literal_eval(response.text)

        for othersContent in markets['results'][0]['others']:
            if "first_set_player_to_break_serve" in othersContent['sp']:
                printCollection(othersContent['sp']['first_set_player_to_break_serve'])

if __name__ == '__main__':
    checkOdds()