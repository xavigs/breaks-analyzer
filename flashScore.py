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
PLAYER1_NAME = "CX"
LIVE = "AI"
HAS_STATS = "AO"
HOME3CHARNAME = "WM"
AWAY3CHARNAME = "WN"
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
SURFACES = {"dura": "D",
            "dura (indoor)": "I",
            "arcilla": "T",
            "hierba": "H",
            "arcilla (indoor)": "T"}

def getDailyGames(day):
    # Load FlashScore WS with daily matches
    if day == "today":
        url = "https://d.flashscore.es/x/feed/f_2_0_1_es_1"
    else:
        url = "https://d.flashscore.es/x/feed/f_2_1_1_es_1"

    # cURL to access to unauthorized page
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

    return parseGames(data.getvalue().decode('UTF-8'), True)

def getPrecedents(idGame, homeKeyword, awayKeyword):
    #url = "https://www.flashscore.es/partido/" + str(idGame) + "/#resumen-del-partido"
    url = "https://www.flashscore.es/partido/848gxv3a/#resumen-del-partido"
    print(url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    scripts = soup.select("script")

    for script in scripts:
        scriptContent = str(script.string).strip()

        if "window.environment" in scriptContent:
            jsonString = scriptContent.replace("window.environment = ", "")
            jsonString = lreplace(";", "", jsonString)
            jsonGame = json.loads(jsonString)
            print(jsonGame['participantsData'])
    exit()

def parseGames(content, future, playerKeyword = None):
    games = []
    tournament = ""
    rows = content.split(JS_ROW_END)
    #i = 0 # To delete

    for row in rows:
        row = row.split(JS_CELL_END)
        #rows[i] = row # To delete
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
                        elif keyFlashScore == SHAREDINDEXES_EVENT_STAGE_ID:
                            if future and int(itemValue) > 1 or not future and int(itemValue) == 1:
                                # Finished game or being played: destroy the game variable
                                del game
                        elif keyFlashScore == PLAYER1_NAME:
                            if "game" in locals():
                                playerName = itemValue.split(" (")
                                game['player1'] = playerName[0]
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
                        elif keyFlashScore == SHAREDINDEXES_EVENT_STAGE_TYPE_ID:
                            # TODO: Implementation has to be understood
                            x = 1
                    else:
                        if "game" in locals():
                            games.append(game)

        #i += 1 # To delete

    if future:
        games = sorted(games, key = lambda k: k['utime'])
    else:
        # TODO: Array slice to get 8 games
        x = 1

    #printCollection(rows)
    #printCollection(games)
    #print(json.dumps(games, sort_keys=False, indent=4))
    return games
