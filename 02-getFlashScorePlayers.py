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
    
    if position > 1323:
        if not playersObj.update(player, [{'startingRanking': position}, {'sex': 'W'}]):
            if not playersObj.update(player, [{'startingRanking': position - 1}, {'sex': 'W'}]):
                if not playersObj.update(player, [{'startingRanking': position - 2}, {'sex': 'W'}]):
                    if not playersObj.update(player, [{'startingRanking': position - 3}, {'sex': 'W'}]):
                        if not playersObj.update(player, [{'startingRanking': position - 4}, {'sex': 'W'}]):
                            if not playersObj.update(player, [{'startingRanking': position - 21}, {'sex': 'W'}]):
                                if not playersObj.update(player, [{'startingRanking': position - 5}, {'sex': 'W'}]):
                                    if not playersObj.update(player, [{'startingRanking': position - 25}, {'sex': 'W'}]):
                                        if not playersObj.update(player, [{'startingRanking': position - 6}, {'sex': 'W'}]):
                                            if not playersObj.update(player, [{'startingRanking': position - 7}, {'sex': 'W'}]):
                                                if not playersObj.update(player, [{'startingRanking': position - 17}, {'sex': 'W'}]):
                                                    if not playersObj.update(player, [{'startingRanking': position - 9}, {'sex': 'W'}]):
                                                        if not playersObj.update(player, [{'startingRanking': position - 19}, {'sex': 'W'}]):
                                                            if not playersObj.update(player, [{'startingRanking': position - 14}, {'sex': 'W'}]):
                                                                if not playersObj.update(player, [{'startingRanking': position - 10}, {'sex': 'W'}]):
                                                                    if not playersObj.update(player, [{'startingRanking': position - 11}, {'sex': 'W'}]):
                                                                        if not playersObj.update(player, [{'startingRanking': position - 8}, {'sex': 'W'}]):
                                                                            exit()
    
    position += 1

dbConnection.close()