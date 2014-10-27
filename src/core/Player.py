class Player():

	_color = ''
	_victoryPoint = 10
	_mills = 0
	_wall = 1
	gold = 0
	votes = {'red': 0, 'blue': 0, 'green': 0}

	def __init__(self, color):
		self._color = color

	def getColor(self):
		return self._color

	def getVictoryPoint(self):
		return self._victoryPoint

	def getMills(self):
		return self._mills

	def getWall(self):
		result = {'type': 'none', 'count': 0}
		if self._wall >= 10:
			return result

		result['type'] = 'vote'
		result['count'] = 2 if self._wall >= 5 else 1
		if self._wall % 3 == 0:
			result['type'] = 'point'
			result['count'] = 0

		self._wall += 1
		return result
