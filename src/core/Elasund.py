import random

from core.Player import Player
from core.Board import Board
from core.SumDice import SumDice
from core.Decorators import *


class Elasund():

    def __init__(self, colors):
        self._state = ''

        self._players = tuple([Player(c) for c in colors])

        self._board = None

        self._message = ''

        self._states = {
            ('*', 'error'): 'error',
            ('', 'init'): 'income',
            ('income', 'incomed'): 'building',
            ('income', 'some_ship'): 'change_ship',
            ('change_ship', 'changed'): 'building',
            ('change_ship', 'red_ship'): 'pirate',
            ('pirate', 'pirated'): 'building',
            ('building', 'build'): 'building2',
            ('building2', 'build'): 'claim',
            ('building', 'firstChurch'): 'firstChurch',
            ('building2', 'firstChurch'): 'firstChurch2',
            ('firstChurch', 'build'): 'building2',
            ('firstChurch2', 'build'): 'claim',
            ('building', 'skip'): 'claim',
            ('building2', 'skip'): 'claim',
            ('claim', 'claimed'): 'adding',
            ('claim', 'skip'): 'adding',
            ('adding', 'add'): 'income',
            ('adding', 'skip'): 'income',
            ('*', 'win'): 'winner',
        }

        self._colors = ['red', 'blue', 'green', 'yellow']

        self._sumDice = SumDice(2, 6)

        # TODO check double colors
        if (len(colors) < 2 or len(colors) > 4):
            self._setError('Count of players must be 2, 3 or 4')
            self._players = ()
            return

        self._currentPlayerIndex = random.randrange(len(self._players))
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

    @checkStateDecorator(('income',), 'Error: current state is not income')
    @returnOkIfNotError
    def income(self):
        dice = self._sumDice.next()

        self._board.shipIsRed = dice == 7
        if dice == self._board.shipPosition or self._board.shipIsRed:
            self._changeState('some_ship')
            return 'change_ship'

        ''' Income '''
        self._board.shipPosition = dice
        self._calcIncome()
        self._changeState('incomed')

    @checkStateDecorator(('change_ship',), 'Error: current state is not change_ship')
    @returnOkIfNotError
    def change_ship(self, row):
        if row < 2 or row > 12 or row == 7:
            return 'Error: incorrect row value'
        if row == self._board.shipPosition:
            return 'Error: no choise some ship position'

        if self._board.shipIsRed:
            self._board.shipPosition = row
            self._changeState('red_ship')
            return {'success': 'pirate_ship', 'cards': self._board.getCountCubeByRow(), 'current_player_count_on_walls': self._board.getCountCubeOnWallByPlayer(self.getCurrentPlayer().getColor())}
        else:
            correct_pos = {
                2: (4, ),
                3: (5, ),
                4: (2, 6, ),
                5: (3, 8, ),
                6: (4, 9, ),
                8: (5, 10, ),
                9: (6, 11, ),
                10: (8, 12, ),
                11: (9, ),
                12: (10, ),
            }
            if row in correct_pos[self._board.shipPosition]:
                self._board.shipPosition = row
                self._calcIncome()
                self._changeState('changed')
            else:
                return 'Error: next position must be diff 2'

    @checkStateDecorator(('pirate',), 'Error: current state is not pirate')
    @returnOkIfNotError
    @changeStateOnSuccessful('pirated')
    def pirate(self, cards, needCurentPlayer):
        needCards = self._board.getCountCubeByRow()
        for color, count in needCards:
            player = None
            for p in self._players:
                if p.getColor() == color:
                    player = p
                    break
            gold = cards.get(color, {}).get('gold', 0)
            if player.gold < gold:
                return 'Error: %s player need %s gold' % (color, gold)

            red = cards.get(color, {}).get('red', 0)
            if player.votes['red'] < red:
                return 'Error: %s player need %s red vote card' % (color, red)

            green = cards.get(color, {}).get('green', 0)
            if player.votes['green'] < green:
                return 'Error: %s player need %s green vote card' % (color, green)

            blue = cards.get(color, {}).get('blue', 0)
            if player.votes['blue'] < blue:
                return 'Error: %s player need %s blue vote card' % (color, blue)

            if (gold + red + blue + green) != count:
                return 'Error: %s player must give %s cards' % (color, count)

        countCubesOnWalls = self._board.getCountCubeOnWallByPlayer(self.getCurrentPlayer().getColor())
        gold = needCurentPlayer.get(color, {}).get('gold', 0)
        red = needCurentPlayer.get(color, {}).get('red', 0)
        green = needCurentPlayer.get(color, {}).get('green', 0)
        blue = needCurentPlayer.get(color, {}).get('blue', 0)
        if (gold + red + blue + green) != countCubesOnWalls:
            return 'Error: current player must take %s cards' % countCubesOnWalls

        for color, count in needCards:
            player = None
            for p in self._players:
                if p.getColor() == color:
                    player = p
                    break
            player.gold -= cards.get(color, {}).get('gold', 0)
            player.votes['red'] -= cards.get(color, {}).get('red', 0)
            player.votes['green'] -= cards.get(color, {}).get('green', 0)
            player.votes['blue'] -= cards.get(color, {}).get('blue', 0)

        currentPlayer = self.getCurrentPlayer()
        currentPlayer.gold += needCurentPlayer.get(color, {}).get('gold', 0)
        currentPlayer.votes['red'] += needCurentPlayer.get(color, {}).get('red', 0)
        currentPlayer.votes['green'] += needCurentPlayer.get(color, {}).get('green', 0)
        currentPlayer.votes['blue'] += needCurentPlayer.get(color, {}).get('blue', 0)

    @checkStateDecorator(('building', 'building2', ), 'Error: current state is not building')
    @returnOkIfNotError
    @changeStateOnSuccessful('build')
    def build(self, position, building, **addition):
        if building.getType() == 'church':
            return 'Error: use buildChurch'
        size = building.getSize()
        square = size[0] * size[1]

        player = self.getCurrentPlayer()

        if building.getType() in ['house', 'small_totem', 'totem', 'workshop']:
            if building.getColor() != player.getColor():
                return 'Error: this building to another player'

        buildings = []
        claims = {c: 0 for c in self._colors}
        count_claims = 0
        for x in range(size[0]):
            for y in range(size[1]):
                pos = (position[0] + x, position[1] + y,)
                cell = self._board.cells.get(pos, None)
                if cell is not None:
                    if cell['type'] == 'ref':
                        cell = self._board.cells[cell['position']]

                    if cell['type'] == 'claim':
                        claims[cell['claim']['color']] += cell['claim']['value']
                        count_claims += 1
                    elif cell['type'] == 'building':
                        buildings.append(cell['building'])

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
                    if cell['type'] == 'ref':
                        cell = self._board.cells[cell['position']]

                    if cell['type'] == 'claim':
                        self._board.removeClaim(pos)
                    elif cell['type'] == 'building':
                        self._preDestroy(cell['building'], pos)

        self._preBuild(building, position)

    @checkStateDecorator(('building', 'building2', ), 'Error: current state is not building')
    @returnOkIfNotError
    @changeStateOnSuccessful('build')
    def buildWall(self, position):
        player = self.getCurrentPlayer()
        wall = player.getNextWall()
        if wall['type'] == 'none':
            return 'Error: player build max walls'

        wall_cost = self._board.getWallCost(position)
        if wall_cost <= 0:
            return 'Error: cell is not for wall'
        if player.gold < wall_cost:
            return 'Error: player need more gold'

        if wall['type'] == 'point':
            self._removeVictoryPoint(player, 1)
        elif wall['type'] == 'vote':
            for i in range(wall['count']):
                player.votes[self._board.getRandomVote()] += 1

        msg = self._board.buildWall(position, wall['value'], player.getColor())
        if msg is not None:
            return msg

    @checkStateDecorator(('building', 'building2', ), 'Error: current state is not building')
    @returnOkIfNotError
    @changeStateOnSuccessful('build')
    def buildChurch(self):
        if len(self._board.buildings['church']) == 9:
            return 'Error: first time use buildFirstChurch()'

    @checkStateDecorator(('building', 'building2', ), 'Error: current state is not building')
    def buildFirstChurch(self):
        if len(self._board.buildings['church']) != 9:
            return 'Error: use buildChurch()'

        result = [self._board.buildings['church'][i]._index for i in range(2)]

        self._changeState('firstChurch')
        return {'success': 'ok', 'values': result}

    @checkStateDecorator(('firstChurch', 'firstChurch2', ), 'Error: current state is not firstChurch')
    @returnOkIfNotError
    @changeStateOnSuccessful('build')
    def selectFirstChurch(self, index):
        if len(self._board.buildings['church']) != 9:
            return 'Error: use buildChurch()'
        if index != 0 and index != 1:
            return 'Error: index must be 0 or 1'
        self._board.destroyBuilding((2, 5,))
        self._board.buildBuilding(self._board.buildings['church'][i], (2, 5,))

    @checkStateDecorator(('claim',), 'Error: current state is not claim')
    @returnOkIfNotError
    @changeStateOnSuccessful('claimed')
    def claim(self, position, value, **addition):
        return self._board.putClaim(self.getCurrentPlayer().getColor(), value, position)

    @checkStateDecorator(('claim',), 'Error: current state is not claim')
    @returnOkIfNotError
    @changeStateOnSuccessful('claimed')
    def takeTwoGold(self):
        self.getCurrentPlayer().gold += 2

    @checkStateDecorator(('adding',), 'Error: current state is not adding')
    @returnOkIfNotError
    @changeStateOnSuccessful('add')
    def adding(self, action):
        # TODO release adding
        pass

    @checkStateDecorator(('building', 'building2', 'claim', 'adding'), 'Error: current state is not correct')
    @returnOkIfNotError
    @changeStateOnSuccessful('skip')
    def skip(self):
        pass

    def victory(self, player):
        self._changeState('win')
        self._message = '%s player is win' % player.getColor()

    def _calcIncome(self):
        ''' Income '''
        y = self._board.getRowByDice(self._board.shipPosition)
        for x in range(0, self._board.getMaxWidthBoard() + 1):
            pos = (x, y,)
            cell = self._board.cells.get(pos, None)
            if cell is None:
                break

            if cell['type'] == 'ref':
                cell = self._board.cells[cell['position']]

            if cell['type'] != 'building':
                break

            building = cell['building']
            incomeType = building.getIncomeType()
            if incomeType is None:
                break

                for p in self._players:
                    if p.getColor() == building.getColor():
                        if incomeType == 'gold':
                            p.gold += 1
                        elif incomeType == 'vote':
                            p.votes[self._board.getRandomVote()] += 1
                        break

    def _preBuild(self, building, position):
        building.setColor(self.getCurrentPlayer().getColor())
        self.getCurrentPlayer().mills += self._board.getCountMills(position)
        self._removeVictoryPoint(self.getCurrentPlayer(), building.getCubes())
        self._board.buildBuilding(building, position)

    def _preDestroy(self, building, position):
        for p in self.getPlayers():
            if p == building.getColor():
                p.mills -= self._board.getCountMills(position)
                self._addVictoryPoint(p, building.getCubes())
                break
        self._board.destroyBuilding(position)

    def _setError(self, msg):
        self._changeState('error')
        self._message = msg

    def _changeState(self, cmd):
        if (self._state, cmd) in self._states:
            self._state = self._states.get((self._state, cmd), self._state)
        elif ('*', cmd) in self._states:
            self._state = self._states.get(('*', cmd), self._state)

    def _addVictoryPoint(self, player, value):
        player.victoryPoint += value

    def _removeVictoryPoint(self, player, value):
        player.victoryPoint -= value
        if player.victoryPoint <= 0:
            count_check = 0
            for pos, cell in self._board.cells.items():
                if cell['type'] == 'building':
                    if cell['building'].getColor() == player.getColor():
                        count_check += cell['building'].getCubes()

            count_check += self._board.getCubesByMills(player.mills)

            count_check += (player._wall - 1) / 3

            if count_check >= 10:
                self.victory(player)
            else:
                self.error = 'Check count cubes on %s player' % player.getColor()

    def _nextPlayer(self):
        self._currentPlayerIndex = (self._currentPlayerIndex + 1) % len(self.getPlayers())
