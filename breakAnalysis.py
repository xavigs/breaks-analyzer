# -*- coding: utf-8 -*-
import sys
import flashScore
sys.path.insert(1, 'models')
import db

breaksDB = db.Database().connect()
print(breaksDB.list_collection_names())
exit()

if len(sys.argv) < 3:
    if len(sys.argv) == 1:
        day = "today"
    else:
        if sys.argv[1] != "today" and sys.argv[1] != "tomorrow" and sys.argv[1] != "test":
            print("ERROR: The received argument is wrong. The system expects the day to analyze (today, tomorrow or test)")
            exit()
        else:
            day = sys.argv[1]
else:
    print("ERROR: Number of received arguments is wrong.")
    exit()

dailyGames = flashScore.getDailyGames(day)

for game in dailyGames:
    previousGames = flashScore.getPreviousGames(game['id'], game['keyword1'], game['keyword2'])
