import unittest

from core.Board import Board
from core.Player import Player


class BoardTestCase(unittest.TestCase):

    def test_createBoard_checkStartBuildings(self):
        colors = ['red', 'blue', 'green', 'yellow']
        players = tuple(Player(c) for c in colors)
        board = Board(colors, players)
        tiles = board.tiles
        self.assertEqual(tiles[(3, 2)][0], 'building')
        self.assertEqual(tiles[(4, 5)][0], 'building')
        self.assertEqual(tiles[(4, 6)][0], 'ref')
        self.assertEqual(len(board.buildings['totem']), 0)
        self.assertEqual(tiles[(3, 2)][1].getColor(), 'red')

if __name__ == '__main__':
    unittest.main()
