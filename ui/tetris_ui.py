import pygame as py
from constants.tetris_constants import BACKGROUND_COLOR


class TetrisUI:
    def __init__(self, game):
        self.game = game
        self.screen = py.display.set_mode((700, 700))
        self.font = py.font.Font(None, 40)
        self.background = py.Surface((300, 600))
        self.background.fill(BACKGROUND_COLOR)

    def draw_screen(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.screen.blit(self.background, (200, 50))
        self.draw_game_elements()
        py.display.update()

    def draw_game_elements(self):
        # Render hold area, next pieces, grid, etc.
        pass
