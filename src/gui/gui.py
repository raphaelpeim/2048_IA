import tkinter as tk

from src.core.ai import get_best_move
from src.common.direction import Direction
from src.core.game import Game2048
from src.common.moves import move_up, move_down, move_left, move_right
from src.common.utils import is_same_board
from src.common.constants import BOARD_SIZE, COLORS


class GameGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.game = Game2048()
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.frame = tk.Frame(self.root, bg="#bbada0", padx=10, pady=10)
        self.frame.pack()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                label = tk.Label(self.frame, text='', width=4, height=2, font=("Helvetica", 32, "bold"), bg="#ccc0b3")
                label.grid(row=i, column=j, padx=5, pady=5)
                self.grid[i][j] = label
        self.update_board()
        self.root.bind("<Key>", self.key_handler)
        self.ai_enabled = False
        self.root.bind("a", self.toggle_ai)

    def key_handler(self, event):
        key = event.keysym
        original = [row[:] for row in self.game.board]

        if key == Direction.UP:
            self.game.board = move_up(self.game.board)
        elif key == Direction.DOWN:
            self.game.board = move_down(self.game.board)
        elif key == Direction.LEFT:
            self.game.board = move_left(self.game.board)
        elif key == Direction.RIGHT:
            self.game.board = move_right(self.game.board)
        else:
            return

        if not is_same_board(self.game.board, original):
            self.game.add_tile()

        self.update_board()

        if self.game.is_won():
            self.show_message("You win!")
        elif not self.game.can_move():
            self.show_message("Game over!")

    def update_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                value = self.game.board[i][j]
                label = self.grid[i][j]
                label.config(text=str(value) if value else "", bg=COLORS.get(value, "#3c3a32"))

    def show_message(self, msg):
        top = tk.Toplevel()
        top.title("2048")
        tk.Label(top, text=msg, font=("Helvetica", 20)).pack(padx=20, pady=20)
        tk.Button(top, text="Close", command=self.root.quit).pack(pady=10)

    def toggle_ai(self, event=None):
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.root.after(100, self.ai_loop)

    def ai_loop(self):
        if not self.ai_enabled:
            return

        move = get_best_move(self.game.board)
        original = [row[:] for row in self.game.board]

        if move == Direction.UP:
            self.game.board = move_up(self.game.board)
        elif move == Direction.DOWN:
            self.game.board = move_down(self.game.board)
        elif move == Direction.LEFT:
            self.game.board = move_left(self.game.board)
        elif move == Direction.RIGHT:
            self.game.board = move_right(self.game.board)

        if not is_same_board(self.game.board, original):
            self.game.add_tile()

        self.update_board()

        if self.game.is_won():
            self.show_message("AI wins!")
            self.ai_enabled = False
        elif not self.game.can_move():
            self.show_message("AI lost!")
            self.ai_enabled = False
        else:
            self.root.after(150, self.ai_loop)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
