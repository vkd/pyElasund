import itertools
import random


class SumDice():

    def __init__(self, count, maxValue):
        self._count = count
        self._maxValue = maxValue
        self._minValue = 1
        self._listValues = []
        self._createList()

    def next(self):
        if len(self._listValues) == 0:
            self._createList()
        return self._listValues.pop()

    def _createList(self):
        if (len(self._listValues) != 0):
            return 'List not empty'

        range_dice = range(self._minValue, self._maxValue + 1)
        self._listValues = map(sum, itertools.product(range_dice, repeat=self._count))
        random.shuffle(self._listValues)
