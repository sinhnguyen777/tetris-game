from core import Game
from services import TetrisService
from ui import TetrisUI
import pygame


class TetrisApp:
    def __init__(self):
        pygame.init()
        self.game = Game()
        self.ui = TetrisUI(self.game)
        self.service = TetrisService(self.game)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.service.handle_events()
            self.service.update_game_state()
            self.ui.draw_screen()
            clock.tick(60)


if __name__ == "__main__":
    app = TetrisApp()
    app.run()
