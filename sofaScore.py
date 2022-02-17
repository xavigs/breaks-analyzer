# -*- coding: utf-8 -*-
import time
from random import seed
from random import randint
import requests
import json
from utils import *

BASE_URL = "https://api.sofascore.com/api/v1/team/"
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
    print(content)

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

getPlayers(2857, 6500)