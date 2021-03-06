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

    def getCountCubeByRow(self):
        dice = self.shipPosition
        buildings = {}
        y = self.getRowByDice(dice)
        for x in range(self.getMaxWidthBoard() + 1):
            cell = self.cells.get((x, y,), None)
            if cell is not None:
                building = cell
                position = (x, y,)
                if cell['type'] == 'ref':
                    position = cell['position']
                    building = self.cells[position]
                if building['type'] == 'building':
                    buildings[position] = building

        result = {}
        for position, building in buildings.items():
            color = building.getColor()
            if color not in result:
                result[color] = 0
            result[color] += building.getCubesByLine(y - position[1])

    def getCountCubeOnWallByPlayer(self, color):
        count = 0

        def getCountCubeByPosition(position, color):
            cell = self.cells.get(position, None)
            if (cell is not None) and (cell['type'] == 'wall'):
                if cell['color'] == color and cell['value'] % 3 == 0:
                    return 1
            return 0

        ''' Top '''
        for x in range(2, 7 + 1):
            count += getCountCubeByPosition((x, -1,), color)
        ''' Right '''

        for y in range(1, 8 + 1):
            count += getCountCubeByPosition((self.getMaxWidthBoard() + 1, y), color)
        ''' Bottom '''
        for x in range(2, 7 + 1):
            count += getCountCubeByPosition((x, 10,), color)

        return count

    def buildBuilding(self, building, position):
        if building is None:
            return 'Error: building is empty'

        if not self._checkAreaByBoardSize(position, building.getSize()):
            return 'Error: out of range of board'

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
        if not self._checkBoardSize(position):
            return 'Error: out of range of board'

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

    def buildWall(self, position, value, color):
        error_msg = 'Error: position is wrong'
        if position[0] >= 2 and position[0] < (2 * self._countPlayers):
            if position[1] == -1:
                type = 'top'
            elif position[1] == 10:
                type = 'bottom'
            else:
                return error_msg
        elif position[0] == (1 + 2 * self._countPlayers) and position[1] >= 1 and position[1] <= 8:
            type = 'right'
        else:
            return error_msg

        current_cell_wall = self.cells.get(position, None)
        if current_cell_wall is not None:
            return 'Error: current position is not empty'

        error_is_None = 'Error: previous cell is empty'
        if type == 'top' or type == 'bottom':
            prev = self.cells.get((position[0] - 1, position[1]), None)
            if prev is None:
                return error_is_None
        elif type == 'right':
            prev_up = self.cells.get((position[0], position[1] - 1), None)
            if prev_up is None:
                return error_is_None
            prev_down = self.cells.get((position[0], position[1] + 1), None)
            if prev_down is None:
                return error_is_None

        self.cells[position] = {'type': 'wall', 'color': color, 'value': value}

    def getWallCost(self, position):
        if position[0] >= 2 and position[0] < (2 * self._countPlayers):
            if position[1] == -1 or position[1] == 10:
                return 2
        elif position[0] == (1 + 2 * self._countPlayers) and position[1] >= 1 and position[1] <= 8:
            return 4
        return -1

    def putClaim(self, color, value, position):
        if not self._checkBoardSize(position):
            return 'Error: out of range of board'

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
        if not self._checkBoardSize(position):
            return 'Error: out of range of board'

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

    def getCountMills(self, position):
        if not self._checkBoardSize(position):
            return 0
        x, y = position
        if x == 0 and y >= 0 and y <= 9:
            return 1
        if x == 5 and (y == 0 or y == 9):
            return 2
        if x == 7 and (y == 0 or y == 9):
            return 2
        return 0

    def getCubesByMills(self, mills):
        count = 0
        if mills >= 3:
            count += 1
        if mills >= 5:
            count += 1
        if mills >= 7:
            count += 1
        if mills >= 9:
            count += 1
        if mills >= 11:
            count += 1
        return count

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
        x, y = position
        if x < 0 or x > self.getMaxWidthBoard():
            return False
        if y < 0 or y > 9:
            return False
        return True

    def _checkAreaByBoardSize(self, position, size):
        for x in range(position[0], position[0] + size[0] + 1):
            for y in range(position[1], position[1] + size[1] + 1):
                if not self._checkBoardSize((x, y,)):
                    return False
        return True
