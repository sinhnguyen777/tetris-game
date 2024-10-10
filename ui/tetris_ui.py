import tkinter as tk


class TetrisUI:
    def __init__(self, root, tetris_service):
        self.root = root
        self.canvas = tk.Canvas(root, width=300, height=600, bg="black")
        self.canvas.pack()

        self.tetris_service = tetris_service
        self.draw_grid()

    def draw_grid(self):
        for i in range(20):
            for j in range(10):
                self.canvas.create_rectangle(
                    j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, outline="white"
                )
