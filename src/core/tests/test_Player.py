import unittest

from core.Player import Player


class PlayerTestCase(unittest.TestCase):

    def test_createNewPlayer_checkInitStatus(self):
        start_color = 'red'
        player = Player(start_color)
        color = player.getColor()
        self.assertEqual(color, start_color)
        vp = player.getVictoryPoint()
        self.assertEqual(vp, 10)
        mills = player.getMills()
        self.assertEqual(mills, 0)

    def test_playersWalls(self):
        player = Player('red')

        types = ['vote', 'vote', 'point', 'vote', 'vote', 'point', 'vote', 'vote', 'point', 'none', 'none']
        counts = [1, 1, 0, 1, 2, 0, 2, 2, 0, 0, 0]
        for i in range(len(types)):
            wall = player.getWall()
            self.assertEqual(wall['type'], types[i])
            self.assertEqual(wall['count'], counts[i])

if __name__ == '__main__':
    unittest.main()
