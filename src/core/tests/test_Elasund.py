import unittest

from core.Elasund import Elasund


class ElasundTestCase(unittest.TestCase):

    def test_build(self):
        colors = ('red', 'blue', 'green', 'yellow',)
        elasund = Elasund(colors)
        player = elasund.getCurrentPlayer()
        player.gold = 3

        error = elasund.claim((5, 5), 1)
        self.assertIsNone(error)
        error = elasund.claim((6, 6), 0)
        self.assertIsNone(error)

        buildings = elasund.getBuildings()
        self.assertEqual(len(buildings['hotel']), 5)

        error = elasund.build((5, 5), buildings['hotel'][0])
        self.assertIsNone(error)

        self.assertEqual(len(buildings['hotel']), 4)

    def test_createNewGame_stateOfEmptyPlayers(self):
        colors = ()
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'error')
        self.assertEqual(len(elasund.getPlayers()), 0)

    def test_createNewGame_stateOfOnePlayers(self):
        colors = ('red',)
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'error')
        self.assertEqual(len(elasund.getPlayers()), 0)

    def test_createNewGame_stateOfTwoPlayers(self):
        colors = ('red', 'blue',)
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'income')
        self.assertEqual(len(elasund.getPlayers()), 2)

    def test_createNewGame_stateOfThreePlayers(self):
        colors = ('red', 'blue', 'green',)
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'income')
        self.assertEqual(len(elasund.getPlayers()), 3)

    def test_createNewGame_stateOfFourPlayers(self):
        colors = ('red', 'blue', 'green', 'yellow',)
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'income')
        self.assertEqual(len(elasund.getPlayers()), 4)

    def test_createNewGame_stateOfFivePlayers(self):
        colors = ('red', 'blue', 'green', 'yellow', 'purple',)
        elasund = Elasund(colors)
        state = elasund.getState()
        self.assertEqual(state, 'error')
        self.assertEqual(len(elasund.getPlayers()), 0)

if __name__ == '__main__':
    unittest.main()
