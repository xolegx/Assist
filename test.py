import datetime
import requests
import time
import hashlib
now = datetime.datetime.now()
print("Местное время: " + now.strftime("%H:%M"))

re = requests.get("https://geek-jokes.sameerkumar.website/api?format=json")
j = re.json()
print(j['joke'])

api = '98c27fa540b57e03cb899c3b969886ed'
city = 'Санкт-Петербург'
response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&lang=ru&APPID=" + api + "&units=metric")

w = response.json()
print(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")