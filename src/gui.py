import tkinter as tk
from src.game import Game2048
from src.moves import move_up, move_down, move_left, move_right
from src.utils import is_same_board
from src.constants import BOARD_SIZE


CELL_COLORS = {
    0: "#ccc0b3",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

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

    def key_handler(self, event):
        key = event.keysym
        original = [row[:] for row in self.game.board]

        if key == "Up":
            self.game.board = move_up(self.game.board)
        elif key == "Down":
            self.game.board = move_down(self.game.board)
        elif key == "Left":
            self.game.board = move_left(self.game.board)
        elif key == "Right":
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
                label.config(text=str(value) if value else "", bg=CELL_COLORS.get(value, "#3c3a32"))

    def show_message(self, msg):
        top = tk.Toplevel()
        top.title("2048")
        tk.Label(top, text=msg, font=("Helvetica", 20)).pack(padx=20, pady=20)
        tk.Button(top, text="Close", command=self.root.quit).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
