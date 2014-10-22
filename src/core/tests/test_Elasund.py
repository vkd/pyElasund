import unittest

from core.Elasund import Elasund


class ElasundTestCase(unittest.TestCase):

    def test_create_new_game(self):
        """Create game instance with difference players"""
        colors = ('red', 'blue')
        elasund = Elasund(colors)
        first_player = elasund.getPlayers()[0]
        print('%s' % first_player.getColor())
        self.assertEqual(first_player.getColor(), colors[0])

if __name__ == '__main__':
    unittest.main()
