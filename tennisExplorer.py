# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils import *
from datetime import date, datetime

BASE_URL = "https://www.tennisexplorer.com/"
COMPETITIONS_TO_SKIP = (
    "A Day at the Drive (Adelaide)", # 29/01/2021
    "Abu Dhabi - exh.", # 16/12/2021
    "Adria Tour", # 03/07/2020
    "Adria Tour 2", # 13/06/2020
    "Adria Tour 3", # 20/06/2020
    "Adria Tour 4", # 27/06/2020
    "Adriatic Tennis Series", # 08/06/2020
    "Altec Styslinger Tennis Exhibition", # 29/06/2020
    "AllAmerican Team Cup", # 03/07/2020
    "Asian Games", # 24/09/2023
    "Atlanta Open", # 24/08/2020
    "Austrian Bundesliga", # 22/05/2022
    "Austrian Championship", # 27/06/2021
    "Austrian Pro Series", # 27/05/2020
    "Austrian Young Guns", # 07/07/2020
    "Baltic Tennis League", # 02/06/2020
    "Basel Open", # 18/07/2020
    "Battle of Bradenton", # 11/06/2020
    "Battle of the Brits", # 23/06/2020
    "Battle of the Brits 2", # 27/07/2020
    "Battle of the Brits 3", # 20/12/2020
    "Bett", # 17/07/2020
    "bett1 Aces", # 13/07/2020
    "Boodles Tennis Challenge", # 25/06/2019
    "Bratislava Open", # 17/06/2020
    "British Tour", # 03/07/2020
    "British Tour 2", # 06/07/2020
    "British Tour 3", # 09/07/2020
    "British Tour 4", # 18/07/2020
    "British Tour 5", # 23/07/2020
    "British Tour 6", # 21/08/2020
    "British Tour 7", # 28/08/2020
    "British Tour 8", # 04/09/2020
    "British Tour 9", # 02/10/2020
    "British Tour 10", # 02/10/2020
    "British Tour 11", # 18/12/2020
    "Budapest Kupa Exhibition Series", # 22/05/2020
    "Bundesliga - men", # 03/07/2022
    "Bundesliga - women", # 08/05/2022
    "Campionati Italiani Assoluti", # 22/06/2020
    "Challenge Elite FFT", # 06/07/2020
    "Challenge Elite FFT 2", # 13/07/2020
    "Challenge Elite FFT 3", # 20/07/2020
    "Copa del Rey", # 21/08/2020
    "Cup of Friendship", # 04/07/2020
    "CZE TA President's Cup", # 26/05/2020
    "Czech league", # 12/12/2021
    "Delray Beach - seniors", # 06/01/2021
    "Diriyah Tennis Cup", # 12/12/2019
    "DTB German Pro Series", # 09/06/2020
    "East Coast Pro Series", # 01/06/2020
    "Eastern European Championship", # 15/06/2020
    "European Pro Tennis Series", # 08/06/2020
    "Finnish Tennis Tour", # 21/08/2020
    "FPT Portugal Series", # 24/06/2020
    "FPT Portugal Series 2", # 01/07/2020
    "FPT Portugal Series 3", # 08/07/2020
    "FPT Portugal Series 4", # 15/07/2020
    "France - Championship", # 20/11/2022
    "Friendship Cup", # 18/05/2020
    "German Championships", # 06/12/2022
    "GP de la Gruyere", # 21/07/2020
    "Grand Slam Tennis Tours MatchPlay", # 26/05/2020
    "Grand Slam Tennis Tours MatchPlay 2020",
    "Hawaii Open",
    "HSC Cup Piestany", # 23/07/2020
    "Hurlingham - exhibition", # 21/06/2022
    "International Premier League", # 27/07/2020
    "International Tennis Series", # 18/04/2020
    "Israel National Tennis Tour", # 23/06/2020
    "Italian Championship", # 20/06/2020
    "Italian National Tour", # 29/06/2020
    "Kooyong - exh.", # 14/01/2020
    "Laver Cup", # 23/09/2022
    "Liga MAPFRE de Tenis", # 10/07/2020
    "Liga MAPFRE de Tenis 2", # 15/07/2020
    "Liga MAPFRE de Tenis 3", # 17/07/2020
    "Liga MAPFRE de Tenis 4", # 22/07/2020
    "Liga MAPFRE de Tenis 5", # 29/07/2020
    "Liverpool - exhibition", # 16/06/2022
    "London - seniors", # 25/11/2021
    "Macha Lake Open", # 24/06/2020
    "Marbello Exhibition Series", # 06/05/2020
    "Merko Cup", # 29/07/2020
    "Moravia Open", # 15/07/2020
    "National Championship", # 11/07/2021
    "National Tennis Tour Switzerland", # 01/07/2020
    "Netherlands - Championship", # 13/12/2022
    "New Zealand Premier League", # 03/06/2020
    "ÖTV Challenge Series", # 06/07/2020
    "ÖTV Challenge Series 2", # 13/07/2020
    "ÖTV Challenge Series 3", # 20/07/2020
    "ÖTV Challenge Series 4", # 27/07/2020
    "Pacific Games", # 22/11/2023
    "Pan American Games", # 24/10/2023
    "Peugeot Tennis Tour", # 25/08/2020
    "Polish national championship", # 10/07/2022
    "Polish National Tour", # 17/06/2020
    "Polish National Tour 2", # 06/07/2020
    "Polish National Tour 3", # 24/07/2020
    "Polish National Tour 4", # 29/07/2020
    "Polish National Tour 5", # 15/08/2020
    "Polish National Tour 6", # 20/08/2020
    "Privatbanka Open", # 09/07/2020
    "Securitas Pro Cup", # 24/07/2020
    "SK Soccer Cup", # 23/05/2020
    "Svijany Open", # 29/07/2020
    "Swedish Summer Tour", # 18/06/2020
    "Swiss Masters", # 06/07/2020
    "Swiss Nationalliga A", # 07/05/2022
    "Tennis Point Exhibition Series", # 01/05/2020
    "Tennis Point Exhibition Series 2", # 07/05/2020
    "Tennis Point Exhibition Series 3", # 10/05/2020
    "Tennis Point Exhibition Series 4", # 14/05/2020
    "Tennis Point Exhibition Series 5", # 20/05/2020
    "Tennis Point Exhibition Series 6", # 27/05/2020
    "Tennis Point Exhibition Series 7", # 03/06/2020
    "Tennis Point Exhibition Series 8", # 10/06/2020
    "Tennis Point Exhibition Series 9", # 07/07/2020
    "Tennis Point Exhibition Series 10", # 14/07/2020
    "Tennis Point Exhibition Series 11", # 21/07/2020
    "Tennis Point Series (USA)", # 14/05/2020
    "Tennis Point Series 2 (USA)", # 22/05/2020
    "Tennisportalen Open", # 26/06/2020
    "Thiem's Seven", # 07/07/2020
    "Tie-Break Cup Zermatt", # 09/07/2020
    "Tipsport Elite Trophy", # 08/08/2020
    "Top League CTS", # 11/06/2020
    "TPG Exhibition Series", # 08/06/2020
    "UK Pro Series", # 16/01/2022
    "UK Pro Series 2", # 20/07/2020
    "UK Pro Series 3", # 27/07/2020
    "UK Pro Series 4", # 03/08/2020
    "UK Pro Series 5", # 10/08/2020
    "Ultimate Tennis Showdown", # 14/06/2020
    "Ultimate Tennis Showdown 2", # 25/07/2020
    "Ultimate Tennis Showdown 3", # 16/10/2020
    "Ultimate Tennis Showdown 2 2020",
    "UTF Invitational", # 09/06/2020
    "UTR Leschly Challenge", # 31/05/2020
    "UTR Pro Match Series", # 01/01/2022
    "UTR Pro Tennis Series", # 09/05/2022
    "UTR Pro Tennis Series 2", # 17/01/2022
    "UTR Pro Tennis Series 3", # 13/12/2020
    "UTR Pro Tennis Series 4", # 25/01/2021
    "UTR Pro Tennis Series 5",
    "UTR Pro Tennis Series 6", # 03/01/2022
    "UTR Pro Tennis Series 7", # 28/03/2022
    "UTR Pro Tennis Series 8", # 04/07/2022
    "UTR Pro Tennis Series 9",
    "UTS Championship", # 24/05/2021
    "Valencia challenge", # 05/06/2020
    "Verbier Open", # 26/09/2020
    "Waikiki Cup", # 18/12/2022
    "West Coast Pro Series", # 01/06/2020
    "World TeamTennis", # 14/11/2021
    "World Tennis League", # 19/12/2022
    "Zilina" # 30/07/2020
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

                    #if game1['tournament'] != "itf" and "itf" not in game1['tournament']:
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

                if row.select("td[class^=tr]")[0].text != "-":
                    tournamentPrize = int(row.select("td[class=tr]")[0].text.split(" ")[0].replace(",", ""))
                else:
                    tournamentPrize = 0

                tournament['_id'] = tournamentElement['href'].split("/")[1]
                tournament['sex'] = sex
                tournament['year'] = year
                tournament['name'] = tournamentElement.text.strip()

                if tournament['name'] not in COMPETITIONS_TO_SKIP:
                    print(tournamentElement.text.strip())
                    tagColor = row.select("td[class=s-color]")[0]
                    tagColorHasChild = len(tagColor.find_all()) != 0
                    print(tagColorHasChild)

                    if tagColorHasChild:
                        tournament['surface'] = SURFACE_ABBREVIATIONS[row.select("td[class=s-color] span")[0]['title']]
                    else:
                        tournament['surface'] = None

                    if " chall" in tournament['name']:
                        tournament['category'] = "CH"
                    elif " ITF" in tournament['name']:
                        tournament['category'] = "ITF"
                    elif sex == "M":
                        tournament['category'] = "ATP"

                        if tournamentPrize > 12000000:
                            tournament['subcategory'] = "GS"
                        elif tournamentPrize > 5000000:
                            tournament['subcategory'] = "1000"
                        elif tournamentPrize > 1300000:
                            tournament['subcategory'] = "500"
                        else:
                            tournament['subcategory'] = "250"
                    else:
                        tournament['category'] = "WTA"

                        if tournamentPrize > 12000000:
                            tournament['subcategory'] = "GS"
                        elif tournamentPrize > 5000000:
                            tournament['subcategory'] = "1000"
                        elif tournamentPrize > 1300000:
                            tournament['subcategory'] = "500"
                        else:
                            tournament['subcategory'] = "250"

                    urlTournament = BASE_URL + "{}/{}/{}/".format(tournament['_id'], year, SEX_KEYWORDS[sex])
                    soup = BeautifulSoup(requests.get(urlTournament).text, "lxml")
                    tournament['country'] = getKeywordFromString(soup.select("h1")[0].text.split(" (")[1].split(")")[0])
                    tournaments.append(tournament)

    return tournaments
