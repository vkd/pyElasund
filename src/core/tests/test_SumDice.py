import unittest

from core.SumDice import SumDice


class TestSumDice(unittest.TestCase):

    def test_createNewSumDice_OneDice_checkAllResults(self):
        result = [0 for i in range(9)]
        sumDice = SumDice(1, 7)
        for i in range(7):
            result[sumDice.next()] += 1
        needResult = [0, 1, 1, 1, 1, 1, 1, 1, 0]
        self.assertListEqual(result, needResult)

        for j in range(2, 10):
            for i in range(7):
                result[sumDice.next()] += 1
            needResult = [0, j, j, j, j, j, j, j, 0]
            self.assertListEqual(result, needResult)

    def test_createNewSumDice_TwoDice_checkAllResults(self):
        result = [0 for i in range(14)]
        sumDice = SumDice(2, 6)
        for i in range(36):
            result[sumDice.next()] += 1
        needResult = [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0]
        self.assertListEqual(result, needResult)

        for j in range(10):
            result = [0 for i in range(14)]
            for i in range(36):
                result[sumDice.next()] += 1
            self.assertListEqual(result, needResult)

if __name__ == '__main__':
    unittest.main()
