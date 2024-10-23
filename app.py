import pygame as py
from core import Game
from services import TetrisService
from ui import TetrisUI


class TetrisApp:
    def __init__(self):
        py.init()
        self.game = Game()
        self.ui = TetrisUI(self.game)
        self.service = TetrisService(self.game, self.ui)

    def run(self):
        clock = py.time.Clock()
        while True:
            self.ui.draw_screen()
            self.ui.draw_game_elements()
            self.service.handle_events()
            clock.tick(60)


if __name__ == "__main__":
    app = TetrisApp()
    app.run()
