class Player():

    def __init__(self, color):
        self.gold = 0
        self.votes = {'red': 0, 'blue': 0, 'green': 0}

        self.victoryPoint = 10
        self.mills = 0

        self._wall = 1
        self._color = color

    def getColor(self):
        return self._color

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
