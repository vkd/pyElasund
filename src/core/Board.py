import random

from core.Building import Building
from core.Map import Map


class Board():

	_shipPosition = 2
	_shipIsRed = False

	_buildings = {}
	_claims = {}

	_map = None

	def __init__(self, colors, players):
		self._buildings = {
			'church': random.shuffle([Building('church', index=i) for i in range(9)]),
			'draw_well': [Building('draw_well') for i in range(4)],
			'fair': [Building('fair') for i in range(4)],
			'government': [Building('government', index=i) for i in range(3)],
			'hotel': [Building('hotel') for i in range(5)],
			'house': [Building('house', color=colors[i]) for i in range(4)],
			'shop': [Building('shop') for i in range(5)],
			'small_totem': [Building('small_totem', color=colors[i]) for i in range(4)],
			'totem': [Building('totem', color=colors[i]) for i in range(4)],
			'workshop': [Building('workshop', color=colors[i]) for i in range(4)],
		}

		self._claims = {color: [i for i in range(5)] for color in colors}

		self._map = Map()
		self._map.addCorners(len(players))
