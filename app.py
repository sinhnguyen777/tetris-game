import tkinter as tk
from services.tetris_service import TetrisService


class MainApp:
    def __init__(self, root, tetris_service):

        self.root = root
        self.root.title("Tetris Game v1.0.0")

        # Tạo khung cho lưới game
        self.canvas = tk.Canvas(root, width=300, height=600, bg="black")
        self.canvas = tk.Pack

        # Tạo nút điều khiển
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_game)
        self.pause_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(side=tk.LEFT)

        self.tetris_service = tetris_service

    def start_game(self):
        self.tetris_service.start_game()

    def pause_game(self):
        self.tetris_service.pause_game()


if __name__ == "__main__":
    root = tk.Tk()
    tetris_service = TetrisService()
    main_app = MainApp(root, tetris_service)
    root.mainloop()
