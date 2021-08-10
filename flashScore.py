import requests
from bs4 import BeautifulSoup

def getDailyGames(day):
    # Load FlashScore WS with daily matches
    if day == "today":
        url = "https://d.flashscore.es/x/feed/f_2_0_1_es_1"
    else:
        url = "https://d.flashscore.es/x/feed/f_2_1_1_es_1"

    return url
