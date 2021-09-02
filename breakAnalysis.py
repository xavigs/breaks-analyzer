import sys
import flashScore

if len(sys.argv) < 3:
    if len(sys.argv) == 1:
        day = "today"
    else:
        if sys.argv[1] != "today" and sys.argv[1] != "tomorrow":
            print("ERROR: El paràmetre passat és incorrecte. S'espera el dia a analitzar (today o tomorrow)")
            exit()
        else:
            day = sys.argv[1]
else:
    print("ERROR: El nombre de paràmetres és incorrecte.")
    exit()

for game in flashScore.getDailyGames(day):
    precedents = flashScore.getPrecedents(game['id'], game['keyword1'], game['keyword2'])
