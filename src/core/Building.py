class Building():

    _color = ''
    _size = ()
    _type = ''
    _index = 0

    def __init__(self, buildingType, **kwargs):
        type_size = {
            'church': (1, 1),
            'draw_well': (1, 1),
            'fair': (2, 1),
            'government': (2, 3),
            'hotel': (2, 2),
            'house': (2, 1),
            'shop': (2, 2),
            'small_totem': (1, 1),
            'totem': (1, 2),
            'workshop': (1, 2),
        }
        self._type = buildingType
        self._size = type_size[self._type]
        self._color = kwargs.get('color', '')
        self._index = kwargs.get('index', 0)

    def getSize(self):
        return self._size

    def getColor(self):
        return self._color

    def getType(self):
        return self._type

    def getIndex(self):
        return self._index

    def getNeedCountClaims(self):
        count_claims = {
            'church': 0,
            'draw_well': 1,
            'fair': 1,
            'government': 3,
            'hotel': 2,
            'house': 1,
            'shop': 2,
            'small_totem': 0,
            'totem': 0,
            'workshop': 1,
        }
        return count_claims[self._type]

    def getCost(self):
        count_claims = {
            'church': 7,
            'draw_well': 5,
            'fair': 5,
            'government': 5,
            'hotel': 3,
            'house': 1,
            'shop': 3,
            'small_totem': 0,
            'totem': 0,
            'workshop': 2,
        }
        return count_claims[self._type]

    def getIncomeType(self):
        incomeType = {
            'hotel': 'vote',
            'house': 'vote',
            'shop': 'gold',
            'small_totem': 'vote',
            'totem': 'gold',
            'workshop': 'gold',
        }
        return incomeType.get(self.getType(), None)
