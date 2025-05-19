import tkinter as tk

from src.gui.gui import GameGUI


if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
