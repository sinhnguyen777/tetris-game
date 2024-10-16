import unittest
from core import Grid
from core import Pieces
from core import GameLogic


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()
        self.piece = Pieces()
        self.logic = GameLogic(self.grid)

    def test_move_piece(self):
        initial_x = self.piece.x
        self.logic.move_piece(self.piece, "left")
        self.assertEqual(self.piece.x, initial_x - 1)


if __name__ == "__main__":
    unittest.main()
