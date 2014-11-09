class SumDice():

    _count = 0
    _minValue = 1
    _maxValue = 0
    _listValues = []

    def __init__(self, count, maxValue):
        self._count = count
        self._maxValue = maxValue
        self._listValues = []
        self._createList()

    def next(self):
        if len(self._listValues) == 0:
            self._createList()
        return self._listValues.pop()

    def _createList(self):
        if (len(self._listValues) != 0):
            return 'List not empty'
        dices = []
        for i in range(self._count):
            dices.append(self._minValue)
        isAll = False
        while not isAll:
            self._listValues.append(sum(dices))

            index = 0
            isNeedInc = True
            while isNeedInc:
                if index == self._count:
                    isNeedInc = False
                    isAll = True
                    break

                dices[index] += 1
                isNeedInc = False
                if (dices[index] > self._maxValue):
                    dices[index] = self._minValue
                    isNeedInc = True

                index += 1
