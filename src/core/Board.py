import random

from core.Building import Building


class Board():

	_shipPosition = 2
	_shipIsRed = False

	buildings = {}
	claims = {}

	tiles = {}

	def __init__(self, colors, players):
		self.buildings = {
			'church': random.shuffle([Building('church', index=i) for i in range(9)]),
			'draw_well': [Building('draw_well') for i in range(4)],
			'fair': [Building('fair') for i in range(4)],
			'government': [Building('government', index=i) for i in range(3)],
			'hotel': [Building('hotel') for i in range(5)],
			'house': {c: Building('house', color=c) for c in colors},
			'shop': [Building('shop') for i in range(5)],
			'small_totem': {c: Building('small_totem', color=c) for c in colors},
			'totem': {c: Building('totem', color=c) for c in colors},
			'workshop': {c: Building('workshop', color=c) for c in colors},
		}

		self.claims = {color: [i for i in range(5)] for color in colors}

		self._addCorners(len(players))
		self._addStartBuildings(players)

	def buildBuilding(self, building, position):
		if building is None:
			return 'Error: building is empty'

		size = building.getSize()

		for x in range(size[0]):
			for y in range(size[1]):
				if self.tiles.get((position[0] + x, position[1] + y), None) is not None:
					return 'Error: cells not free'

		for x in range(size[0]):
			for y in range(size[1]):
				self.tiles[(position[0] + x, position[1] + y)] = ('ref', position,)

		self.tiles[position] = ('building', building)

	def _addCorners(self, countPlayers):
		index = 2 * countPlayers
		self.tiles[(index, -1)] = {'type': 'corner'}
		self.tiles[(index + 1, -1)] = {'type': 'corner'}
		self.tiles[(index + 1, 0)] = {'type': 'corner'}

		self.tiles[(index, 10)] = {'type': 'corner'}
		self.tiles[(index + 1, 10)] = {'type': 'corner'}
		self.tiles[(index + 1, 9)] = {'type': 'corner'}

	def _addStartBuildings(self, players):
		totem_position = {
			'red': (4, 5),
			'blue': (1, 5),
			'green': (4, 3),
			'yellow': (1, 3),
		}
		small_totem_position = {
			'red': (3, 2),
			'blue': (2, 2),
			'green': (3, 7),
			'yellow': (2, 7),
		}
		for player in players:
			self.buildBuilding(self.buildings['totem'].pop(player.getColor(), None), totem_position[player.getColor()])
			self.buildBuilding(self.buildings['small_totem'].pop(player.getColor(), None), small_totem_position[player.getColor()])
