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
        self.assertEqual(tiles[(3, 2)][0], 'building')
        self.assertEqual(tiles[(4, 5)][0], 'building')
        self.assertEqual(tiles[(4, 6)][0], 'ref')
        self.assertEqual(len(board.buildings['totem']), 0)
        self.assertEqual(tiles[(3, 2)][1].getColor(), 'red')

    def test_buildBuilding(self):
        board = self.initialize_board()
        self.assertEqual(len(board.buildings['hotel']), 5)
        board.buildBuilding(board.buildings['hotel'][0], (5, 5))
        self.assertEqual(len(board.buildings['hotel']), 4)

        cell = board.cells[(5, 5)]
        self.assertEqual(cell[0], 'building')
        self.assertEqual(cell[1].getType(), 'hotel')

        cell = board.cells[(5, 6)]
        self.assertEqual(cell[0], 'ref')
        self.assertTupleEqual(cell[1], (5, 5))

        cell = board.cells[(6, 5)]
        self.assertEqual(cell[0], 'ref')
        self.assertTupleEqual(cell[1], (5, 5))

        cell = board.cells[(6, 6)]
        self.assertEqual(cell[0], 'ref')
        self.assertTupleEqual(cell[1], (5, 5))

        cell = board.cells.get((7, 6), 'empty')
        self.assertEqual(cell, 'empty')

        cell = board.cells.get((6, 7), 'empty')
        self.assertEqual(cell, 'empty')

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
