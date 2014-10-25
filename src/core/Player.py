class Player():

	_color = ''
	_victoryPoint = 10
	_mills = 0

	def __init__(self, color):
		self._color = color

	def getColor(self):
		return self._color

	def getVictoryPoint(self):
		return self._victoryPoint

	def getMills(self):
		return self._mills
