import os
import webbrowser
import sys
import requests


def weather():
	'''Для работы этого кода нужно зарегистрироваться на сайте
	https://openweathermap.org или переделать на ваше усмотрение под что-то другое'''
	try:
		params = {'q': 'London', 'units': 'metric', 'lang': 'ru', 'appid': 'ключ к API'}
		response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
		if not response:
			raise
		w = response.json()
		print(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

	except:
		print('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def about():
	print('я умею узнавать погоду, говорю сколько время и могу рассказать анекдот')


def clock():
	print('time')


def joke():
	print('finger')

