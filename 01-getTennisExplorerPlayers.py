# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
sys.path.insert(1, 'models')
import db, objects

categories = [{'category': 'ATP', 'sex': 'M', 'URL_BASE': "https://www.tennisexplorer.com/ranking/atp-men/?page="},
              {'category': 'WTA', 'sex': 'W', 'URL_BASE': "https://www.tennisexplorer.com/ranking/wta-women/?page="}]

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
playersObj.empty() # To delete

for category in categories:
    page = 1
    ranking = 1
    end = False

    while not end:
        print("# Extracting " + categories['category'] + " players from the page " + str(page))
        url = category['URL_BASE'] + str(page)
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        players = soup.select("tbody[class=flags] tr")
        
        if len(players) == 0:
            end = True
            continue
        else:
            for player in players:
                playerDB = {}
                tennisExplorerKeyword = player.select("td[class=t-name] a")[0]['href'].split("/")[2]
                playerDB['_id'] = tennisExplorerKeyword
                playerDB['sex'] = category['sex']
                playerDB['startingRanking'] = ranking
                playerDB['tennisExplorerKeyword'] = tennisExplorerKeyword
                playerDB['tennisExplorerName'] = player.select("td[class=t-name]")[0].text
                playersObj.write(playerDB)
                ranking += 1

        page += 1

dbConnection.close()