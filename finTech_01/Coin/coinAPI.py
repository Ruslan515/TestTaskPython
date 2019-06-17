from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def coinAPIres():#logger, numThread): 
	
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
	
	parameters = {'start':'1',
	'limit':'10', # возвращаем первые 10 токенов
	'convert':'USD',
	'sort' : 'volume_24h'}# которые осторированны по объему за 24 часа
	
	headers = {'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': 'xxxxxxxxx',}  #здесь нужно поставить ваш ключ API
	
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(url, params=parameters)
		timeResp = response.elapsed.total_seconds() # время отклика
		data_first10 = json.loads(response.text) # данные
		return timeResp, data_first10['data'] # возвращаем время отклика и данные(массив словарей со всеми данными о 10 токенах) 
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
