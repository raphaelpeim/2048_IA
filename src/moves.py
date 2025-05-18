def compress(row):
    """Slide all non-zero tiles to the left."""
    new_row = [num for num in row if num != 0]
    new_row += [0] * (len(row) - len(new_row))
    return new_row

def merge(row):
    """Merge adjacent equal tiles and double their value."""
    for i in range(len(row) - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def compress_and_merge_row(row):
    row = compress(row)
    row = merge(row)
    row = compress(row)
    return row

def transpose(board):
    return [list(row) for row in zip(*board)]

def reverse(board):
    return [row[::-1] for row in board]

def move_left(board):
    return [compress_and_merge_row(row) for row in board]

def move_right(board):
    reversed_board = reverse(board)
    moved = [compress_and_merge_row(row) for row in reversed_board]
    return reverse(moved)

def move_up(board):
    transposed = transpose(board)
    moved = [compress_and_merge_row(row) for row in transposed]
    return transpose(moved)

def move_down(board):
    transposed = transpose(board)
    reversed_transposed = reverse(transposed)
    moved = [compress_and_merge_row(row) for row in reversed_transposed]
    return transpose(reverse(moved))
