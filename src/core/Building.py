class Building():

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

    def setColor(self, color):
        if self.getType() not in ['house', 'small_totem', 'totem', 'workshop']:
            self._color = color

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

    def getCubes(self):
        cubes = {
            'church': 1,
            'draw_well': 1,
            'fair': 1,
            'government': 2,
            'hotel': 1,
            'shop': 1,
        }
        return cubes.get(self._type, 0)

    def getCubesByLine(self, y):
        cubesByLine = {
            ('church', 0): 1,
            ('draw_well', 0): 1,
            ('fair', 0): 1,
            ('government', 0): 1,
            ('government', 1): 1,
            ('hotel', 0): 1,
            ('shop', 0): 1,
        }
        return cubesByLine.get((self._type, y), 0)
