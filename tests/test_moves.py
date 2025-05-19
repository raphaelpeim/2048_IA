import unittest
from src.common.moves import compress, merge, move_left, move_right, move_up, move_down


class Test2048Moves(unittest.TestCase):

    # --- Compress tests ---
    def test_compress(self):
        self.assertEqual(compress([2, 0, 2, 4]), [2, 2, 4, 0])
        self.assertEqual(compress([0, 0, 2, 2]), [2, 2, 0, 0])
        self.assertEqual(compress([0, 2, 0, 2]), [2, 2, 0, 0])
        self.assertEqual(compress([0, 0, 0, 0]), [0, 0, 0, 0])

    # --- Merge tests ---
    def test_merge(self):
        self.assertEqual(merge([2, 2, 4, 0]), [4, 0, 4, 0])
        self.assertEqual(merge([2, 2, 2, 2]), [4, 0, 4, 0])
        self.assertEqual(merge([4, 4, 4, 4]), [8, 0, 8, 0])
        self.assertEqual(merge([2, 4, 8, 16]), [2, 4, 8, 16])
        self.assertEqual(merge([0, 0, 0, 0]), [0, 0, 0, 0])

    # --- Transpose tests ---
    def test_transpose(self):
        board = [
            [2, 2, 0, 0],
            [4, 0, 4, 0],
            [2, 2, 2, 2],
            [0, 0, 0, 0]
        ]
        expected = [
            [2, 4, 2, 0],
            [2, 0, 2, 0],
            [0, 4, 2, 0],
            [0, 0, 2, 0]
        ]
        self.assertEqual(transpose(board), expected)

    # --- Move left ---
    def test_move_left(self):
        board = [
            [2, 0, 2, 4],
            [0, 4, 4, 8],
            [2, 2, 0, 0],
            [0, 0, 0, 2]
        ]
        expected = [
            [4, 4, 0, 0],
            [8, 8, 0, 0],
            [4, 0, 0, 0],
            [2, 0, 0, 0]
        ]
        self.assertEqual(move_left(board), expected)

    # --- Move right ---
    def test_move_right(self):
        board = [
            [2, 0, 2, 4],
            [0, 4, 4, 8],
            [2, 2, 0, 0],
            [0, 0, 0, 2]
        ]
        expected = [
            [0, 0, 4, 4],
            [0, 0, 8, 8],
            [0, 0, 0, 4],
            [0, 0, 0, 2]
        ]
        self.assertEqual(move_right(board), expected)

    # --- Move up ---
    def test_move_up(self):
        board = [
            [2, 0, 2, 4],
            [2, 4, 0, 4],
            [0, 4, 2, 0],
            [2, 0, 2, 0]
        ]
        expected = [
            [4, 8, 4, 8],
            [2, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(move_up(board), expected)

    # --- Move down ---
    def test_move_down(self):
        board = [
            [2, 0, 2, 4],
            [2, 4, 0, 4],
            [0, 4, 2, 0],
            [2, 0, 2, 0]
        ]
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 2, 0],
            [4, 8, 4, 8]
        ]
        self.assertEqual(move_down(board), expected)

if __name__ == '__main__':
    unittest.main()
