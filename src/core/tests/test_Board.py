import unittest

from core.Board import Board
from core.Player import Player


class BoardTestCase(unittest.TestCase):

    def initialize_board(self):
        colors = ['red', 'blue', 'green', 'yellow']
        players = tuple(Player(c) for c in colors)
        return Board(colors, players)

    def test_createBoard_checkStartBuildings(self):
        board = self.initialize_board()
        tiles = board.cells
        self.assertEqual(tiles[(3, 2)]['type'], 'building')
        self.assertEqual(tiles[(4, 5)]['type'], 'building')
        self.assertEqual(tiles[(4, 6)]['type'], 'ref')
        self.assertEqual(len(board.buildings['totem']), 0)
        self.assertEqual(tiles[(3, 2)]['building'].getColor(), 'red')

    def test_buildBuilding(self):
        board = self.initialize_board()
        self.assertEqual(len(board.buildings['hotel']), 5)
        board.buildBuilding(board.buildings['hotel'][0], (5, 5))
        self.assertEqual(len(board.buildings['hotel']), 4)

        cell = board.cells[(5, 5)]
        self.assertEqual(cell['type'], 'building')
        self.assertEqual(cell['building'].getType(), 'hotel')

        cell = board.cells[(5, 6)]
        self.assertEqual(cell['type'], 'ref')
        self.assertTupleEqual(cell['position'], (5, 5))

        cell = board.cells[(6, 5)]
        self.assertEqual(cell['type'], 'ref')
        self.assertTupleEqual(cell['position'], (5, 5))

        cell = board.cells[(6, 6)]
        self.assertEqual(cell['type'], 'ref')
        self.assertTupleEqual(cell['position'], (5, 5))

        cell = board.cells.get((7, 6), None)
        self.assertIsNone(cell)

        cell = board.cells.get((6, 7), None)
        self.assertIsNone(cell)

    def test_destroyBuilding_onList(self):
        board = self.initialize_board()
        building = board.buildings['hotel'][0]
        board.buildBuilding(building, (5, 5))
        board.destroyBuilding((5, 5))

        for x in range(5, 8):
            for y in range(5, 8):
                cell = board.cells.get((x, y), 'empty')
                self.assertEqual(cell, 'empty')

    def test_destroyBuilding_onDict(self):
        board = self.initialize_board()
        building = board.buildings['house']['red']
        board.buildBuilding(building, (5, 5))
        board.destroyBuilding((5, 5))

        for x in range(5, 8):
            for y in range(5, 8):
                cell = board.cells.get((x, y), 'empty')
                self.assertEqual(cell, 'empty')

    def test_destroyBuilding_fromRef(self):
        board = self.initialize_board()
        building = board.buildings['house']['red']
        board.buildBuilding(building, (5, 5))
        board.destroyBuilding((5, 5))

        for x in range(5, 8):
            for y in range(5, 8):
                cell = board.cells.get((x, y), 'empty')
                self.assertEqual(cell, 'empty')

if __name__ == '__main__':
    unittest.main()
