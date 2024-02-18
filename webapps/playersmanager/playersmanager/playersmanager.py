from django.http import JsonResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import ssl

def strToKeyword(text):
    keyword = text.replace(" ", "-").lower()
    keyword = keyword.replace("'", "-")
    keyword = keyword.replace("(", "")
    keyword = keyword.replace(")", "")
    return keyword

def keywordToStr(text):
    string = text.replace("-", " ").title()
    return string

def button(request):
    return render(request, 'playersmanager.html')

def saveNewPlayer(request):
    tennisExplorerURLParts = request.POST.get('tennisExplorerURL').split("/")
    flashScoreURLParts = None
    sofaScoreURLParts = None
    country = ""

    if request.POST.get('flashScoreURL') != "":
        flashScoreURLParts = request.POST.get('flashScoreURL').split("/")

    if request.POST.get('sofaScoreURL') != "":
        sofaScoreURLParts = request.POST.get('sofaScoreURL').split("/")

    # Get DB Data
    client = MongoClient("mongodb://juxtepuas:DeBuSsY84@cluster0-shard-00-00.3ndc2.mongodb.net:27017,cluster0-shard-00-01.3ndc2.mongodb.net:27017,cluster0-shard-00-02.3ndc2.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-zvh8zj-shard-0&authSource=admin&retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
    db = client['breaksDB']
    playersDB = db.players
    playerDB = playersDB.find_one({'_id': tennisExplorerURLParts[-2]})

    if playerDB is None:
        maxPlayerID = playersDB.find_one({'sex': 'M'}, sort=[("startingRanking", -1)])['startingRanking']

        # Get Tennis Explorer Data
        r = requests.get(request.POST.get('tennisExplorerURL'))
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        tennisExplorerName = soup.select("table[class=plDetail] h3")[0].text
        playerFeatures = soup.select("table[class=plDetail] div[class=date]")

        for playerFeature in playerFeatures:
            if "Country" in playerFeature.text:
                country = playerFeature.text.replace("Country: ", "")
                break

        player = {}
        player['_id'] = tennisExplorerURLParts[-2]
        player['country'] = strToKeyword(country)
        player['tennisExplorerName'] = tennisExplorerName
        player['tennisExplorerKeyword'] = tennisExplorerURLParts[-2]
        player['sex'] = "M"
        player['startingRanking'] = maxPlayerID + 1

        if flashScoreURLParts is not None:
            player['flashScoreId'] = flashScoreURLParts[-2]
            player['flashScoreName'] = keywordToStr(flashScoreURLParts[-3])
        else:
            player['flashScoreId'] = ""
            player['flashScoreName'] = ""

        if sofaScoreURLParts is not None:
            player['sofaScoreID'] = int(sofaScoreURLParts[-1])

        playersDB.insert_one(player)
        return JsonResponse({"output": player}, status=200)
    else:
        return JsonResponse({"output": "Ja existeix, merci"}, status=200)
