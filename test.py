import unittest
from Coin import coinAPI # наша функция находиться в папке Coin в файле coinAPI.py

class coinTest(unittest.TestCase):
	def test_coin(self):
		resp_time, data10 = coinAPI.coinAPIres() # получаем время отклика и данные
		self.assertLess(resp_time, 0.5) # проверяем на условие: время отклика менее 500мс
		
if __name__ == '__main__':
	unittest.main()