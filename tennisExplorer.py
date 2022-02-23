# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils import *
from datetime import date, datetime

BASE_URL = "https://www.tennisexplorer.com/"
COMPETITIONS_TO_SKIP = (
    "A Day at the Drive (Adelaide)",
    "Abu Dhabi - exh.",
    "Adria Tour",
    "Adria Tour 2",
    "Adria Tour 3",
    "Adria Tour 4",
    "Adriatic Tennis Series",
    "Altec Styslinger Tennis Exhibition",
    "AllAmerican Team Cup",
    "Atlanta Open",
    "Austrian Championship",
    "Austrian Pro Series",
    "Austrian Young Guns",
    "Baltic Tennis League",
    "Basel Open",
    "Battle of Bradenton",
    "Battle of the Brits",
    "Battle of the Brits 2",
    "Battle of the Brits 3",
    "Bett",
    "bett1 Aces",
    "Boodles Tennis Challenge",
    "Bratislava Open",
    "British Tour",
    "British Tour 2",
    "British Tour 3",
    "British Tour 4",
    "British Tour 5",
    "British Tour 6",
    "British Tour 7",
    "British Tour 8",
    "British Tour 9",
    "British Tour 10",
    "British Tour 11",
    "Budapest Kupa Exhibition Series",
    "Bundesliga - men",
    "Campionati Italiani Assoluti",
    "Challenge Elite FFT",
    "Challenge Elite FFT 2",
    "Challenge Elite FFT 3",
    "Copa del Rey",
    "Cup of Friendship",
    "CZE TA President's Cup",
    "Czech league",
    "Delray Beach - seniors",
    "Diriyah Tennis Cup",
    "DTB German Pro Series",
    "East Coast Pro Series",
    "Eastern European Championship",
    "European Pro Tennis Series",
    "Finnish Tennis Tour",
    "FPT Portugal Series",
    "FPT Portugal Series 2",
    "FPT Portugal Series 3",
    "FPT Portugal Series 4",
    "Friendship Cup",
    "GP de la Gruyere",
    "Grand Slam Tennis Tours MatchPlay",
    "Grand Slam Tennis Tours MatchPlay 2020",
    "Hawaii Open",
    "HSC Cup Piestany",
    "Hurlingham - exhibition",
    "Indian Wells - pre-qualifier",
    "International Premier League",
    "International Tennis Series",
    "Israel National Tennis Tour",
    "Italian Championship",
    "Italian National Tour",
    "Kooyong - exh.",
    "Laver Cup",
    "Liga MAPFRE de Tenis",
    "Liga MAPFRE de Tenis 2",
    "Liga MAPFRE de Tenis 3",
    "Liga MAPFRE de Tenis 4",
    "Liga MAPFRE de Tenis 5",
    "London - seniors",
    "Macha Lake Open",
    "Marbello Exhibition Series",
    "Merko Cup",
    "Moravia Open",
    "National Championship",
    "National Tennis Tour Switzerland",
    "Netherlands - Championship",
    "New Zealand Premier League",
    "ÖTV Challenge Series",
    "ÖTV Challenge Series 2",
    "ÖTV Challenge Series 3",
    "ÖTV Challenge Series 4",
    "Peugeot Tennis Tour",
    "Polish National Tour",
    "Polish National Tour 2",
    "Polish National Tour 3",
    "Polish National Tour 4",
    "Polish National Tour 5",
    "Polish National Tour 6",
    "Privatbanka Open",
    "Securitas Pro Cup",
    "SK Soccer Cup",
    "Svijany Open",
    "Swedish Summer Tour",
    "Swiss Masters",
    "Tennis Point Exhibition Series",
    "Tennis Point Exhibition Series 2",
    "Tennis Point Exhibition Series 3",
    "Tennis Point Exhibition Series 4",
    "Tennis Point Exhibition Series 5",
    "Tennis Point Exhibition Series 6",
    "Tennis Point Exhibition Series 7",
    "Tennis Point Exhibition Series 8",
    "Tennis Point Exhibition Series 9",
    "Tennis Point Exhibition Series 10",
    "Tennis Point Exhibition Series 11",
    "Tennis Point Series (USA)",
    "Tennis Point Series 2 (USA)",
    "Tennisportalen Open",
    "Thiem's Seven",
    "Tie-Break Cup Zermatt",
    "Tipsport Elite Trophy",
    "Top League CTS",
    "TPG Exhibition Series",
    "UK Pro Series",
    "UK Pro Series 2",
    "UK Pro Series 3",
    "UK Pro Series 4",
    "UK Pro Series 5",
    "Ultimate Tennis Showdown",
    "Ultimate Tennis Showdown 2",
    "Ultimate Tennis Showdown 3",
    "Ultimate Tennis Showdown 2 2020",
    "UTF Invitational",
    "UTR Leschly Challenge",
    "UTR Pro Match Series",
    "UTR Pro Tennis Series",
    "UTR Pro Tennis Series 2",
    "UTR Pro Tennis Series 3",
    "UTR Pro Tennis Series 4",
    "UTR Pro Tennis Series 5",
    "UTS Championship",
    "Verbier Open",
    "West Coast Pro Series",
    "World TeamTennis",
    "Zilina"
)
SEX_KEYWORDS = {'M': 'atp-men', 'W': 'wta-women'}
SURFACE_ABBREVIATIONS = {
    "Clay": "T",
    "Grass": "H",
    "Hard": "D",
    "Indoors": "I"
}

def getLastGamesByPlayer(playerID, numGames = 8):
    year = date.today().year
    print("# Player => {}".format(player['tennisExplorerKeyword']))
    lastGames = []

    while len(lastGames) < numGames and year > 2018:
        url = BASE_URL + "player/{}?annual={}".format(player['tennisExplorerKeyword'], year)
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

def getDailyGames(day = date.today().strftime("%Y-%m-%d"), sex = "men"):
    gamesDay = datetime.strptime(day, "%Y-%m-%d")

    if sex == "men":
        url = BASE_URL + "next/?type=atp-single&year={}&month={}&day={}".format(gamesDay.year, '{:02d}'.format(gamesDay.month), '{:02d}'.format(gamesDay.day))
    else:
        url = BASE_URL + "next/?type=wta-single&year={}&month={}&day={}".format(gamesDay.year, '{:02d}'.format(gamesDay.month), '{:02d}'.format(gamesDay.day))

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

def getTournaments(sex, year):
    tournaments = []
    url = BASE_URL + "calendar/{}/{}/".format(SEX_KEYWORDS[sex], year)
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    rows = soup.select("table[id=tournamentList] tbody tr")

    for row in rows:
        if not "month" in row['class']:
            tournament = {}
            rowHead = row.select("th")
            
            if len(rowHead) > 0:
                tournamentElement = rowHead[0].select("a")[0]
                tournamentPrize = int(row.select("td[class=tr]")[0].text.split(" ")[0].replace(",", ""))
                tournament['_id'] = tournamentElement['href'].split("/")[1]
                tournament['sex'] = sex
                tournament['name'] = tournamentElement.text
                tournament['surface'] = SURFACE_ABBREVIATIONS[row.select("td[class=s-color] span")[0]['title']]

                if " chall" in tournament['name']:
                    tournament['category'] = "CH"
                elif " ITF" in tournament['name']:
                    tournament['category'] = "ITF"
                elif sex == "M":
                    tournament['category'] = "ATP"

                    if tournamentPrize > 2000000:
                        tournament['subcategory'] = "GS"
                    elif tournamentPrize > 1200000:
                        tournament['subcategory'] = "500"
                    else:
                        tournament['subcategory'] = "250"
                else:
                    tournament['category'] = "WTA"

                    if tournamentPrize > 2000000:
                        tournament['subcategory'] = "GS"
                    elif tournamentPrize > 1200000:
                        tournament['subcategory'] = "500"
                    else:
                        tournament['subcategory'] = "250"

                urlTournament = BASE_URL + "{}/{}/{}/".format(tournament['_id'], year, SEX_KEYWORDS[sex])
                soup = BeautifulSoup(requests.get(urlTournament).text, "lxml")
                tournament['country'] = getKeywordFromString(soup.select("h1")[0].text.split(" (")[1].split(")")[0])
                tournaments.append(tournament)
    
    return tournaments