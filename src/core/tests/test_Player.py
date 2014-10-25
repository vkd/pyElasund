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

if __name__ == '__main__':
    unittest.main()
