import requests
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO
import certifi
from utils import *

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

    return parseGames(data.getvalue().decode('UTF-8'))

def parseGames(content):
    rows = content.split(JS_ROW_END)
    i = 0 # To delete

    for row in rows:
        row = row.split(JS_CELL_END)
        rows[i] = row # To delete
        '''indexName, indexValue = row[0].split(JS_INDEX)

        if indexName == SHAREDINDEXES_TOURNAMENT_NAME:
            if "EXHIBICIÓN" not in indexValue and "DOBLES" not in indexValue:
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
                print(tournament, surface)
        elif indexName == SHAREDINDEXES_EVENT_ID:
            print("Matx")'''

        i += 1 # To delete

    printCollection(rows)
    return ""
