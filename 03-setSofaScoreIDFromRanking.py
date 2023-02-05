# -*- coding: utf-8 -*-
import json
from colorama import init, Back, Fore, Style
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
playersObj = objects.Players(breaksDB)
init(autoreset = True)

jsonFile = open('sofaScoreTOP500W.json')
playersData = json.load(jsonFile)

for playerIndex, playerData in enumerate(playersData['rankings'][467:500]):
    print(playerData['team']['slug'])
    sofaScoreName = getStringFromKeyword(playerData['team']['slug'])
    origText = ("Mcdonal", "Oconnell", "Mededovic", "Mccabe", "Sasikumar", "Mchugh", "Jr Martin", "Mateus", "Fancutt Thomas", "Mcnally", "Yuan Yue", "Makarova Ekaterina", "Vogele", "Barkova", "Hurricane", "Elizabeth")
    newText = ("McDonal", "O'Connell", "Medjedovic", "McCabe", "Sasi Kumar", "McHugh", "Martin (2003)", "Mateus (2001)", "Fancutt Thomas John", "McNally", "Yuan Yue (1998)", "Makarova Ekaterina (1996)", "Voegele", "Prozorova", "Hurricane Tyra", "Ellie")

    for index in range(0, len(origText)):
        sofaScoreName = sofaScoreName.replace(origText[index], newText[index])

    print(sofaScoreName)
    sofaScoreNameParts = sofaScoreName.split(" ")
    playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

    if playerID is None:
        playerID = playersObj.find([{'flashScoreName': sofaScoreName, 'startingRanking': playerData['ranking']}])

        if playerID is None:
            if len(sofaScoreNameParts) == 4:
                sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[1]
                playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                if playerID is None:
                    print(Fore.RED + Style.BRIGHT + "[ERROR] " + Fore.WHITE + Style.NORMAL + "Player not found in the DB")
                    exit()
                else:
                    playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
            elif len(sofaScoreNameParts) == 3:
                sofaScoreName = sofaScoreNameParts[0] + "-" + sofaScoreNameParts[1] + " " + sofaScoreNameParts[2]
                playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                if playerID is None:
                    sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[1] + "-" + sofaScoreNameParts[2]
                    playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                    if playerID is None:
                        playerID = playersObj.find([{'flashScoreName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                        if playerID is None:
                            sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[1]
                            playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                            if playerID is None:
                                sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[2] + " " + sofaScoreNameParts[1]
                                playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                                if playerID is None:
                                    sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[2]
                                    playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                                    if playerID is None:
                                        sofaScoreName = sofaScoreNameParts[1] + " " + sofaScoreNameParts[2]
                                        playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                                        if playerID is None:
                                            sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[2]
                                            print(Fore.RED + Style.BRIGHT + "[ERROR] " + Fore.WHITE + Style.NORMAL + "Player not found in the DB")
                                            exit()
                                        else:
                                            playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
                                else:
                                    playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
                            else:
                                playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
                        else:
                            playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
                    else:
                        playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
                else:
                    playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
            elif len(sofaScoreNameParts) == 2:
                sofaScoreName = sofaScoreNameParts[1] + " " + sofaScoreNameParts[0]
                playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                if playerID is None:
                    print(Fore.RED + Style.BRIGHT + "[ERROR] " + Fore.WHITE + Style.NORMAL + "Player not found in the DB")
                    exit()
                else:
                    playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
            elif len(sofaScoreNameParts) == 5:
                sofaScoreName = sofaScoreNameParts[0] + " " + sofaScoreNameParts[1] + " " + sofaScoreNameParts[2] + " " + sofaScoreNameParts[4]
                playerID = playersObj.find([{'tennisExplorerName': sofaScoreName, 'startingRanking': playerData['ranking']}])

                if playerID is None:
                    print(Fore.RED + Style.BRIGHT + "[ERROR] " + Fore.WHITE + Style.NORMAL + "Player not found in the DB")
                    exit()
                else:
                    playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
            else:
                print(len(sofaScoreNameParts))
                exit()
        else:
            playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])
    else:
        playersObj.update({'sofaScoreID': playerData['team']['id']}, [{'_id': playerID['_id']}])