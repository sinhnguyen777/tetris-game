import tkinter as tk
from services.tetris_service import *
from ui.tetris_ui import *


if __name__ == "__main__":
    root = tk.Tk()
    tetris_service = TetrisService()
    ui = TetrisUI(root, tetris_service)

    root.mainloop()
