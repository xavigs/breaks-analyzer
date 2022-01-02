# -*- coding: utf-8 -*-
import sys
from datetime import date
import requests
from bs4 import BeautifulSoup
sys.path.insert(1, 'models')
import db, objects
from utils import *

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)

players = playersObj.read()
startLimit = 11
endLimit = 20
index = 1
currentYear = date.today().year
invalidCompetitions = ("A Day at the Drive (Adelaide)",
                        "Abu Dhabi - exh.")
shownCompetitions = []

for player in players:
    if index < startLimit:
        index += 1
        continue
    elif index > endLimit:
        break
    else:
        year = currentYear
        lastGames = []

        while len(lastGames) < 8 and year > 2018:
            url = "https://www.tennisexplorer.com/player/" + player['tennisExplorerKeyword'] + "?annual=" + str(year)
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, "lxml")
            table = soup.select("div[id=matches-" + str(year) + "-1-data]")
            
            if len(table) > 0:
                schedule = table[0].select("tr")
                noMatches = schedule[0].select("td.first.tl")

                if len(noMatches) == 0:
                    for game in schedule:
                        if "head" in game['class']:
                            # Competition
                            competition = game.select("a")[0].text.strip()
                            validCompetition = competition not in invalidCompetitions
                        else:
                            # Game
                            if validCompetition:
                                if competition not in shownCompetitions:
                                    print(competition)
                                    shownCompetitions.append(competition)
                                previousGame = {}
                                time = game.select("td")[0].text.split(".")
                                previousGame['time'] = "{}-{}-{}".format(year, time[1], time[0])
                                player1 = game.select("td")[2].select("a")[0]['href'].split("/")[-2]
                                player2 = game.select("td")[2].select("a")[1]['href'].split("/")[-2]
                                numPlayer = player1 == player['tennisExplorerKeyword'] and 1 or 2
                                previousGame['opponent'] = numPlayer == 1 and player2 or player1
                                score = game.select("td")[4].select("a")[0].text.split(", ")
                                
                                if score[0] != "":
                                    set1 = score[0].split("-")
                                    playerGames = numPlayer == 1 and int(set1[0]) or int(set1[1])
                                    opponentGames = numPlayer == 1 and int(set1[1]) or int(set1[0])

                                    if playerGames > 60:
                                        playerGames = 6
                                    elif opponentGames > 60:
                                        opponentGames = 6
                                    
                                    if playerGames - opponentGames >= 2:
                                        previousGame['breakDone'] = 1
                                        previousGame['breakReceived'] = -1
                                    elif opponentGames - playerGames >= 2:
                                        previousGame['breakDone'] = -1
                                        previousGame['breakReceived'] = 1
                                    elif playerGames == 0:
                                        previousGame['breakDone'] = 0
                                    elif opponentGames == 0:
                                        previousGame['breakReceived'] = 0
                                    else:
                                        previousGame['breakDone'] = -1
                                        previousGame['breakReceived'] = -1

                                    lastGames.append(previousGame)

                                    if len(lastGames) == 8:
                                        break
            
            year -= 1
    
    updatedPlayer = {}
    updatedPlayer['lastGames'] = lastGames
    updatedPlayer['definedGames'] = 0
    playersObj.update(updatedPlayer, [{'_id': player['_id']}])
    index += 1