import requests

url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"

querystring = {"sport_id":"13"
            }

headers = {
    'x-rapidapi-host': "betsapi2.p.rapidapi.com",
    'x-rapidapi-key': "3e97c91aafmshc84c15e2551bf04p1bc471jsn02c308e0a98d"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()
print(data['pager'])
exit()
print(len(data['results']))

for fixture in data['results']:
    print(fixture)