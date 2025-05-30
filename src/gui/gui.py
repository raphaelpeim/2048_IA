import tkinter as tk

from src.ai.q_learning import QLearningAgent
from src.core.bot import get_best_move
from src.core.game import Game2048
from src.common.utils import is_same_board, simulate_move, get_valid_moves, serialize_board
from src.common.constants import BOARD_SIZE, COLORS, KEYBOARD_ARROW_DIRECTIONS


class GameGUI:

    def __init__(self, root):
        # Board
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
        # User
        self.root.bind("<Key>", self.key_handler)
        # Bot
        self.bot_enabled = False
        self.root.bind("b", self.toggle_bot)
        # AI
        self.ai_enabled = False
        self.root.bind("a", self.toggle_ai)
        self.q_agent = QLearningAgent()

    def key_handler(self, event):
        if self.ai_enabled or self.bot_enabled:
            return

        move = event.keysym
        original = [row[:] for row in self.game.board]

        self.game.board = simulate_move(self.game.board, KEYBOARD_ARROW_DIRECTIONS[move])

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
        self.bot_enabled = False
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.root.after(100, self.ai_loop)

    def toggle_bot(self, event=None):
        self.ai_enabled = False
        self.bot_enabled = not self.bot_enabled
        if self.bot_enabled:
            self.root.after(100, self.bot_loop)

    def ai_loop(self):
        if not self.ai_enabled:
            return

        state = serialize_board(self.game.board)
        valid = get_valid_moves(self.game.board)
        move = self.q_agent.get_move(state, valid)

        original = [row[:] for row in self.game.board]

        self.game.board = simulate_move(self.game.board, move)

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

    def bot_loop(self):
        if not self.bot_enabled:
            return

        move = get_best_move(self.game.board)
        original = [row[:] for row in self.game.board]

        self.game.board = simulate_move(self.game.board, move)

        if not is_same_board(self.game.board, original):
            self.game.add_tile()

        self.update_board()

        if self.game.is_won():
            self.show_message("AI wins!")
            self.bot_enabled = False
        elif not self.game.can_move():
            self.show_message("AI lost!")
            self.bot_enabled = False
        else:
            self.root.after(150, self.bot_loop)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()