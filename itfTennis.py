# -*- coding: utf-8 -*-
import sys
import time
import requests
import json
from utils import *

# Constants
SURFACES = {
    'H': 'D',
    'C': 'T',
    'I': 'I',
    'G': 'H',
    'A': 'M'
}

def getTournaments(sex, year):
    tournaments = []
    skip = 0

    # Get cookie from a random URL
    '''headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.8',
        'Cache-Control': 'max-age=0',
        'If-None-Match': '"d0a8a31d"',
        'Priority': "u=0, i",
        'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    randomURL = 'https://www.itftennis.com/en/tournament-calendar/mens-world-tennis-tour-calendar'
    session = requests.Session()
    session.get(randomURL, headers=headers)

    for cookie in session.cookies:
        if 'incap_ses_' in cookie.name:
            cookies = f'{cookie.name}={session.cookies[cookie.name]}'
    
    #headers = {'Cookie': cookies}'''
    headers = {'Cookie': 'incap_ses_1773_178373=TK0EJvDRjUVO4XvLUPaaGPo4jWcAAAAALtYaccy/3liKX7xDJBQPog=='}
    #print(headers)

    while skip < 700:
        url = "https://www.itftennis.com/tennis/api/TournamentApi/GetCalendar?circuitCode={}T&searchString=&skip={}&take=100&nationCodes=&zoneCodes=&dateFrom={}-01-01&dateTo={}-12-31&indoorOutdoor=&categories=&isOrderAscending=true&orderField=startDate&surfaceCodes=".format(sex, skip, year, year)
        content = requests.request('GET', url, data='', headers=headers).text
        #print(content)
        tournamentsData = json.loads(content)
        skip += 100

        for tournamentData in tournamentsData['items']:
            if tournamentData['surfaceCode'] == 'H' and tournamentData['indoorOrOutDoor'] == 'Indoor':
                tournamentData['surfaceCode'] = 'I'

            tournament = {
                '_id': tournamentData['tournamentKey'].lower(),
                'category': 'ITF',
                'name': tournamentData['tournamentName'],
                'country': getKeywordFromString(tournamentData['hostNation']).replace(",", "").replace(".", ""),
                'surface': SURFACES[tournamentData['surfaceCode']],
                'sex': sex,
                'year': year
            }
            tournaments.append(tournament)

    print(tournaments)
    return tournaments

def getDailyGames(day):
    games = []

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.9,ca;q=0.8',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'If-None-Match': '"0ebe71f6b4291ffd8b0b61f6e2f119ad96444eff"',
        'Origin': 'https://live.itftennis.com',
        'Priority': 'u=1, i',
        'Referer': 'https://live.itftennis.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = "https://api.itf-production.sports-data.stadion.io/custom/wttCompleteMatchList/{}".format(day)
    #url = 'https://ls.fn.sportradar.com/itf/en/Europe:Berlin/gismo/client_dayinfo/20241229'
    print(url)
    numRetries = 0
    tournamentsData = []

    while numRetries < 5:
        try:
            content = requests.request("GET", url, data = "", headers = headers).text
            tournamentsData = json.loads(content)['data']
            break
        except:
            time.sleep(2)
            numRetries += 1

    if len(tournamentsData) == 0:
        print("No hi siguis")
        sys.exit(1)

    for tournament, tournamentData  in tournamentsData.items():
        tournamentID = tournamentData['tennisId']
        '''if "Davis Cup" not in gameData['param5']:
            game = {
                'home': gameData['match']['teams']['home']['name'].replace(", ", " ").replace(",", " ").replace("  ", " "),
                'away': gameData['match']['teams']['away']['name'].replace(", ", " ").replace(",", " ").replace("  ", " "),
                'tournament': gameData['param4']
            }
            games.append(game)'''
        for courtName, courtData in tournamentData['courts'].items():
            for gameData in courtData:
                if len(gameData['sides']) == 2 and len(gameData['sides'][0]['sidePlayer']) > 0 and len(gameData['sides'][1]['sidePlayer']) > 0 and gameData['sides'][0]['sidePlayer'][0]['player']['person'] is not None and gameData['sides'][1]['sidePlayer'][0]['player']['person'] is not None:
                    game = {
                        'home': f"{gameData['sides'][0]['sidePlayer'][0]['player']['person']['lastName']} {gameData['sides'][0]['sidePlayer'][0]['player']['person']['firstName']}",
                        'away': f"{gameData['sides'][1]['sidePlayer'][0]['player']['person']['lastName']} {gameData['sides'][1]['sidePlayer'][0]['player']['person']['firstName']}",
                        'tournament': tournamentID
                    }
                    games.append(game)

    return games
