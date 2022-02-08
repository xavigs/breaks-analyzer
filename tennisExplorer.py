# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils import *
from datetime import date, timedelta

COMPETITIONS_TO_SKIP = (
    "A Day at the Drive (Adelaide)",
    "Abu Dhabi - exh.",
    "Battle of the Brits",
    "Battle of the Brits 2",
    "Bundesliga - men",
    "Challenge Elite FFT",
    "Challenge Elite FFT 2",
    "Challenge Elite FFT 3",
    "Czech league",
    "Laver Cup",
    "Netherlands - Championship",
    "UK Pro Series",
    "Ultimate Tennis Showdown 2",
    "Ultimate Tennis Showdown 2 2020",
    "UTR Pro Match Series",
    "UTR Pro Tennis Series 4",
    "UTR Pro Tennis Series 5",
    "World TeamTennis",
)

def getLastGamesByPlayer(playerID, numGames = 8):
    year = date.today().year
    print("# Player => {}".format(player['tennisExplorerKeyword']))
    lastGames = []

    while len(lastGames) < numGames and year > 2018:
        url = "https://www.tennisexplorer.com/player/{}?annual={}".format(player['tennisExplorerKeyword'], year)
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

                                if len(lastGames) == numGames:
                                    break

        year -= 1

    return lastGames

def getDailyGames(day = "today", sex = "men"):
    gamesDay = day == "today" and date.today() or date.today() + timedelta(days=1)

    if sex == "men":
        url = "https://www.tennisexplorer.com/next/?type=atp-single&year={}&month={}&day={}".format(gamesDay.year, '{:02d}'.format(gamesDay.month), '{:02d}'.format(gamesDay.day))
    else:
        url = "https://www.tennisexplorer.com/next/?type=wta-single&year={}&month={}&day={}".format(gamesDay.year, '{:02d}'.format(gamesDay.month), '{:02d}'.format(gamesDay.day))

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    tables = soup.select("table[class=result]")
    dottedDate = "{}. {}. {}".format('{:02d}'.format(gamesDay.day), '{:02d}'.format(gamesDay.month), gamesDay.year)
    played = False
    tournament = None
    tournaments = []
    games = []

    for table in tables:
        liSet = table.parent.select("li[class=set]")

        if len(liSet) > 0 and liSet[0].text == dottedDate:
            rows = table.select("tr")
            break

    for row in rows:
        rowClasses = row['class']

        if "head" in rowClasses:
            # Competition
            tournament = None
            links = row.select("td[class=t-name] a")

            if len(links) > 0:
                tournamentName = row.select("td[class=t-name] a")[0].text.strip()

                if tournamentName not in COMPETITIONS_TO_SKIP:
                    if tournamentName not in tournaments:
                        tournaments.append(tournamentName)

                    href = row.select("td[class=t-name] a")[0]['href'].split("/")
                    tournament = href[1]
            else:
                tournament = "itf"
        else:
            id = row['id']

            if id[-1] != "b":
                # Home player
                thirdColumn = row.select("td")[2]

                if "result" in thirdColumn['class']:
                    # Game played
                    played = True
                else:
                    # Game not played
                    played = False

                    if tournament is not None:
                        game1 = {
                            'tournament': tournament,
                            'time': row.select("td")[0].text[0:5]
                        }
                        game2 = game1.copy()
                        game1['player1'] = row.select("td")[1].select("a")[0]['href'].split("/")[2]
                        game2['player2'] = row.select("td")[1].select("a")[0]['href'].split("/")[2]
            else:
                # Away player
                if not played and tournament is not None:
                    game1['player2'] = row.select("td")[0].select("a")[0]['href'].split("/")[2]
                    game2['player1'] = row.select("td")[0].select("a")[0]['href'].split("/")[2]

                    if game1['tournament'] != "itf" and "itf" not in game1['tournament']:
                        games.append(game1)
                        games.append(game2)

    return games
