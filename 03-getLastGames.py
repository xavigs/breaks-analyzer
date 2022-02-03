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
startLimit = 1
endLimit = 500
index = 1
currentYear = date.today().year
invalidCompetitions = ("A Day at the Drive (Adelaide)",
                        "Abu Dhabi - exh.",
                        "World TeamTennis",
                        "Laver Cup",
                        "Netherlands - Championship",
                        "Czech league",
                        "Bundesliga - men",
                        "Battle of the Brits 2",
                        "Battle of the Brits",
                        "UK Pro Series",
                        "UTR Pro Match Series",
                        "UTR Pro Tennis Series 5",
                        "Ultimate Tennis Showdown 2 2020",
                        "Challenge Elite FFT 3",
                        "Challenge Elite FFT 2",
                        "Challenge Elite FFT",
                        "Ultimate Tennis Showdown 2",
                        "UTR Pro Tennis Series 4",
                        "Grand Slam Tennis Tours MatchPlay 2020",
                        "UTR Pro Tennis Series",
                        "Grand Slam Tennis Tours MatchPlay")
shownCompetitions = []

for player in players:
    if index < startLimit:
        index += 1
        continue
    elif index > endLimit:
        break
    else:
        rankingNameLength = len(str(index)) + len(player['tennisExplorerName'])
        print("\n" + "-" * (rankingNameLength + 25))
        print("|          ({}) {}          |".format(index, player['tennisExplorerName'].upper()))
        print("-" * (rankingNameLength + 25))
        year = currentYear
        lastGames = []

        while len(lastGames) < 8 and year > 2018:
            url = "https://www.tennisexplorer.com/player/" + player['tennisExplorerKeyword'] + "?annual=" + str(year)
            print(url)
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
                            competitionLinks = game.select("a")

                            if len(competitionLinks) > 0:
                                competition = game.select("a")[0].text.strip()
                            else:
                                competition = game.select("span")[0].text.strip()

                            validCompetition = competition not in invalidCompetitions
                        else:
                            # Game
                            if validCompetition:
                                if competition not in shownCompetitions:
                                    try:
                                        print("\t-> {}".format(competition))
                                    except Exception as e:
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

                                    if playerGames > 10:
                                        numGames = playerGames // 10
                                        playerGames = numGames
                                    elif opponentGames > 10:
                                        numGames = opponentGames // 10
                                        opponentGames = numGames
                                    
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