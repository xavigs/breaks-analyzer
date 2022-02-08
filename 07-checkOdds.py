from datetime import date
import re
import requests
import ast
import click
import Levenshtein as lev
from colorama import init, Back, Fore, Style
from credentials import *
from utils import *
from models import db, objects

def matchNames(gamesBet365, gameDB):
    maxRatio = 0
    indexMaxRatio = -1

    for indexGame, gameBet365 in enumerate(gamesBet365):
        homeName = gameBet365['home']['name']
        awayName = gameBet365['away']['name']
        #print("{} vs {}".format(homeName, awayName))
        player1FS = gameDB['FS-player1'].split(" ")
        player1TE = gameDB['TE-player1'].split(" ")
        player2FS = gameDB['FS-player2'].split(" ")
        player2TE = gameDB['TE-player2'].split(" ")
        player1Found = True
        player2Found = True

        # Exact string
        for namePart in player1FS:
            if namePart not in homeName and namePart not in awayName:
                player1Found = False
                break

        if not player1Found:
            player1Found = True

            for namePart in player1TE:
                if namePart not in homeName and namePart not in awayName:
                    player1Found = False
                    break

        if player1Found:
            for namePart in player2FS:
                if namePart not in homeName and namePart not in awayName:
                    player2Found = False
                    break

            if not player2Found:
                player2Found = True

                for namePart in player2TE:
                    if namePart not in homeName and namePart not in awayName:
                        player2Found = False
                        break

        if player1Found and player2Found:
            print("Max. ratio: 100%!!")
            return indexGame
        else:
            ratio = getGameRatio(gameBet365, gameDB)

            if ratio > maxRatio:
                maxRatio = ratio
                indexMaxRatio = indexGame
    
    print("Max. ratio: {}".format(maxRatio))
    if maxRatio > 0.7:
        return indexMaxRatio
    else:
        return -1

def getGameRatio(gameBet365, gameDB):
    player1FSRatio1 = getPlayerRatio(gameBet365['home']['name'], gameDB['FS-player1'])
    player1TERatio1 = getPlayerRatio(gameBet365['home']['name'], gameDB['TE-player1'])
    player1FSRatio2 = getPlayerRatio(gameBet365['away']['name'], gameDB['FS-player1'])
    player1TERatio2 = getPlayerRatio(gameBet365['away']['name'], gameDB['TE-player1'])
    player2FSRatio1 = getPlayerRatio(gameBet365['away']['name'], gameDB['FS-player2'])
    player2TERatio1 = getPlayerRatio(gameBet365['away']['name'], gameDB['TE-player2'])
    player2FSRatio2 = getPlayerRatio(gameBet365['home']['name'], gameDB['FS-player2'])
    player2TERatio2 = getPlayerRatio(gameBet365['home']['name'], gameDB['TE-player2'])
    player1Ratios = [player1FSRatio1, player1TERatio1, player1FSRatio2, player1TERatio2]
    player2Ratios = [player2FSRatio1, player2TERatio1, player2FSRatio2, player2TERatio2]
    player1Ratio = max(player1Ratios)
    player2Ratio = max(player2Ratios)
    return (player1Ratio + player2Ratio) / 2

def getPlayerRatio(name1, name2):
    name1Parts = re.split(' |-', name1)
    name2Parts = re.split(' |-', name2)
    numParts = len(name1Parts)
    totalRatios = 0.0

    for name1Part in name1Parts:
        name1Part = str(name1Part)
        maxRatio = 0.0

        for name2Part in name2Parts:
            name2Part = str(name2Part)

            if lev.ratio(name1Part, name2Part) > maxRatio:
                maxRatio = lev.ratio(name1Part, name2Part)

        totalRatios += maxRatio

    ratioAvg = totalRatios / numParts
    return ratioAvg

init(autoreset = True)
@click.command()
@click.option(
    '-d', '--games-day',
    help = "Game date to check", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)

def checkOdds(games_day):
    '''url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"
    querystring = {"sport_id":"13"}
    headers = {
        'x-rapidapi-host': "betsapi2.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers = headers, params = querystring)
    data = response.json()
    gamesBet365 = data['results']
    print(gamesBet365)
    exit()
    printCollection(gamesBet365)
    exit()'''

    gamesBet365 = [{u'league': {u'id': u'10046367', u'name': u'ATP Rotterdam'}, u'our_event_id': u'4650370', u'ss': None, u'away': {u'id': u'10400176', u'name': u'Alejandro Davidovich Fokina'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10416295', u'name': u'Stefanos Tsitsipas'}, u'id': u'114703366', u'sport_id': u'13'}, {u'league': {u'id': u'10046469', u'name': u'ATP Buenos Aires MD'}, u'our_event_id': u'4652510', u'ss': None, u'away': {u'id': u'10364622', u'name': u'Sonego/Vavassori'}, u'updated_at': u'1644324656', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10499124', u'name': u'Bolelli/Gonzalez'}, u'id': u'114753744', u'sport_id': u'13'}, {u'league': {u'id': u'10067564', u'name': u'ITF W25 Porto'}, u'our_event_id': u'4658427', u'ss': None, u'away': {u'id': u'10364673', u'name': u'Maria Gutierrez Carrasco'}, u'updated_at': u'1644344047', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10402528', u'name': u'Yasmine Mansouri'}, u'id': u'114816936', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659154', u'ss': None, u'away': {u'id': u'10813506', u'name': u'Valsecchi/Villoslada'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10813505', u'name': u'Munoz/Tremblay'}, u'id': u'114822066', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659155', u'ss': None, u'away': {u'id': u'10415296', u'name': u'Martinez/Wenger'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10466115', u'name': u'Brugnerotto/Pozzi'}, u'id': u'114822073', u'sport_id': u'13'}, {u'league': {u'id': u'10073146', u'name': u'ITF M25 Cancun'}, u'our_event_id': u'4658934', u'ss': None, u'away': {u'id': u'10424570', u'name': u'Oliver Crawford'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10432858', u'name': u'Keegan Smith'}, u'id': u'114833758', u'sport_id': u'13'}, {u'league': {u'id': u'10073145', u'name': u'ITF M25 Cancun MD'}, u'our_event_id': u'4658808', u'ss': None, u'away': {u'id': u'10813494', u'name': u'Kaghami/Sanchez'}, u'updated_at': u'1644342116', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10813493', u'name': u'Cressoni/Yeshaya'}, u'id': u'114834767', u'sport_id': u'13'}, {u'league': {u'id': u'10073144', u'name': u'ITF W25 Cancun'}, u'our_event_id': u'4658787', u'ss': None, u'away': {u'id': u'10536178', u'name': u'Madison Sieg'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10542680', u'name': u'Maria Fernanda Navarro'}, u'id': u'114835887', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659158', u'ss': None, u'away': {u'id': u'10813508', u'name': u'Kania-Chodun/Papamichail'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644345000', u'home': {u'id': u'10813507', u'name': u'Hosonuma/Santos'}, u'id': u'114836991', u'sport_id': u'13'}, {u'league': {u'id': u'10046358', u'name': u'WTA St. Petersburg'}, u'our_event_id': u'4649905', u'ss': None, u'away': {u'id': u'10400787', u'name': u'Irina-Camelia Begu'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10433205', u'name': u'Shuai Zhang'}, u'id': u'114714555', u'sport_id': u'13'}, {u'league': {u'id': u'10046412', u'name': u'Challenger Cherbourg'}, u'our_event_id': u'4658623', u'ss': None, u'away': {u'id': u'10361465', u'name': u'Ernests Gulbis'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10365582', u'name': u'Dan Added'}, u'id': u'114816495', u'sport_id': u'13'}, {u'league': {u'id': u'10073085', u'name': u'ITF W25 Tucuman'}, u'our_event_id': u'4658539', u'ss': None, u'away': {u'id': u'10428852', u'name': u'Solana Sierra'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10363690', u'name': u'Jazmin Ortenzi'}, u'id': u'114819822', u'sport_id': u'13'}, {u'league': {u'id': u'10073092', u'name': u'ITF W25 Tucuman WD'}, u'our_event_id': u'4658606', u'ss': None, u'away': {u'id': u'10813472', u'name': u'C-Karlau/M Rocca'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10813471', u'name': u'Fruhvirtova/Papadakis'}, u'id': u'114820999', u'sport_id': u'13'}, {u'league': {u'id': u'10050040', u'name': u'UTR Pro Tennis Series California Women'}, u'our_event_id': u'4658811', u'ss': None, u'away': {u'id': u'10521009', u'name': u'Rebecca Lynn'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10520134', u'name': u'Katie Codd'}, u'id': u'114830767', u'sport_id': u'13'}, {u'league': {u'id': u'10050040', u'name': u'UTR Pro Tennis Series California Women'}, u'our_event_id': u'4659806', u'ss': None, u'away': {u'id': u'10401481', u'name': u'Tricia Mar'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644346800', u'home': {u'id': u'10813607', u'name': u'Eliana Hanna'}, u'id': u'114845305', u'sport_id': u'13'}, {u'league': {u'id': u'10073123', u'name': u'ATP Dallas'}, u'our_event_id': u'4659468', u'ss': None, u'away': {u'id': u'10361511', u'name': u'Peter Gojowczyk'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10361670', u'name': u'Liam Broady'}, u'id': u'114828914', u'sport_id': u'13'}, {u'league': {u'id': u'10073123', u'name': u'ATP Dallas'}, u'our_event_id': u'4659467', u'ss': None, u'away': {u'id': u'10417426', u'name': u'Jurij Rodionov'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10403087', u'name': u'Maxime Cressy'}, u'id': u'114828915', u'sport_id': u'13'}, {u'league': {u'id': u'10073145', u'name': u'ITF M25 Cancun MD'}, u'our_event_id': u'4658817', u'ss': None, u'away': {u'id': u'10804492', u'name': u'Bergevi/Veldheer'}, u'updated_at': u'1644342116', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10456064', u'name': u'Farren/Flores'}, u'id': u'114834765', u'sport_id': u'13'}, {u'league': {u'id': u'10073145', u'name': u'ITF M25 Cancun MD'}, u'our_event_id': u'4659000', u'ss': None, u'away': {u'id': u'10813498', u'name': u'F Tessari/G Fitzmaurice'}, u'updated_at': u'1644342116', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10813497', u'name': u'Strode/Vance'}, u'id': u'114834770', u'sport_id': u'13'}, {u'league': {u'id': u'10073145', u'name': u'ITF M25 Cancun MD'}, u'our_event_id': u'4659001', u'ss': None, u'away': {u'id': u'10807801', u'name': u'Novikov/Roelofse'}, u'updated_at': u'1644342116', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10813496', u'name': u'Blancaneaux/Geerts'}, u'id': u'114834771', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659157', u'ss': None, u'away': {u'id': u'10813510', u'name': u'Bhatia/H Gonzalez'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644348600', u'home': {u'id': u'10813509', u'name': u'Helgo/Silva'}, u'id': u'114836985', u'sport_id': u'13'}, {u'league': {u'id': u'10046367', u'name': u'ATP Rotterdam'}, u'our_event_id': u'4654177', u'ss': None, u'away': {u'id': u'10361612', u'name': u'Botic Van De Zandschulp'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644350400', u'home': {u'id': u'10417278', u'name': u'Bernabe Zapata Miralles'}, u'id': u'114763676', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659198', u'ss': None, u'away': {u'id': u'10538412', u'name': u'H. Boyer/D. Boyer'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644350400', u'home': {u'id': u'10461330', u'name': u'Cid Subervi/Oliveira'}, u'id': u'114822064', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659238', u'ss': None, u'away': {u'id': u'10813523', u'name': u'Briand/Musialek'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644350400', u'home': {u'id': u'10810816', u'name': u'Comesana/Monzon'}, u'id': u'114822067', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659239', u'ss': None, u'away': {u'id': u'10813526', u'name': u'Beltre/Puello'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644350400', u'home': {u'id': u'10708798', u'name': u'H Lilleengen/Rivera'}, u'id': u'114822070', u'sport_id': u'13'}, {u'league': {u'id': u'10073147', u'name': u'ITF M15 Punta Cana MD'}, u'our_event_id': u'4659240', u'ss': None, u'away': {u'id': u'10813525', u'name': u'Pichler/Prihodko'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644350400', u'home': {u'id': u'10813524', u'name': u'G Meza/C Loureiro'}, u'id': u'114822074', u'sport_id': u'13'}, {u'league': {u'id': u'10073092', u'name': u'ITF W25 Tucuman WD'}, u'our_event_id': u'4658607', u'ss': None, u'away': {u'id': u'10813473', u'name': u'G P Cano/Rossini'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644352200', u'home': {u'id': u'10698966', u'name': u'Carle/Estable'}, u'id': u'114821000', u'sport_id': u'13'}, {u'league': {u'id': u'10073092', u'name': u'ITF W25 Tucuman WD'}, u'our_event_id': u'4658608', u'ss': None, u'away': {u'id': u'10813474', u'name': u'Herrera/Ruiz'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644352200', u'home': {u'id': u'10810800', u'name': u'Ng/Seibold'}, u'id': u'114821001', u'sport_id': u'13'}, {u'league': {u'id': u'10073092', u'name': u'ITF W25 Tucuman WD'}, u'our_event_id': u'4658613', u'ss': None, u'away': {u'id': u'10749298', u'name': u'Gerlach/Seguel'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644352200', u'home': {u'id': u'10429153', u'name': u'Doldan/Doldan'}, u'id': u'114821005', u'sport_id': u'13'}, {u'league': {u'id': u'10050040', u'name': u'UTR Pro Tennis Series California Women'}, u'our_event_id': u'4658810', u'ss': None, u'away': {u'id': u'10708258', u'name': u'Olivia Halvorsen'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644352200', u'home': {u'id': u'10521008', u'name': u'A-C Lutkemeyer'}, u'id': u'114830764', u'sport_id': u'13'}, {u'league': {u'id': u'10050040', u'name': u'UTR Pro Tennis Series California Women'}, u'our_event_id': u'4658812', u'ss': None, u'away': {u'id': u'10520030', u'name': u'Brandy Walker'}, u'updated_at': u'1644344081', u'time_status': u'0', u'r_id': None, u'time': u'1644352200', u'home': {u'id': u'10740652', u'name': u'Madison Lee'}, u'id': u'114830768', u'sport_id': u'13'}, {u'league': {u'id': u'10073123', u'name': u'ATP Dallas'}, u'our_event_id': u'4652914', u'ss': None, u'away': {u'id': u'10405622', u'name': u'Jack Sock'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10361469', u'name': u'Oscar Otte'}, u'id': u'114729630', u'sport_id': u'13'}, {u'league': {u'id': u'10073123', u'name': u'ATP Dallas'}, u'our_event_id': u'4659465', u'ss': None, u'away': {u'id': u'10425541', u'name': u'Denis Kudla'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10361471', u'name': u'Cedrik-Marcel Stebe'}, u'id': u'114828917', u'sport_id': u'13'}, {u'league': {u'id': u'10073145', u'name': u'ITF M25 Cancun MD'}, u'our_event_id': u'4658999', u'ss': None, u'away': {u'id': u'10813500', u'name': u'Kouzmine/Franco'}, u'updated_at': u'1644342116', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813499', u'name': u'Aragone/Polansky'}, u'id': u'114834764', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659170', u'ss': None, u'away': {u'id': u'10725304', u'name': u'Rogers/Rosca'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813511', u'name': u'Hibino/Kung'}, u'id': u'114836982', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659195', u'ss': None, u'away': {u'id': u'10813516', u'name': u'Cabaj Awad/Glushko'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813515', u'name': u'Failla/Sada Nahimana'}, u'id': u'114836983', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659231', u'ss': None, u'away': {u'id': u'10541182', u'name': u'Imanishi/Ogata'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813520', u'name': u'Partaud/Vedder'}, u'id': u'114836984', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659232', u'ss': None, u'away': {u'id': u'10784554', u'name': u'Fernandez/Torres Murcia'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813517', u'name': u'Fung/Marino'}, u'id': u'114836986', u'sport_id': u'13'}, {u'league': {u'id': u'10073148', u'name': u'ITF W25 Cancun WD'}, u'our_event_id': u'4659233', u'ss': None, u'away': {u'id': u'10813519', u'name': u'Chang/Sun'}, u'updated_at': u'1644344112', u'time_status': u'0', u'r_id': None, u'time': u'1644354000', u'home': {u'id': u'10813518', u'name': u'McAdoo/Sebov'}, u'id': u'114836990', u'sport_id': u'13'}, {u'league': {u'id': u'10046375', u'name': u'ATP Buenos Aires'}, u'our_event_id': u'4653013', u'ss': None, u'away': {u'id': u'10361531', u'name': u'Pedro Martinez'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644355800', u'home': {u'id': u'10405770', u'name': u'Alejandro Tabilo'}, u'id': u'114749202', u'sport_id': u'13'}, {u'league': {u'id': u'10046375', u'name': u'ATP Buenos Aires'}, u'our_event_id': u'4653014', u'ss': None, u'away': {u'id': u'10400495', u'name': u'Pablo Andujar'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644355800', u'home': {u'id': u'10363981', u'name': u'Juan Ignacio Londero'}, u'id': u'114749204', u'sport_id': u'13'}, {u'league': {u'id': u'10073122', u'name': u'ATP Dallas MD'}, u'our_event_id': u'4651402', u'ss': None, u'away': {u'id': u'10812898', u'name': u'Querrey/Withrow'}, u'updated_at': u'1644344113', u'time_status': u'0', u'r_id': None, u'time': u'1644359400', u'home': {u'id': u'10812897', u'name': u'Neff/Thamma'}, u'id': u'114730035', u'sport_id': u'13'}, {u'league': {u'id': u'10046375', u'name': u'ATP Buenos Aires'}, u'our_event_id': u'4653015', u'ss': None, u'away': {u'id': u'10400463', u'name': u'Federico Delbonis'}, u'updated_at': u'1644344079', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10813015', u'name': u'Juan Martin Del Potro'}, u'id': u'114749205', u'sport_id': u'13'}, {u'league': {u'id': u'10073125', u'name': u'ITF M25 Canberra'}, u'our_event_id': u'4655322', u'ss': None, u'away': {u'id': u'10463930', u'name': u'Nikita Volonski'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10463987', u'name': u'Matthew Romios'}, u'id': u'114793482', u'sport_id': u'13'}, {u'league': {u'id': u'10073125', u'name': u'ITF M25 Canberra'}, u'our_event_id': u'4655458', u'ss': None, u'away': {u'id': u'10404567', u'name': u'Eric Vanshelboim'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10488396', u'name': u'Philip Sekulic'}, u'id': u'114793487', u'sport_id': u'13'}, {u'league': {u'id': u'10045269', u'name': u'ITF W25 Canberra'}, u'our_event_id': u'4655462', u'ss': None, u'away': {u'id': u'10425488', u'name': u'Tina Nadine Smith'}, u'updated_at': u'1644344078', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10417989', u'name': u'Abbie Myers'}, u'id': u'114794039', u'sport_id': u'13'}, {u'league': {u'id': u'10045269', u'name': u'ITF W25 Canberra'}, u'our_event_id': u'4655464', u'ss': None, u'away': {u'id': u'10515791', u'name': u'Alexandra Osborne'}, u'updated_at': u'1644344078', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10417988', u'name': u'Priscilla Hon'}, u'id': u'114794041', u'sport_id': u'13'}, {u'league': {u'id': u'10045269', u'name': u'ITF W25 Canberra'}, u'our_event_id': u'4655465', u'ss': None, u'away': {u'id': u'10783578', u'name': u'Sienna Leeson'}, u'updated_at': u'1644344078', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10443880', u'name': u'Talia Gibson'}, u'id': u'114794042', u'sport_id': u'13'}, {u'league': {u'id': u'10045269', u'name': u'ITF W25 Canberra'}, u'our_event_id': u'4655468', u'ss': None, u'away': {u'id': u'10417991', u'name': u'Alicia Smith'}, u'updated_at': u'1644344078', u'time_status': u'0', u'r_id': None, u'time': u'1644361200', u'home': {u'id': u'10417985', u'name': u'Chihiro Muramatsu'}, u'id': u'114794047', u'sport_id': u'13'}, {u'league': {u'id': u'10073125', u'name': u'ITF M25 Canberra'}, u'our_event_id': u'4655286', u'ss': None, u'away': {u'id': u'10416830', u'name': u'Calum Puttergill'}, u'updated_at': u'1644344046', u'time_status': u'0', u'r_id': None, u'time': u'1644366600', u'home': {u'id': u'10361644', u'name': u'Akira Santillan'}, u'id': u'114793474', u'sport_id': u'13'}]

    dbConnection = db.Database()
    breaksDB = dbConnection.connect()
    gamesObj = objects.Games(breaksDB)
    gamesDB = gamesObj.find_all([{'gameDay': games_day, 'profitable': True}])

    for gameDB in gamesDB:
        print(Back.CYAN + Fore.BLACK + " {} vs {} ".format(gameDB['FS-player1'], gameDB['FS-player2']))
        indexGameBet365 = matchNames(gamesBet365, gameDB)
        print(Fore.GREEN + Style.BRIGHT + "Bet365 Index: {}".format(indexGameBet365))
        print(Fore.YELLOW + "Bet365 Game => {} vs {}".format(gamesBet365[indexGameBet365]['home']['name'], gamesBet365[indexGameBet365]['away']['name']))

    exit()

    for fixture in data['results']:
        print(".:: {} vs {} ::.\n".format(fixture['home']['name'], fixture['away']['name']))
        url = "https://betsapi2.p.rapidapi.com/v3/bet365/prematch"
        querystring = {"FI":fixture['id']}
        headers = {
            'x-rapidapi-host': "betsapi2.p.rapidapi.com",
            'x-rapidapi-key': RAPIDAPI_KEY
            }
        response = requests.request("GET", url, headers = headers, params = querystring)
        markets = ast.literal_eval(response.text)

        for othersContent in markets['results'][0]['others']:
            if "first_set_player_to_break_serve" in othersContent['sp']:
                printCollection(othersContent['sp']['first_set_player_to_break_serve'])

if __name__ == '__main__':
    checkOdds()