import requests
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO
import certifi

def getDailyGames(day):
    # Load FlashScore WS with daily matches
    if day == "today":
        url = "https://d.flashscore.es/x/feed/f_2_0_1_es_1"
    else:
        url = "https://d.flashscore.es/x/feed/f_2_1_1_es_1"

    data = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(crl.HEADER, 0)
    crl.setopt(crl.TIMEOUT, 30)
    crl.setopt(crl.HTTPHEADER, ["x-fsign: SW9D1eZo"])
    crl.setopt(crl.WRITEFUNCTION, data.write)
    crl.setopt(crl.CAINFO, certifi.where())
    crl.perform()
    crl.close()

    return data.getvalue()
