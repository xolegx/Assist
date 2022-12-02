import os
import webbrowser
import sys
import requests
import datetime


def weather():
	'''Для работы этого кода нужно зарегистрироваться на сайте
	https://openweathermap.org'''
	try:
		api = '98c27fa540b57e03cb899c3b969886ed'
		city = 'London'
		response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&lang=ru&APPID=" + api + "&units=metric")
		if not response:
			raise
		w = response.json()
		print(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

	except:
		print('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def about():
	print('Я умею узнавать погоду, говорю сколько время и могу рассказать анекдот')


def clock():
	now = datetime.datetime.now()
	print("Местное время: " + now.strftime("%H:%M"))


def joke():
	print('finger')

