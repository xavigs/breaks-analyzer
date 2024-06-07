# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import click
from utils import *
import tennisExplorer
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersMissingObj = objects.PlayersMissing(breaksDB)
playersObj = objects.Players(breaksDB)
invalidCompetitions = (
    "A Day at the Drive (Adelaide)", # 29/01/2021
    "Abu Dhabi - exh.", # 16/12/2021
    "Adria Tour", # 03/07/2020
    "Adria Tour 2", # 13/06/2020
    "Adria Tour 3", # 20/06/2020
    "Adria Tour 4", # 27/06/2020
    "Adriatic Tennis Series", # 08/06/2020
    "African Games",
    "Altec Styslinger Tennis Exhibition", # 29/06/2020
    "AllAmerican Team Cup", # 03/07/2020
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
    "British Tour 10", # 09/10/2020
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
    "France - Championship", # 20/11/2022
    "FPT Portugal Series", # 24/06/2020
    "FPT Portugal Series 2", # 01/07/2020
    "FPT Portugal Series 3", # 08/07/2020
    "FPT Portugal Series 4", # 15/07/2020
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
shownCompetitions = []

@click.command()
@click.option(
    '-d', '--limit-date',
    help = "Limit date to get previous games", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)
@click.option(
    '-t', '--tomorrow',
    help = "Set tomorrow as limit date", type = str, default = "N", show_default = True
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
    help = "Index player that we get previous games to", type = int, default = 999999, show_default = True
)

def getLastGames(limit_date, tomorrow, sex, from_player, limit_player):
    playersMissingObj.empty()
    playersObj.unsetAllToModify()
    playersToModify = tennisExplorer.getLastDaysPlayers()

    if tomorrow == 'Y':
        limit_date = str(date.today() + timedelta(1))

    currentYear = datetime.strptime(limit_date, '%Y-%m-%d').year
    limitYear = currentYear - 4

    if from_player == 0 and limit_player == 999999:
        if sex == 'M':
            players = playersObj.getMenWithSofaScoreID()
        else:
            players = playersObj.getWomenWithSofaScoreID()
    elif from_player > 0 and limit_player == 999999:
        if sex == 'M':
            players = playersObj.getMenWithSofaScoreID(from_player)
        else:
            players = playersObj.getWomenWithSofaScoreID(from_player)
    elif from_player > 0 and limit_player < 999999:
        if sex == 'M':
            players = playersObj.getMenWithSofaScoreID(from_player, limit_player)
        else:
            players = playersObj.getWomenWithSofaScoreID(from_player, limit_player)

    print("{} players with SofaScore ID found in the database.".format(len(list(players))))
    print("{} players are going to be analyzed.".format(len(playersToModify)))
    players.rewind()

    for player in players:
        if player['_id'] not in playersToModify:
            continue
        else:
            rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
            print("\n" + "-" * (rankingNameLength + 25))
            print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].encode('utf-8').upper()))
            print("-" * (rankingNameLength + 25))
            year = currentYear
            lastGames = []

            while len(lastGames) < 8 and year > limitYear:
                url = "https://www.tennisexplorer.com/player/" + player['tennisExplorerKeyword'] + "?annual=" + str(year)
                print(url)
                soup = getSoup(url)
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
                                            print("\t-> {}".format(competition.encode('utf-8')))
                                        except Exception as e:
                                            print("Exception with the competition {}".format(competition))
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
            updatedPlayer['toModify'] = True
            playersObj.update(updatedPlayer, [{'_id': player['_id']}])

if __name__ == '__main__':
    getLastGames()
