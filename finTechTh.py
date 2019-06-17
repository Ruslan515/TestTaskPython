import threading
import logging
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import numpy as np

resp_time = [0, 0, 0, 0, 0, 0, 0, 0] # массив для хранения данных по отклику от CoinMarket
 
# Данные по работе с API взяты с док-и с сайта
def coinAPIres(logger, numThread): 
	
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
	
	parameters = {'start':'1',
	'limit':'10',	# получаем первые 10 токенов
	'convert':'USD',
	'sort' : 'volume_24h'} # которые осторированны по объему за 24 часа
	
	headers = {'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': 'XXXXXXXXX',} # здесь нужно поставить ваш ключ API
	
	global resp_time # объявляем что это глобальный массив
	logger.debug('coinAPIres function run') # делаем запись в debug file о времени начала потока numThread
	session = Session()
	session.headers.update(headers)
	try:
		response = session.get(url, params=parameters) 
		timeResp = response.elapsed.total_seconds() #время отклика от CoinMarket
		resp_time[numThread] = timeResp # записываем в массив время отклика под номером потока который передаеться в виде аргумента
		logger.debug('coinAPIres ended with: time:{} array time:{}'.format(timeResp, resp_time)) # делаем запись времени отклика данного потока и весь массив
		data = json.loads(response.text)
		return timeResp, data['data'] #возвращаем время и данные
		#print(data)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)


# функция для вывода данных потоков в файл thFinTech.log
def get_logger():
	logger = logging.getLogger("threading_example")
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler("thFinTech.log")
	fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s' #формат вывода: время - имя потока - урвоень - лог. сообщение
	formatter = logging.Formatter(fmt)
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	return logger
 
if __name__ == '__main__':
	threads = [] # массив потоков
	logger = get_logger()
	thread_names = ['Thread #0', 'Thread #1', 'Thread #2', 'Thread #3', 'Thread #4', 'Thread #5', 'Thread #6', 'Thread #7'] # имена потоков. Их всего 8
	# запускаем потоки
	for i in range(len(thread_names)): 
		my_thread = threading.Thread(target=coinAPIres, name=thread_names[i], args=(logger,i))
		threads.append(my_thread)
		my_thread.start()
	# останавливаем потоки
	for t in threads:
		t.join()
	print(resp_time)
	resp_time_np = np.array(resp_time) # преобразуем в массив numpy
	per_80 = np.percentile(resp_time_np, 80) # считаем 80% процентиль времени отклика
	rps = 8 / resp_time_np.sum()
	print(rps)
	
	resp_bool = True # переменная для определения истинности условия: времени отклика всех потоков менее 500мс 
	for i in range(len(resp_time_np)):
		if resp_time_np[i] >= 0.5: # если хотя бы у одного потока время отклика менее 500 мс то тест не проходит проверку
			resp_bool = False
			break
	print(resp_bool)
	#проверяем условие на соответсвие 80% процентиля менее 450мс и того что каждый поток успел уложиться в 500 мс
	if (resp_bool) & (per_80 < 0.45):
		print('Test OK. 80% percentile: {:.3f} '.format(per_80))# тест пройден
	else:
		print('Test Bad. 80% percentile: {:.3f} '.format(per_80))# тест непройден