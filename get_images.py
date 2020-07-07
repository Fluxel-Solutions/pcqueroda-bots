import requests
import json

url = "https://bing-image-search1.p.rapidapi.com/images/search"

headers = {
    'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
    'x-rapidapi-key': "2ef7d32b60msh66373608c8b8a44p196ddfjsne7a020b41d7a"
    }

games_with_images = {}

with open('games.json', 'r') as games:
    for game in json.load(games)['list']:
        try:
            querystring = {"q": f"{game['name']} wallpaper", "count": 1}
            response = requests.request("GET", url, headers=headers, params=querystring)
            games_with_images[game['name']] = response.json()['value'][0]['thumbnailUrl']
        except:
            print('Error: ' + game['name'])

print(games_with_images)

with open('games_images.json', 'w+') as images:
    json.dump(games_with_images, images, indent=4, sort_keys=True)
