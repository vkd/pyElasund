import unittest

from core.SumDice import SumDice


class TestSumDice(unittest.TestCase):

	def test_createNewSumDice_OneDice_checkAllResults(self):
		result = [0 for i in range(8)]
		sumDice = SumDice(1, 6)
		for i in range(6):
			result[sumDice.next()] += 1
		needResult = [0, 1, 1, 1, 1, 1, 1, 0]
		self.assertListEqual(result, needResult)

	def test_createNewSumDice_OneDice_checkAllResultsSixTimes(self):
		result = [0 for i in range(8)]
		sumDice = SumDice(1, 6)
		for i in range(36):
			result[sumDice.next()] += 1
		needResult = [0, 6, 6, 6, 6, 6, 6, 0]
		self.assertListEqual(result, needResult)

	def test_createNewSumDice_TwoDice_checkAllResultsTwice(self):
		result = [0 for i in range(14)]
		sumDice = SumDice(2, 6)
		for i in range(36):
			result[sumDice.next()] += 1
		needResult = [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0]
		self.assertListEqual(result, needResult)

		result = [0 for i in range(14)]
		for i in range(36):
			result[sumDice.next()] += 1
		self.assertListEqual(result, needResult)

if __name__ == '__main__':
	unittest.main()
