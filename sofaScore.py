# -*- coding: utf-8 -*-
import time
from random import seed
from random import randint
import requests
import json
from utils import *

BASE_URL = "https://api.sofascore.com/api/v1/team/"
HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ca-ES,ca;q=0.9,es;q=0.8,en;q=0.7',
    'authority': 'api.sofascore.com',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"d9193d7c2e"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
}

def getJSONFromURL(url):
    return json.loads(requests.request("GET", url, data = "", headers = HEADERS).text)

def getPlayers(fromID = 1, toID = None):
    seed(1)
    currentID = fromID

    while currentID <= toID:
        print("# Analyzing the team with ID {}...".format(currentID))
        url = "{}{}".format(BASE_URL, currentID)
        dataJSON = getJSONFromURL(url)
        
        if dataJSON['team']['category']['sport']['id'] == 5:
            print(dataJSON)
            exit()

        currentID += 1
        secondsToWait = randint(10, 15)
        time.sleep(secondsToWait)

getPlayers(11, 100)