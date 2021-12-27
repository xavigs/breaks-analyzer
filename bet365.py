import credentials
import requests

url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"

querystring = {"sport_id":"13"
            }

headers = {
    'x-rapidapi-host': "betsapi2.p.rapidapi.com",
    'x-rapidapi-key': credentials.RAPIDAPI_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()
print(data['pager'])
exit()
print(len(data['results']))

for fixture in data['results']:
    print(fixture)