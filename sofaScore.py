# -*- coding: utf-8 -*-
import time
from random import seed
from random import randint
import requests
import json
from utils import *

BASE_URL = "https://api.sofascore.com/api/v1/"
HEADERS = {
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "sec-ch-ua-platform": "\"Windows\"",
    "accept": "*/*",
    "origin": "https://www.sofascore.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.sofascore.com/",
    #    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

def getJSONFromURL(url):
    content = requests.request("GET", url, data = "", headers = HEADERS).text
    #print(content)

    try:
        jsonContent = json.loads(content)
        return jsonContent
    except:
        return False

def getPlayers(fromID = 1, toID = None):
    seed(1)
    currentID = fromID

    while currentID <= toID:
        print("# Analyzing the team with ID {}...".format(currentID))
        url = "{}{}".format(BASE_URL, currentID)
        dataJSON = getJSONFromURL(url)
        
        if dataJSON:
            print("PLAYER!!!")

            if not "error" in dataJSON and "team" in dataJSON and dataJSON['team']['category']['sport']['id'] == 5:
                print(dataJSON)

        currentID += 1
        secondsToWait = randint(10, 15)
        time.sleep(secondsToWait)

def checkBreaksUndefinedGamesByPlayer(playerID, lastGames):
    breakData = {'definedGames': lastGames['definedGames'], 'games': []}

    for indexGame, game in enumerate(lastGames['games']):
        if "opponent" in game and (game['breakDone'] == -1 or game['breakReceived'] == -1):
            url = "{}{}{}".format(BASE_URL, "sport/tennis/scheduled-events/", game['date'])
            print(url)
            dataJSON = getJSONFromURL(url)
            
            for dailyGame in dataJSON['events']:
                homePlayer = dailyGame['homeTeam']['id']
                awayPlayer = dailyGame['awayTeam']['id']
                
                if homePlayer == playerID and awayPlayer == game['opponent'] or homePlayer == game['opponent'] and awayPlayer == playerID:
                    urlGame = "{}{}{}".format(BASE_URL, "event/", dailyGame['id'])
                    print(urlGame)
                    gameJSON = getJSONFromURL(urlGame)

                    if "period1" in gameJSON['event']['homeScore']:
                        wonGamesHome = gameJSON['event']['homeScore']['period1']
                        wonGamesAway = gameJSON['event']['awayScore']['period1']

                        if abs(wonGamesHome - wonGamesAway) > 1 and max(wonGamesHome, wonGamesAway) > 5 or max(wonGamesHome, wonGamesAway) == 7:
                            setFinished = True
                        else:
                            setFinished = False

                        urlStats = "{}{}{}{}".format(BASE_URL, "event/", dailyGame['id'], "/statistics")
                        print(urlStats)
                        statsJSON = getJSONFromURL(urlStats)
                        
                        if "statistics" in statsJSON:
                            for phase in statsJSON['statistics']:
                                if phase['period'] == "1ST":
                                    for group in phase['groups']:
                                        if group['groupName'] == "Return":
                                            for item in group['statisticsItems']:
                                                if item['name'] == "Break points converted":
                                                    breakItem = {'index': indexGame}

                                                    if not setFinished and (int(item['home']) == 0 or int(item['away']) == 0):
                                                        # Player retired during the 1st set without break for both players
                                                        breakItem['toDelete'] = True
                                                    else:
                                                        if homePlayer == playerID:
                                                            breakItem['breakDone'] = int(item['home']) > 0 and 1 or 0
                                                            breakItem['breakReceived'] = int(item['away']) > 0 and 1 or 0
                                                        else:
                                                            breakItem['breakDone'] = int(item['away']) > 0 and 1 or 0
                                                            breakItem['breakReceived'] = int(item['home']) > 0 and 1 or 0
                                                        
                                                        breakData['definedGames'] += 1

                                                    breakData['games'].append(breakItem)
                    else:
                        # El matx s'ha d'eliminar
                        x = 1

                    break

    return breakData