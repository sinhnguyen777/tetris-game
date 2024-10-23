import pygame as py
from core import Game
from services import TetrisService
from ui import tetris_gui_ui  # Import UI mới

class TetrisApp:
    def __init__(self):
        py.init()
        self.game = Game()
        self.ui = tetris_gui_ui.TetrisUI(self.game)  # Khởi tạo UI mới
        self.service = TetrisService(self.game, self.ui)

    def run(self):
        clock = py.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0  # Tính thời gian giữa các khung hình

            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                if not self.ui.handle_events(event):
                    running = False

            self.ui.manager.update(time_delta)
            self.ui.draw_screen()

            if self.ui.state == 'playing':
                self.ui.draw_game_elements()
                self.service.handle_events()

if __name__ == "__main__":
    app = TetrisApp()
    app.run()
