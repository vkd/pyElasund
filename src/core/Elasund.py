from core.Player import Player
from core.Board import Board


class Elasund():
	_state = ''

	_board = None
	_players = ()

	_message = ''

	_states = {
		('*', 'error'): 'error',
		('', 'init'): 'income',
	}

	_colors = ['red', 'blue', 'green', 'yellow']

	def __init__(self, colors):
		if (len(colors) < 2 or len(colors) > 4):
			self._setError('Count of players must be 2, 3 or 4')
			return
		self._players = tuple(Player(p) for p in colors)
		self._board = Board(self._colors, self._players)
		self._changeState('init')

	def getPlayers(self):
		return self._players

	def getState(self):
		return self._state

	def _setError(self, msg):
		self._changeState('error')
		self._message = msg

	def _changeState(self, cmd):
		if (self._state, cmd) in self._states:
			self._state = self._states.get((self._state, cmd), self._state)
		elif ('*', cmd) in self._states:
			self._state = self._states.get(('*', cmd), self._state)
