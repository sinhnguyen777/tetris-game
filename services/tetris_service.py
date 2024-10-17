import repository as rp
from core.grid import Grid
from core.tetromino import Pieces
from core.game_logic import GameLogic
from ui.tetris_ui import TetrisUI


class TetrisService:
    def __init__(self):
        self.ui = TetrisUI()
        self.grid = Grid()
        self.logic = GameLogic(self.grid)

    def start_game(self):
        while self.ui.running:
            self.ui.handle_events()
            # Logic game loop
            self.ui.draw_grid(self.grid)
            self.ui.clock.tick(30)
        self.ui.quit()

    def update_game(self):
        pass

    def render(self, screen):
        pass
