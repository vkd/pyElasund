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
        self._size = type_size[buildingType]
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
