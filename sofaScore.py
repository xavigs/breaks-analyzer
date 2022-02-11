# -*- coding: utf-8 -*-
import requests
import json
from utils import *

BASE_URL = "https://api.sofascore.com/api/v1/team/"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ca,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'api.sofascore.com',
    'If-None-Match': 'W/"db2547deaf"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
}

'''
    "authority": "api.sofascore.com",
    "cache-control": "max-age=0",
    "sec-ch-ua": "^\^Chromium^^;v=^\^92^^, ^\^"

{
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
'''

def getPlayers(fromID = 1, toID = None):
    currentID = fromID
    end = False

    while not end:
        url = "{}{}".format(BASE_URL, currentID)
        soup = requests.request("GET", url, data = "", headers = HEADERS).text
        print(soup)
        exit()
        dataJSON = json.loads(urllib.request.urlopen(url).read())
        printCollection(dataJSON)
        exit()
        currentID += 1

getPlayers(1, 100)