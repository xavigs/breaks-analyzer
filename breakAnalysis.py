import sys
import flashScore

if len(sys.argv) == 2:
    if sys.argv[1] != "today" and sys.argv[1] != "tomorrow":
        print("ERROR: El paràmetre passat és incorrecte. S'espera el dia a analitzar (today o tomorrow)")
    else:
        day = sys.argv[1]
        print(day)
        exit()
        url = flashScore.getDailyGames(day)
else:
    print("ERROR: El nombre de paràmetres és incorrecte.")
