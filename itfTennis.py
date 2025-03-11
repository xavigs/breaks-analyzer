# -*- coding: utf-8 -*-
import sys
import time
import requests
import json
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import *

# Constants
PROXY_LIST_HOME = 'https://www.geonode.com/free-proxy-list'
PROXY_LIST_API = 'https://proxylist.geonode.com/api/proxy-list'
PROXY_LIST_PARAMS = {
    'protocols': 'http, https',
    'limit': 500,
    'page': 1,
    'sort_by': 'lastChecked',
    'sort_type': 'desc'
}
ITF_HOME_URL = 'https://www.itftennis.com/'
SURFACES = {
    'H': 'D',
    'C': 'T',
    'I': 'I',
    'G': 'H',
    'A': 'M'
}
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

def getTournaments(sex, year):
    tournaments = []
    proxiesPool = []
    skip = 0

    # Pre-connection to proxy list home
    print('Connecting to proxy list URL...')
    chromeService = Service('./chromedriver.exe')
    browser = webdriver.Chrome(service=chromeService)
    browser.get(PROXY_LIST_HOME)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Accept all cookies"]'))).click()
    time.sleep(10)

    # Transfer cookies from Selenium to Requests Session
    print('Transferring cookies from Selenium to Session...')
    session = requests.Session()

    for cookie in browser.get_cookies():
        c = {cookie['name']: cookie['value']}
        session.cookies.update(c)

    browser.close()

    # Get proxy list
    print('Getting proxy list...')
    proxiesResponse = session.get(PROXY_LIST_API, params=PROXY_LIST_PARAMS)
    proxiesJSON = json.loads(proxiesResponse.content.decode('utf-8'))
    proxiesData = proxiesJSON['data']

    for proxyData in proxiesData:
        proxy = {
            'protocol': proxyData['protocols'][0],
            'ip': proxyData['ip'],
            'port': proxyData['port']
        }
        proxiesPool.append(proxy)

    '''print(json.dumps(proxiesPool, sort_keys=True, indent=4))
    exit()'''

    # Get cookie from a random URL
    proxyData = proxiesPool.pop()
    #proxy = {f'{proxyData['protocol']}' : f'{proxyData['protocol']}://{proxyData['ip']}:{proxyData['port']}'}
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = '{}:{}'.format(proxyData['ip'], proxyData['port'])
    '''prox.socks_proxy = f"{proxyData['ip']}:{proxyData['port']}"
    prox.ssl_proxy = f"{proxyData['ip']}:{proxyData['port']}"'''

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    print(f'Connecting to proxy {proxy}...')
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    browser = uc.Chrome(options=options, desired_capabilities=capabilities)
    script = "Object.defineProperty(navigator, 'webdriver', {get: () => false})"
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': script})
    browser.get(ITF_HOME_URL)

    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'sign-up-form')))
    except:
        print(browser.page_source)
        exit()

    print('Getting cookies...')

    for cookie in browser.get_cookies():
        if 'incap_ses_' in cookie['name']:
            headers = {'Cookie': f"{cookie['name']}={cookie['value']}"}
            break

    browser.close()
    print(headers)

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
                'country': getKeywordFromString(tournamentData['hostNation']).replace(",", "").replace(".", "").replace('turkiye', 'turkey').replace('china-pr', 'china'),
                'surface': SURFACES[tournamentData['surfaceCode']],
                'sex': sex,
                'year': year
            }
            tournaments.append(tournament)

    print(tournaments)
    return tournaments

def getDailyGames(day):
    games = []
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
                        'home': '{} {}'.format(gameData['sides'][0]['sidePlayer'][0]['player']['person']['lastName'], gameData['sides'][0]['sidePlayer'][0]['player']['person']['firstName']),
                        'away': '{} {}'.format(gameData['sides'][1]['sidePlayer'][0]['player']['person']['lastName'], gameData['sides'][1]['sidePlayer'][0]['player']['person']['firstName']),
                        'tournament': tournamentID
                    }
                    games.append(game)

    return games

def findBreakStats(gameDB, playerTEName, playerFSName):
    breaksData = {}
    matchListURL = 'https://api.itf-production.sports-data.stadion.io/custom/wttCompleteMatchList/{}'.format(gameDB['gameDay'])
    numRetries = 0
    tournamentsData = []

    while numRetries < 5:
        try:
            content = requests.request('GET', matchListURL, data = '', headers = headers).text
            tournamentsData = json.loads(content)['data']
            break
        except:
            time.sleep(2)
            numRetries += 1
    
    if len(tournamentsData) == 0:
        print('No hi siguis')
        return False

    for tournament, tournamentData  in tournamentsData.items():
        if 'tennisId' in tournamentData and tournamentData['tennisId'] is not None and tournamentData['tennisId'].lower() == gameDB['tournament']:
            # We have found the game tournament
            #print(tournamentData['_name'])
            for courtName, courtGames in tournamentData['courts'].items():
                #print(f'Court {courtName} ({len(courtGames)} games)')

                for courtGame in enumerate(courtGames):
                    for gameData in courtGame:
                        if isinstance(gameData, dict):
                            try:
                                homePlayerName = '{} {}'.format(gameData['sides'][0]['sidePlayer'][0]['player']['person']['lastName'], gameData['sides'][0]['sidePlayer'][0]['player']['person']['firstName'])
                                homePlayerSideId = gameData['sides'][0]['sidePlayer'][0]['sideId']
                                awayPlayerName = '{} {}'.format(gameData['sides'][1]['sidePlayer'][0]['player']['person']['lastName'], gameData['sides'][1]['sidePlayer'][0]['player']['person']['firstName'])
                                awayPlayerSideId = gameData['sides'][1]['sidePlayer'][0]['sideId']
                                #print(homePlayerName, awayPlayerName)
                            except:
                                continue

                            if homePlayerName == playerTEName or homePlayerName == playerFSName:
                                playerSideId = homePlayerSideId
                                opponentSideId = awayPlayerSideId
                            elif awayPlayerName == playerTEName or awayPlayerName == playerFSName:
                                playerSideId = awayPlayerSideId
                                opponentSideId = homePlayerSideId
                            else:
                                #print('The player names are different; bye byesos')
                                break

                            if (homePlayerName == gameDB['TE-player1'] or homePlayerName == gameDB['FS-player1']) and (awayPlayerName == gameDB['TE-player2'] or awayPlayerName == gameDB['FS-player2']) or (homePlayerName == gameDB['TE-player2'] or homePlayerName == gameDB['FS-player2']) and (awayPlayerName == gameDB['TE-player1'] or awayPlayerName == gameDB['FS-player1']):
                                # Game found
                                print(playerSideId, opponentSideId)
                                gameStatsURL = 'https://api.itf-production.sports-data.stadion.io/custom/widgetMatchStats/{}'.format(gameData['id'])
                                print(gameStatsURL)
                                numRetries = 0

                                while numRetries < 5:
                                    try:
                                        content = requests.request('GET', gameStatsURL, data = '', headers = headers).text
                                        gameStats = json.loads(content)['data']
                                        break
                                    except:
                                        time.sleep(2)
                                        numRetries += 1

                                for gameStat in gameStats:
                                    if gameStat['setNumber'] == 1 and gameStat['_name'] == 'Break Points Conversions':
                                        if gameStat['sideId'] == playerSideId:
                                            breaksData['player'] = gameStat['value']
                                        elif gameStat['sideId'] == opponentSideId:
                                            breaksData['opponent'] = gameStat['value']
                                        #print(json.dumps(gameStat, sort_keys=True, indent=4))

                                return breaksData

    return breaksData