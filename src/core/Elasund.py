from core.Player import Player
from core.Board import Board


class Elasund():
    _state = ''

    _board = None
    _players = ()
    _currentPlayerIndex = 0

    _message = ''

    _states = {
        ('*', 'error'): 'error',
        ('', 'init'): 'income',
    }

    _colors = ['red', 'blue', 'green', 'yellow']

    def __init__(self, colors):
        # TODO double colors
        if (len(colors) < 2 or len(colors) > 4):
            self._setError('Count of players must be 2, 3 or 4')
            return
        self._state = ''
        self._message = ''
        self._players = tuple(Player(p) for p in colors)
        self._currentPlayerIndex = 0
        self._board = Board(self._colors, self._players)
        self._changeState('init')

    def getPlayers(self):
        return self._players

    def getCurrentPlayer(self):
        return self._players[self._currentPlayerIndex]

    def getState(self):
        return self._state

    def getTiles(self):
        return self._board.tiles

    def getBuildings(self):
        return self._board.buildings

    def build(self, position, building):
        size = building.getSize()
        square = size[0] * size[1]

        player = self.getCurrentPlayer()

        buildings = []
        claims = {c: 0 for c in self._colors}
        count_claims = 0
        for x in range(size[0]):
            for y in range(size[1]):
                pos = (position[0] + x, position[1] + y,)
                cell = self._board.cells.get(pos, None)
                if cell is not None:
                    if cell[0] == 'ref':
                        cell = self._board.cells[cell[1]]

                    if cell[0] == 'claim':
                        claims[cell[1]['color']] += cell[1]['value']
                        count_claims += 1
                    elif cell[0] == 'building':
                        buildings.append(cell[1])

        for b in buildings:
            if b.getType() in ['church']:
                return 'Church cannot destroy'
            b_size = b.getSize()
            b_square = b_size[0] * b_size[1]
            if square <= b_square:
                return 'Building in (%s, %s) more or equal then current' % pos

        other_gold = 0
        for color, value in claims.items():
            if color != self.getCurrentPlayer().getColor():
                other_gold += value

        if player.gold < building.getCost() + other_gold:
            return 'Need more gold'

        my_claimValue = claims[self.getCurrentPlayer().getColor()]
        for color, value in claims.items():
            if color != self.getCurrentPlayer().getColor() and my_claimValue <= value:
                return 'Current player is not greater claims'

        if count_claims < building.getNeedCountClaims():
            return 'Need more claims'

        # end checked - build building
        player.gold -= building.getCost()
        player.gold -= other_gold

        for color, value in claims.items():
            if color != self.getCurrentPlayer().getColor():
                for p in self._players:
                    if p.getColor() == color:
                        p.gold += value
                        break

        for x in range(size[0]):
            for y in range(size[1]):
                pos = (position[0] + x, position[1] + y,)
                cell = self._board.cells.get(pos, None)
                if cell is not None:
                    if cell[0] == 'ref':
                        cell = self._board.cells[cell[1]]

                    if cell[0] == 'claim':
                        self._board.removeClaim(pos)
                    elif cell[0] == 'building':
                        self._board.destroyBuilding(pos)

        self._board.buildBuilding(building, position)

    def claim(self, position, value):
        return self._board.putClaim(self._players[self._currentPlayerIndex].getColor(), value, position)

    def _setError(self, msg):
        self._changeState('error')
        self._message = msg

    def _changeState(self, cmd):
        if (self._state, cmd) in self._states:
            self._state = self._states.get((self._state, cmd), self._state)
        elif ('*', cmd) in self._states:
            self._state = self._states.get(('*', cmd), self._state)
