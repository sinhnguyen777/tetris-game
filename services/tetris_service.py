import pygame as py
from constants import GAME_UPDATE, SOFT_DROP


class TetrisService:
    def __init__(self, game):
        self.game = game
        self.ev_game_update_running = True

    def handle_events(self):
        for ev in py.event.get():
            if ev.type == py.QUIT:
                py.quit()
                exit()
            elif ev.type == py.KEYDOWN:
                if ev.key == py.K_LEFT:
                    self.game.move_left()
                elif ev.key == py.K_RIGHT:
                    self.game.move_right()
                elif ev.key == py.K_DOWN:
                    self.ev_game_update_running = False
                    self.game.move_down()
                elif ev.key == py.K_SPACE:
                    self.game.hard_drop()
            elif ev.type == GAME_UPDATE:
                if self.ev_game_update_running:
                    self.game.move_down()

    def update_game_state(self):
        pass  # Logic to update the game state, e.g., check for game over or line clear
