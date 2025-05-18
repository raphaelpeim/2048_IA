from src.direction import Direction
from src.game import Game2048
from src.moves import move_up, move_down, move_left, move_right
from src.utils import print_board, get_input, is_same_board


move_map = {
    Direction.UP: move_up,
    Direction.DOWN: move_down,
    Direction.LEFT: move_left,
    Direction.RIGHT: move_right
}

def main():
    game = Game2048()

    while True:
        print_board(game.board)

        direction = get_input()

        if direction == 'quit':
            break

        move_function = move_map.get(direction)

        if move_function:
            new_board = move_function(game.board)

            if not is_same_board(new_board, game.board):
                game.board = new_board
                game.add_tile()

            if game.is_won():
                print_board(game.board)
                print("🎉 You win!")
                break
            elif not game.can_move():
                print_board(game.board)
                print("💀 Game over!")
                break

if __name__ == "__main__":
    main()
