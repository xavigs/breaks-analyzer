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
    print("Analyzing {}...".format(player['flashScoreName']))
    lastGames = []

    for game in player['lastGames']:
        previousGame = {}
        previousGame['opponent'] = playersObj.find([{'_id': game['opponent']}])['flashScoreId']
        previousGame['date'] = game['time']
        lastGames.append(previousGame)
    
    lastGamesBreaks = flashScore.checkBreaksLastGamesByPlayer(player['flashScoreId'], player['flashScoreName'], lastGames)
    playersObj.updateBreakData(player['_id'], lastGamesBreaks)