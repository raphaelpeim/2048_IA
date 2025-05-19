import unittest

from src.common.constants import BOARD_SIZE
from src.core.game import Game2048


class TestGame(unittest.TestCase):
    # --- Add tile tests ---
    def test_add_tile(self):
        game = Game2048()
        game.add_tile()
        count = sum(tile in (2, 4) for row in game.board for tile in row)
        self.assertEqual(count, 3)

    def test_add_tile_on_almost_full_board(self):
        game = Game2048()

        # Fill the board with 2s
        game.board = [[2 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Leave one cell empty
        game.board[BOARD_SIZE - 1][BOARD_SIZE - 1] = 0

        # Check there is exactly one empty cell before
        empty_before = sum(tile == 0 for row in game.board for tile in row)
        self.assertEqual(empty_before, 1)

        # Add a tile
        game.add_tile()

        # Check there are now zero empty cells
        empty_after = sum(tile == 0 for row in game.board for tile in row)
        self.assertEqual(empty_after, 0)

        # Check the newly added tile is 2 or 4
        added_tile = game.board[3][3]
        self.assertIn(added_tile, (2, 4))

    # --- Is won tests ---
    def test_is_won_false(self):
        game = Game2048()
        game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertFalse(game.is_won())

    def test_is_won_true(self):
        game = Game2048()
        game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 0],
            [0, 0, 0, 0]
        ]
        self.assertTrue(game.is_won())

    # --- Can move tests ---
    def test_can_move_with_empty_tiles(self):
        game = Game2048()
        game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 0],
            [512, 1024, 256, 512],
            [2, 4, 8, 16]
        ]
        self.assertTrue(game.can_move())

    def test_can_move_with_merge_possible(self):
        game = Game2048()
        game.board = [
            [2, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 2],
            [4, 8, 16, 32]
        ]
        self.assertTrue(game.can_move())

    def test_cannot_move(self):
        game = Game2048()
        game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [8, 16, 32, 64]
        ]
        self.assertFalse(game.can_move())

    if __name__ == '__main__':
        unittest.main()
