# -*- coding: utf-8 -*-
import sys
import flashScore
sys.path.insert(1, 'models')
import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)

players = playersObj.read()

for player in players[0:50]:
    rankingNameLength = len(str(player['startingRanking'])) + len(player['tennisExplorerName'])
    print("\n" + "-" * (rankingNameLength + 25))
    print("|          ({}) {}          |".format(player['startingRanking'], player['tennisExplorerName'].upper()))
    print("-" * (rankingNameLength + 25))
    lastGames = []

    for game in player['lastGames']:
        previousGame = {}
        previousGame['opponent'] = playersObj.find([{'_id': game['opponent']}])['flashScoreId']
        previousGame['date'] = game['time']
        lastGames.append(previousGame)
    
    lastGamesBreaks = flashScore.checkBreaksLastGamesByPlayer(player['flashScoreId'], player['flashScoreName'], lastGames)
    playersObj.updateBreakData(player['_id'], lastGamesBreaks)
    playersObj.printBreakData(player['_id'])