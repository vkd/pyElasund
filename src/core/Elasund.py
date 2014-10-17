from core.Player import Player

class Elasund():

	_players = []
	_current_player = None

	def __init__(self, *args):
		self._players = tuple(Player(p) for p in args)

	def getPlayers(self):
		return self._players
