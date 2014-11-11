import random

from core.Building import Building


class Board():

    def __init__(self, colors, players):
        self.cells = {}

        self._sumDice = None
        self.shipPosition = 0
        self.shipIsRed = False
        self._countPlayers = len(players)

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

        self.claims = {color: [{'color': color, 'value': i} for i in range(5)] for color in colors}

        self._addCorners()
        self._addStartBuildings(players)

    def getMaxWidthBoard(self):
        return 2 * self._countPlayers

    def getRowByDice(self, dice):
        return dice - (3 if dice >= 8 else 2)

    def buildBuilding(self, building, position):
        if building is None:
            return 'Error: building is empty'

        if building.getType() in ['house', 'small_totem', 'totem', 'workshop']:
            del self.buildings[building.getType()][building.getColor()]
        # elif building.getType() in ['church', 'government']:
        else:
            self.buildings[building.getType()].remove(building)

        size = building.getSize()

        for x in range(size[0]):
            for y in range(size[1]):
                if self.cells.get((position[0] + x, position[1] + y), None) is not None:
                    return 'Error: cells not free'

        for x in range(size[0]):
            for y in range(size[1]):
                self.cells[(position[0] + x, position[1] + y)] = {
                    'type': 'ref',
                    'position': position
                }

        self.cells[position] = {
            'type': 'building',
            'building': building
        }

    def destroyBuilding(self, position):
        cell = self.cells.get(position, None)

        if cell is None:
            return 'Cell is empty'
        elif cell['type'] == 'ref':
            cell = self.cells.get(cell['position'], None)

        if cell['type'] != 'building':
            return 'Cell is not a building'

        building = cell['building']
        if building.getType() in ['house', 'small_totem', 'totem', 'workshop']:
            self.buildings[building.getType()][building.getColor()] = building
        else:
            self.buildings[building.getType()].append(building)

        size = building.getSize()

        for x in range(size[0]):
            for y in range(size[1]):
                del self.cells[(position[0] + x, position[1] + y)]

    def putClaim(self, color, value, position):
        for c in self.claims[color]:
            if c['value'] == value:
                exists = True
                break

        if not exists:
            return 'Error: claim not found'

        if self.cells.get(position, None) is not None:
            return 'Cell in not empty'

        claim = self.claims[color].pop(value)
        self.cells[position] = {
            'type': 'claim',
            'claim': claim
        }

    def removeClaim(self, position):
        if self.cells.get(position, None) is None:
            return 'Cell is empty'

        cell = self.cells[position]
        if cell['type'] != 'claim':
            return 'Cell is not claim'

        claim = cell['claim']
        del self.cells[position]

        self.claims[claim['color']].insert(claim['value'], claim)

    def getRandomVote(self):
        votes = ['red', 'blue', 'green']
        return random.choice(votes)

    def _addCorners(self):
        index = self.getMaxWidthBoard()
        self.cells[(index, -1)] = {'type': 'corner'}
        self.cells[(index + 1, -1)] = {'type': 'corner'}
        self.cells[(index + 1, 0)] = {'type': 'corner'}

        self.cells[(index, 10)] = {'type': 'corner'}
        self.cells[(index + 1, 10)] = {'type': 'corner'}
        self.cells[(index + 1, 9)] = {'type': 'corner'}

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
            self.buildBuilding(self.buildings['totem'][player.getColor()], totem_position[player.getColor()])
            self.buildBuilding(self.buildings['small_totem'][player.getColor()], small_totem_position[player.getColor()])

    def _checkBoardSize(self, position):
        if position[0] < 0 or position[1] > self.getMaxWidthBoard():
            return False
