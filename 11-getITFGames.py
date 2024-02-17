# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import itfTennis
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
gamesObj = objects.Games(breaksDB)
tournamentsObj = objects.Tournaments(breaksDB)
dayDateTime = date.today()
#dayDateTime += timedelta(1)
day = dayDateTime.strftime("%Y%m%d")
gameDay = dayDateTime.strftime("%Y-%m-%d")
games = itfTennis.getDailyGames(day)
ORIGIN_NAMES = ["Alexander"]
FINAL_NAMES = ["Alex"]

for game in games:
    if game['tournament'][0] == "M" and "/" not in game['home']:
        print(u"{} vs {}".format(game['home'], game['away']))
        gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['home'], 'TE-player2': game['away']}])

        if gameDB is not None:
            tournamentDB = tournamentsObj.find([{'_id': game['tournament'].lower()}])
            gamesObj.update({'tournament': tournamentDB['_id']}, [{'_id': gameDB['_id']}])
        else:
            for index, originName in enumerate(ORIGIN_NAMES):
                gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['home'].replace(originName, FINAL_NAMES[index]), 'TE-player2': game['away']}])

                if gameDB is None:
                    gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['home'], 'TE-player2': game['away'].replace(originName, FINAL_NAMES[index])}])

                    if gameDB is None:
                        gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['home'].replace(originName, FINAL_NAMES[index]), 'TE-player2': game['away'].replace(originName, FINAL_NAMES[index])}])

            if gameDB is not None:
                tournamentDB = tournamentsObj.find([{'_id': game['tournament'].lower()}])
                gamesObj.update({'tournament': tournamentDB['_id']}, [{'_id': gameDB['_id']}])
            else:
                print("NONE!!!")

        print(u"{} vs {}".format(game['away'], game['home']))
        gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['away'], 'TE-player2': game['home']}])

        if gameDB is not None:
            tournamentDB = tournamentsObj.find([{'_id': game['tournament'].lower()}])
            gamesObj.update({'tournament': tournamentDB['_id']}, [{'_id': gameDB['_id']}])
        else:
            for index, originName in enumerate(ORIGIN_NAMES):
                gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['away'].replace(originName, FINAL_NAMES[index]), 'TE-player2': game['home']}])

                if gameDB is None:
                    gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['away'], 'TE-player2': game['home'].replace(originName, FINAL_NAMES[index])}])

                    if gameDB is None:
                        gameDB = gamesObj.find([{'gameDay': gameDay, 'TE-player1': game['away'].replace(originName, FINAL_NAMES[index]), 'TE-player2': game['home'].replace(originName, FINAL_NAMES[index])}])

            if gameDB is not None:
                tournamentDB = tournamentsObj.find([{'_id': game['tournament'].lower()}])
                gamesObj.update({'tournament': tournamentDB['_id']}, [{'_id': gameDB['_id']}])
            else:
                print("NONE!!!")
