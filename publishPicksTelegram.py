import asyncio
import re
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
import telegram
from models import db, objects

# Database connection
dbConnection = db.Database()
breaksDB = dbConnection.connect()
picksTelegramObj = objects.PicksTelegram(breaksDB)
tournamentsObj = objects.Tournaments(breaksDB)

# Credentials
TOKEN = '6976497176:AAEL9sNN9ysFrycNN1TmOS0Z68pAyqIzAYU'
bot = telegram.Bot(token=TOKEN)
channelID = '-1001505314231'
#channelID = '222946111'
tipsterlandID = '16775'

# Constants and variables
emojisNumbers = ('0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣')
weekdays = ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')
SURFACES = {'I': 'Pista dura indoor', 'D': 'Pista dura outdoor', 'T': 'Tierra batida', 'H': 'Hierba', 'M': 'Moqueta'}
FLAGS = {
    'germany': '🇩🇪'
}

async def send(imageURL, message):
    await bot.send_photo(chat_id=channelID, photo=imageURL, caption=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# Get Tipsterland picks
picksTelegramDB = picksTelegramObj.find_all()
numPublishedPicks = len(list(picksTelegramDB))
url = 'https://www.tipsterland.com/api/picks/cards?tipster_id={}&month=2&year=2024&pending=false&requestId=1&page=1'.format(tipsterlandID)
jsonContent = json.loads(requests.get(url).text)
soup = BeautifulSoup(jsonContent['data'], 'lxml')
picks = soup.select('div[class*=x-pick-card]')
today = datetime.now()
numPicks = 0
numPick = numPublishedPicks + 1

for pick in picks:
    pickDate = pick.select_one('div[class=pick-card-event-date] span').text
    pickDateParts = pickDate.split(' ')
    pickDateParts[0] = pickDateParts[0].zfill(2)
    pickDateParts[1] = pickDateParts[1].title()
    pickDate = ' '.join(pickDateParts)
    pickDate = datetime.strptime(pickDate, '%d %b. %H:%M')
    pickDate = pickDate.replace(year=today.year)

    if pickDate > today''' or numPicks < 1''':
        # Future pick
        pickDB = {}
        numPickString = str(numPick)
        numPickEmoji = ''

        for numPickChar in numPickString:
            numPickEmoji += emojisNumbers[int(numPickChar)]

        pickDB['pick'] = pick.select_one('div[class^="x-pick-alert"]').text.strip()
        pickDB['competition'] = pick.select_one('div[class=pick-card-competition]').text.strip()
        tournamentParts = pickDB['competition'].split(' ')
        category = tournamentParts[0]
        tournamentName = ' '.join(tournamentParts[1:])

        if category == 'ITF':
            tournament = tournamentsObj.find([{'category': 'ITF'}, {'name': {'$regex': tournamentName}}])

        country = tournament['country']

        if country in FLAGS:
            flag = FLAGS[country]

        pickDB['event'] = pick.select_one('div[class=pick-card-event]').text.strip()
        weekday = weekdays[pickDate.weekday()]
        pickDB['date'] = '{} {}, a las {} h.'.format(weekday, pickDate.strftime('%d/%m'), pickDate.strftime('%H:%M'))
        pickDB['odd'] = pick.select_one('div[class*="odds-rounded-label"]').text.strip()
        print(pickDB)
        foundPick = picksTelegramObj.find([{'date': pickDate.strftime('%Y-%m-%d %H:%M')}, {'pick': pickDB['pick']}])

        if foundPick is None:
            # Get picture
            pickID = pick.select_one('button[data-pick-id]')['data-pick-id']
            pickURL = 'https://www.tipsterland.com/api/dlg-pick-view/{}?dlgId=dlg_pick_card_details&show_tipster=false'.format(pickID)
            r = requests.get(pickURL)
            pickSoup = BeautifulSoup(r.text, 'lxml')
            imageURL = pickSoup.select_one('img[class=pick-image]')['src']

            # Send message to Telegram
            message = '{} *{}*\n\n🏆 {} {}\n📌 {}\n🎾 {}\n⏰ {}\n💰 @{}'.format(numPickEmoji, re.escape(pickDB['pick']), pickDB['competition'], flag, SURFACES[tournament['surface']], pickDB['event'], re.escape(pickDB['date']), pickDB['odd'])
            print(message)
            asyncio.run(send(imageURL, message))

            # Insert into DB
            pickTelegram = {
                '_id': numPick,
                'date': pickDate.strftime('%Y-%m-%d %H:%M'),
                'competition': pickDB['competition'],
                'pick': pickDB['pick'],
                'odd': float(pickDB['odd'].replace(',', '.'))
            }

            picksTelegramObj.create(pickTelegram)
            numPick += 1

    numPicks += 1
