# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO
import certifi
from utils import *
from datetime import datetime
import json
import re

JS_ROW_END = "~"
JS_CELL_END = "¬"
JS_INDEX = "÷"
SHAREDINDEXES_SPORT_ID = "SA"
DCAPIPARTICIPANTINDEXES_TEAM_INFO = "PR"
DCAPIPARTICIPANTINDEXES_TEAM_INFO_DELETED = "PRD"
SHAREDINDEXES_TOURNAMENT_NAME = "ZA"
SHAREDINDEXES_EVENT_ID = "AA"
SHAREDINDEXES_MATCH_START_UTIME = "AD"
SHAREDINDEXES_EVENT_STAGE_TYPE_ID = "AB"
SHAREDINDEXES_EVENT_STAGE_ID = "AC"
PLAYER1_ID = "PX"
PLAYER1_NAME = "CX"
LIVE = "AI"
HAS_STATS = "AO"
HOME3CHARNAME = "WM"
AWAY3CHARNAME = "WN"
PLAYER2_ID = "PY"
PLAYER2_NAME = "AF"
HOME_ENCODED_PARTICIPANT_ID = "JA"
AWAY_ENCODED_PARTICIPANT_ID = "JB"
HOME_KEYWORD = "WU"
AWAY_KEYWORD = "WV"
FULLFEEDINDEXES_MOVED_EVENTS_ID = "QA"
SHAREDINDEXES_FEED_SIGNATURE = "A1"
SPORT_SCORE_PART_LIST = 5
SHAREDINDEXES_HOME_RESULT_PERIOD_1 = "BA"
SHAREDINDEXES_HOME_RESULT_PERIOD_2 = "BC"
SHAREDINDEXES_HOME_RESULT_PERIOD_3 = "BE"
SHAREDINDEXES_HOME_RESULT_PERIOD_4 = "BG"
SHAREDINDEXES_HOME_RESULT_PERIOD_5 = "BI"
SHAREDINDEXES_AWAY_RESULT_PERIOD_1 = "BB"
SHAREDINDEXES_AWAY_RESULT_PERIOD_2 = "BD"
SHAREDINDEXES_AWAY_RESULT_PERIOD_3 = "BF"
SHAREDINDEXES_AWAY_RESULT_PERIOD_4 = "BH"
SHAREDINDEXES_AWAY_RESULT_PERIOD_5 = "BJ"
STATS_SET = "HA"
STATS_CATEGORY = "SF"
STATS_PARAMETER = "SG"
STATS_HOME = "SH"
STATS_AWAY = "SI"
POINTS_DETAIL = "HL"
STATS_ENDGAME = "A1"
RANKING_REGISTER = "TS"
RANKING_PLAYER = "RW"
RANKING_PLAYER_TAG = "PT"
RANKING_PLAYER_VALUE = "PV"
RANKING_PLAYER_NAME = "PN"
RANKING_PLAYER_ID = "PI"
RANKING_POSITION = "RA"
SURFACES = {"hard": "D",
            "hard (indoor)": "I",
            "clay": "T",
            "grass": "H",
            "clay (indoor)": "T"}

def getUnauthorizedContent(url):
    data = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(crl.HEADER, 0)
    crl.setopt(crl.TIMEOUT, 30)
    crl.setopt(crl.HTTPHEADER, ["x-fsign: SW9D1eZo"])
    crl.setopt(crl.WRITEFUNCTION, data.write)
    crl.setopt(crl.CAINFO, certifi.where())
    crl.perform()
    crl.close()

    return data.getvalue()

def getDailyGames(day):
    # Load FlashScore WS with daily matches
    if day == "today":
        url = "https://d.flashscore.es/x/feed/f_2_0_1_es_1"
    elif day == "tomorrow":
        url = "https://d.flashscore.es/x/feed/f_2_1_1_es_1"
    elif day == "test":
        url = "https://d.flashscore.es/x/feed/f_2_-1_1_es_1"

    return parseGames(getUnauthorizedContent(url), True)

def getPreviousGames(idGame, homeKeyword, awayKeyword):
    games = {}
    url = "https://www.flashscore.es/partido/" + str(idGame) + "/#resumen-del-partido"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    scripts = soup.select("script")

    for script in scripts:
        scriptString = script.string

        if scriptString is not None:
            scriptContent = str(scriptString.encode('utf-8')).strip()

            if "window.environment" in scriptContent:
                jsonString = scriptContent.replace("window.environment = ", "")
                jsonString = lreplace(";", "", jsonString)
                jsonGame = json.loads(jsonString)
                idHomePlayer = jsonGame['participantsData']['home'][0]['id']
                idAwayPlayer = jsonGame['participantsData']['away'][0]['id']

                # Home player
                url = "https://www.flashscore.es/jugador/" + homeKeyword + "/" + idHomePlayer + "/resultados"
                r = requests.get(url)
                data = r.text
                soup = BeautifulSoup(data, "lxml")
                data = soup.select("div#participant-page-data-results_s")[0].text
                games['home'] = parseGames(data.encode('utf-8'), False)
                
                # Away player
                url = "https://www.flashscore.es/jugador/" + awayKeyword + "/" + idAwayPlayer + "/resultados"
                r = requests.get(url)
                data = r.text
                soup = BeautifulSoup(data, "lxml")
                data = soup.select("div#participant-page-data-results_s")[0].text
                games['away'] = parseGames(data.encode('utf-8'), False)

                return games

def parseGames(content, future, playerKeyword = None, lastGames = None):
    games = []
    tournament = ""
    rows = content.split(JS_ROW_END)

    for row in rows:
        row = row.split(JS_CELL_END)
        index = row[0].split(JS_INDEX)
        indexName = ""
        indexValue = ""

        if len(index) > 0 and index[0] != "":
            indexName = index[0]

        if len(index) > 1 and index[1] != "":
            indexValue = index[1]

        if indexName == SHAREDINDEXES_TOURNAMENT_NAME:
            if "EXHIBICIÓN" not in indexValue and "DOBLES" not in indexValue and "JÚNIOR" not in indexValue:
                categoryTournament = indexValue.split(" - ")
                tournamentName = categoryTournament[1].split(":")
                tournamentNameParts = tournamentName[1].split(", ")

                if categoryTournament[0] == "ATP":
                    sex = "Masc."
                    category = "ATP"
                elif categoryTournament[0] == "CHALLENGER MASCULINO":
                    sex = "Masc."
                    category = "Challenger"
                elif categoryTournament[0] == "ITF MASCULINO":
                    sex = "Masc."
                    category = "ITF"
                elif categoryTournament[0] == "WTA":
                    sex = "Fem."
                    category = "WTA"
                elif categoryTournament[0] == "CHALLENGER FEMENINO":
                    sex = "Fem."
                    category = "Challenger"
                elif categoryTournament[0] == "ITF FEMENINO":
                    sex = "Fem."
                    category = "ITF"

                tournament = tournamentNameParts[0].strip()

                if len(tournamentNameParts) > 1:
                    surface = tournamentNameParts[1]
                else:
                    surface = "?"
            else:
                tournament = ""
        elif indexName == SHAREDINDEXES_EVENT_ID:
            if tournament != "":
                game = {}
                game['id'] = indexValue
                game['category'] = category
                game['sex'] = sex
                game['tournament'] = tournament

                if surface != "?":
                    game['surface'] = SURFACES[surface]
                else:
                    game['surface'] = surface

                for item in row:
                    if item != "":
                        keyFlashScore, itemValue = item.split(JS_INDEX)

                        if keyFlashScore == SHAREDINDEXES_MATCH_START_UTIME:
                            game['utime'] = int(itemValue)
                            game['date'] = datetime.fromtimestamp(game['utime']).strftime("%Y-%m-%d")
                            game['time'] = datetime.fromtimestamp(game['utime']).strftime("%H:%M")
                        elif keyFlashScore == SHAREDINDEXES_EVENT_STAGE_TYPE_ID:
                            if future and int(itemValue) > 1 or not future and int(itemValue) == 1:
                                # Finished game or being played: destroy the game variable
                                del game
                        elif keyFlashScore == SHAREDINDEXES_EVENT_STAGE_ID:
                            if "game" in locals() and itemValue == 9:
                                del game
                        elif keyFlashScore == PLAYER1_ID:
                            if "game" in locals():
                                game['player1ID'] = itemValue
                        elif keyFlashScore == PLAYER1_NAME:
                            if "game" in locals():
                                playerName = itemValue.split(" (")
                                game['player1'] = playerName[0]
                        elif keyFlashScore == PLAYER2_ID:
                            if "game" in locals():
                                game['player2ID'] = itemValue
                        elif keyFlashScore == PLAYER2_NAME:
                            if "game" in locals():
                                playerName = itemValue.split(" (")
                                game['player2'] = playerName[0]
                        elif keyFlashScore == HOME_KEYWORD:
                            if "game" in locals():
                                game['keyword1'] = itemValue

                                if not future and game['keyword1'] == playerKeyword:
                                    game['player'] = 1
                        elif keyFlashScore == AWAY_KEYWORD:
                            if "game" in locals():
                                game['keyword2'] = itemValue

                                if not future and game['keyword2'] == playerKeyword:
                                    game['player'] = 2
                    else:
                        if "game" in locals():
                            games.append(game)

    if future:
        games = sorted(games, key = lambda k: k['utime'])
    else:
        newLastGames = []
        itemsFound = 0

        for game in games:
            found = -1

            for index, previousGame in enumerate(lastGames):
                if game['date'] == previousGame['date'] and (game['player1ID'] == previousGame['opponent'] or game['player2ID'] == previousGame['opponent']):
                    found = index
                    itemsFound += 1
                    break
            
            newLastGame = {'index': index}

            if found > -1:
                newLastGame['game'] = game
            else:
                newLastGame['game'] = False
            
            newLastGames.append(newLastGame)
            
            if itemsFound == 8:
                break
        
        return newLastGames

    #printCollection(rows)
    #printCollection(games)
    #print(json.dumps(games, sort_keys=False, indent=4))
    return games

def parseStats(content):
    homeBreaks = 0
    awayBreaks = 0
    rows = content.split(JS_ROW_END)
    
    for row in rows:
        row = row.split(JS_CELL_END)
        index = row[0].split(JS_INDEX)
        indexName = ""
        indexValue = ""

        if len(index) > 0 and index[0] != "":
            indexName = index[0]

        if len(index) > 1 and index[1] != "":
            indexValue = index[1]
        
        if indexName != "" and indexValue != "":
            if indexName == STATS_SET:
                if indexValue == "Set 1":
                    stats = {}
                elif "stats" in locals():
                    stats['homeBreaks'] = homeBreaks
                    stats['awayBreaks'] = awayBreaks
                    return stats
            elif "stats" in locals():
                indexGame = 0

                for item in row:
                    if item != "":
                        keyFS, itemValue = item.split(JS_INDEX)

                        if keyFS == POINTS_DETAIL and indexGame == 5:
                            if row[4][-1] == "1":
                                homeBreaks += 1
                            else:
                                awayBreaks += 1
                    
                    indexGame += 1

        elif indexName == STATS_ENDGAME and "stats" in locals():
            stats['homeBreaks'] = homeBreaks
            stats['awayBreaks'] = awayBreaks
            return stats

    exit()

def getBreakData(game):
    url = "https://d.flashscore.com/x/feed/df_mh_1_" + game['id']
    h = {
        'Host':'d.flashscore.com',
        'User-Agent':'core',
        'Accept':'*/*',
        'Accept-Language':'*',
        'Accept-Encoding':'gzip,deflate,br',
        'Referer':'https://d.flashscore.com/x/feed/proxy-local',
        'X-GeoIP':'1',
        'X-Referer':'https://www.flashscore.com/tennis/',
        'X-Fsign':'SW9D1eZo',
        'X-Requested-With':'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cookie':'_ga=GA1.2.149667040.1559363495; _gid=GA1.2.1231578565.1559363495; _sessionhits_UA-207011-5=2; _gat_UA-207011-5=1; _session_UA-207011-5=true',
        'TE':'Trailers'
    }
    r = requests.get(url, headers = h)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    #content = getUnauthorizedContent(url)
    content = soup.select("p")[0].text
    return parseStats(content)

def getRanking(category):
    fullranking = []
    url = "https://www.flashscore.com/tennis/rankings/" + category + "/"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    scripts = soup.select("script")

    for script in scripts:
        scriptString = script.string

        if scriptString is not None:
            scriptContent = str(scriptString.encode('utf-8')).strip()

            if "_cjs.rankingId" in scriptContent:
                rankingIdTextPos = scriptContent.index("_cjs.rankingId")
                rankingId = scriptContent[(rankingIdTextPos + 18):(rankingIdTextPos + 26)]

                for page in range(1, 3):
                    rankingURL = "https://d.flashscore.com/x/feed/ran_" + rankingId + "_" + str(page)
                    ranking = parseRanking(getUnauthorizedContent(rankingURL))
                    fullranking += ranking

                return fullranking

def parseRanking(content):
    players = []
    typeValue = None
    rows = content.split(JS_ROW_END)
    validFields = (RANKING_PLAYER_NAME, RANKING_PLAYER_ID, RANKING_POSITION)
    
    for row in rows:
        row = row.split(JS_CELL_END)
        
        for cell in row:
            if JS_INDEX in cell:
                indexName, indexValue = cell.split(JS_INDEX)
                
                if indexName == RANKING_REGISTER and indexValue == RANKING_PLAYER:
                    player = {}
                elif indexName == RANKING_PLAYER_TAG and indexValue == RANKING_PLAYER_NAME:
                    typeValue = "name"
                elif indexName == RANKING_PLAYER_VALUE and typeValue == "name":
                    player['flashScoreName'] = indexValue
                elif indexName == RANKING_PLAYER_TAG and indexValue == RANKING_PLAYER_ID:
                    typeValue = "id"
                elif indexName == RANKING_PLAYER_VALUE and typeValue == "id":
                    player['flashScoreId'] = indexValue
                elif indexName == RANKING_PLAYER_TAG and indexValue == RANKING_POSITION:
                    typeValue = "ranking"
                elif indexName == RANKING_PLAYER_VALUE and typeValue == "ranking":
                    player['ranking'] = int(indexValue)
                    players.append(player)
                    typeValue = None
                elif indexName == RANKING_PLAYER_TAG not in validFields:
                    typeValue = None

    return players

def checkBreaksLastGamesByPlayer(playerID, playerName, lastGames):
    lastGamesBreakData = {}
    lastGamesBreakData['games'] = []
    definedGames = 0
    playerKeyword = getKeywordFromString(playerName)
    url = "https://www.flashscore.com/player/" + playerKeyword + "/" + playerID + "/results"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    data = soup.select("div#participant-page-data-results_s")[0].text
    games = parseGames(data.encode('utf-8'), False, lastGames = lastGames)
    
    for index, event in enumerate(games):
        if event['game']:
            gameBreakData = {}
            playerLocation = event['game']['player1ID'] == playerID and "home" or "away"
            opponentLocation = playerLocation == "home" and "away" or "home"
            breakData = getBreakData(event['game'])
            gameBreakData['index'] = index
            gameBreakData['breakDone'] = breakData[playerLocation + "Breaks"] > 0 and 1 or 0
            gameBreakData['breakReceived'] = breakData[opponentLocation + "Breaks"] > 0 and 1 or 0
            definedGames += 1
            lastGamesBreakData['games'].append(gameBreakData)

    lastGamesBreakData['definedGames'] = definedGames
    return lastGamesBreakData