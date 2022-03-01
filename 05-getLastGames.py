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
invalidCompetitions = (
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
    "UTR Pro Tennis Series 6",
    "UTS Championship",
    "Verbier Open",
    "West Coast Pro Series",
    "World TeamTennis",
    "Zilina"
)
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
                                        previousGame['breakReceived'] = -1
                                    elif opponentGames == 0:
                                        previousGame['breakDone'] = -1
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