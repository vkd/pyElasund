import unittest
from core.Elasund import Elasund


class ElasundTestCase(unittest.TestCase):

    def test_create_new_game(self):
        """Create game instance with difference players"""
        self.assertTupleEqual(Elasund('red', 'blue'), ('red', 'blue'))

if __name__ == '__main__':
    unittest.main()
