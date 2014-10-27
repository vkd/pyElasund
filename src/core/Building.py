class Building():

	_color = ''
	_size = ()

	def __init__(self, type, **kwargs):
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
		self._size = type_size[type]

	def getSize(self):
		return self._size
