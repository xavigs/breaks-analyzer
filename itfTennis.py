# -*- coding: utf-8 -*-
import requests
import json
from utils import *

# Constants
SURFACES = {
    'H': 'D',
    'C': 'T',
    'I': 'I',
    'G': 'H',
    'A': 'M'
}

def getTournaments(sex, year):
    tournaments = []
    skip = 0
    headers = {
        'Cookie': "OptanonAlertBoxClosed=2024-02-15T20:58:39.538Z; _fbp=fb.1.1708030719744.468837504; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP6BUgAP6BUgAEsACBESAnEoAP_gAEPgAAQ4INJD7D7FbSFCwHpzaLsAMAhHRsCAQoQAAASBAmABQAKQIAQCgkAQFASgBAACAAAAICZBIQAECAAACUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAAAAEAAIAAAAEAAAmAgAAIIACAAAhAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAQOhQD2F2K2kKFkPCmQWYAQBCijYEAhQAAAAkCBIAAgAUgQAgFIIAgAIFAAAAAAAAAQEgCQAAQABAAAIACgAAAAAAIAAAAAAAQQAAAAAIAAAAAAAAEAAAAAAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~2072.70.89.93.108.122.149.196.2253.2299.259.2357.311.313.323.2373.338.358.2415.415.449.2506.2526.486.494.495.2568.2571.2575.540.574.2624.609.2677.864.981.1029.1048.1051.1095.1097.1126.1201.1205.1211.1276.1301.1344.1365.1415.1423.1449.1451.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958~dv.%22%2C%22DE6165C8-4835-4FA0-8A84-968DEE75C65A%22%5D%5D; cookieconsent_status=allow; _gid=GA1.2.1862257292.1709452771; FCNEC=%5B%5B%22AKsRol8W8cqT_-QViRCkVCmdh4TuAlyxilMSI7iobiJYGiuPbHg20_Atk4RtOWb3NWLB-amL7cso42rfhyt4mS0ZAlN1d2vw9EzvfTeqpiJ0a0vOAv-IM5_da31_QWKyJKRGNZ8GiZdJUlk_rGJ5rGNyNlG7hj5-Bw%3D%3D%22%5D%5D; __gads=ID=910ac1684170f985:T=1708030979:RT=1709452789:S=ALNI_MbhpQ1gtBR--EqNYPKcFbWizXwZKg; __gpi=UID=00000d23aef5dbcb:T=1708030979:RT=1709452789:S=ALNI_ManTL1YCCZv71q2Emm52YVsJ_nRUg; __eoi=ID=e104c984ec5f0844:T=1708030979:RT=1709452789:S=AA-AfjYRgryyzuZA-4u2WzOvO5Ws; incap_ses_268_178373=KPHyOv+VMxOKXrZK9iC4A21z5WUAAAAAgLTV2oqhlKwijDH2SID7GQ==; visid_incap_178373=7bqtcXtYR4WgyftsiSPiVvp6zmUAAAAAR0IPAAAAAACA7MGyAbnbiN0y5esVr0hyPBNwkZ4no1N/; ARRAffinity=196a83c309c56a708974ff3a9f8713c3f13758cf2adce06853fc42cdccdf5e4f; ARRAffinitySameSite=196a83c309c56a708974ff3a9f8713c3f13758cf2adce06853fc42cdccdf5e4f; nlbi_178373=JRymGsihDhwAc63wtoSRdQAAAAAdre09FATFbS+KL9v5cd2K; _gat_UA-337765-1=1; _ga=GA1.2.1882973956.1708030720; _ga_ZRMHKRE9CL=GS1.1.1709536114.28.1.1709536139.0.0.0; _ga_DH6MMHJPYQ=GS1.2.1709536115.28.1.1709536139.36.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+04+2024+08%3A08%3A59+GMT%2B0100+(hora+est%C3%A1ndar+de+Europa+central)&version=6.23.0&isIABGlobal=false&hosts=&consentId=ee0f0b45-2752-44a1-96b7-dcfd662b300c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=ES%3BCT&AwaitingReconsent=false",
        'If-None-Match': '"5500cdf6"',
        'Referer': "https://www.itftennis.com/en/tournament-calendar/mens-world-tennis-tour-calendar/?categories=All&startdate=2023",
        'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile': "?0",
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    while skip < 600:
        url = "https://www.itftennis.com/tennis/api/TournamentApi/GetCalendar?circuitCode={}T&searchString=&skip={}&take=100&nationCodes=&zoneCodes=&dateFrom={}-01-01&dateTo={}-12-31&indoorOutdoor=&categories=&isOrderAscending=true&orderField=startDate&surfaceCodes=".format(sex, skip, year, year)
        content = requests.request("GET", url, data = "", headers = headers).text
        tournamentsData = json.loads(content)
        skip += 100

        for tournamentData in tournamentsData['items']:
            if tournamentData['surfaceCode'] == 'H' and tournamentData['indoorOrOutDoor'] == 'Indoor':
                tournamentData['surfaceCode'] = 'I'

            tournament = {
                '_id': tournamentData['tournamentKey'].lower(),
                'category': 'ITF',
                'name': tournamentData['tournamentName'],
                'country': getKeywordFromString(tournamentData['hostNation']).replace(",", "").replace(".", ""),
                'surface': SURFACES[tournamentData['surfaceCode']],
                'sex': sex,
                'year': year
            }
            tournaments.append(tournament)

    return tournaments

def getDailyGames(day):
    games = []

    headers = {
        'If-None-Match': '"eba15a1e003323ee2a9fc65246f428a17da87dfd"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    url = "https://ls.fn.sportradar.com/itf/en/Europe:Berlin/gismo/client_dayinfo/{}".format(day)
    print(url)
    content = requests.request("GET", url, data = "", headers = headers).text
    gamesData = json.loads(content)['doc'][0]['data']['matches']

    for gameID, gameData in gamesData.items():
        if "Davis Cup" not in gameData['param5']:
            game = {
                'home': gameData['match']['teams']['home']['name'].replace(", ", " ").replace(",", " ").replace("  ", " "),
                'away': gameData['match']['teams']['away']['name'].replace(", ", " ").replace(",", " ").replace("  ", " "),
                'tournament': gameData['param4']
            }
            games.append(game)

    return games
