class Map():
	tiles = {}

	def addCorners(self, countPlayers):
		index = 2 * countPlayers
		self.tiles[(index, -1)] = {'type': 'corner'}
		self.tiles[(index + 1, -1)] = {'type': 'corner'}
		self.tiles[(index + 1, 0)] = {'type': 'corner'}

		self.tiles[(index, 10)] = {'type': 'corner'}
		self.tiles[(index + 1, 10)] = {'type': 'corner'}
		self.tiles[(index + 1, 9)] = {'type': 'corner'}
