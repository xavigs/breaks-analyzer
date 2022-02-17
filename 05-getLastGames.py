# -*- coding: utf-8 -*-
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup
import click
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
invalidCompetitions = ("A Day at the Drive (Adelaide)",
                        "Abu Dhabi - exh.",
                        "Battle of the Brits",
                        "Battle of the Brits 2",
                        "Bundesliga - men",
                        "Challenge Elite FFT",
                        "Challenge Elite FFT 2",
                        "Challenge Elite FFT 3",
                        "Czech league",
                        "Grand Slam Tennis Tours MatchPlay",
                        "Grand Slam Tennis Tours MatchPlay 2020",
                        "Laver Cup",
                        "Netherlands - Championship",
                        "UK Pro Series",
                        "Ultimate Tennis Showdown 2",
                        "Ultimate Tennis Showdown 2 2020",
                        "UTR Pro Match Series",
                        "UTR Pro Tennis Series",
                        "UTR Pro Tennis Series 4",
                        "UTR Pro Tennis Series 5",
                        "World TeamTennis")
shownCompetitions = []

@click.command()
@click.option(
    '-d', '--limit-date',
    help = "Limit date to get previous games", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)
@click.option(
    '-s', '--sex',
    help = "Sex players to get previous games", type = str, default = "M", show_default = True
)
@click.option(
    '-f', '--from-player',
    help = "Index player that we get previous games from", type = int, default = 0, show_default = True
)
@click.option(
    '-l', '--limit-player',
    help = "Index player that we get previous games to", type = int, default = 200, show_default = True
)

def getLastGames(limit_date, sex, from_player, limit_player):
    currentYear = datetime.strptime(limit_date, "%Y-%m-%d").year
    limitYear = currentYear - 4

    if sex == "M":
        players = playersObj.read()
    else:
        players = playersObj.getWomen()

    for player in players[from_player:limit_player]:
        rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
        print("\n" + "-" * (rankingNameLength + 25))
        print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].upper()))
        print("-" * (rankingNameLength + 25))
        year = currentYear
        lastGames = []

        while len(lastGames) < 8 and year > limitYear:
            url = "https://www.tennisexplorer.com/player/" + player['tennisExplorerKeyword'] + "?annual=" + str(year)
            print(url)
            soup = BeautifulSoup(requests.get(url).text, "lxml")
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
                                day = "{}-{}-{}".format(year, time[1], time[0])

                                if day > limit_date:
                                    continue

                                previousGame['time'] = day
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

if __name__ == '__main__':
    getLastGames()