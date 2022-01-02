# -*- coding: utf-8 -*-
import sys
import flashScore
sys.path.insert(1, 'models')
import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)

ranking = flashScore.getRanking('wta')
position = 1

for player in ranking:
    del(player['ranking'])
    
    if position > 1250:
        playersObj.update(player, [{'startingRanking': position}, {'sex': 'W'}])
    
    position += 1

dbConnection.close()