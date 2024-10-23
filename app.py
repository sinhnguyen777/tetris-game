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
        self.running = True
        self.game_started = False
        self.game_over = False

        self.das_value = self.game.das
        self.arr_value = self.game.arr
        self.soft_drop_speed = self.game.soft_drop_speed

    def run(self):
        clock = py.time.Clock()
        while self.running:
            if not self.game_started:
                self.ui.draw_start_screen()
                self.handle_start_screen_events()
            elif self.game_over:
                self.ui.draw_game_over_screen()
                self.handle_game_over_events()
            else:
                self.ui.draw_screen()
                self.ui.draw_game_elements()
                self.service.handle_events()
                self.check_game_over()
            clock.tick(60)

    def handle_start_screen_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if self.ui.start_button.collidepoint(event.pos):
                    self.game_started = True
                elif self.ui.exit_button.collidepoint(event.pos):
                    self.running = False
                elif self.ui.settings_button.collidepoint(event.pos):
                    self.open_settings_screen()

    def handle_game_over_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if self.ui.restart_button.collidepoint(event.pos):
                    self.reset_game()
                elif self.ui.exit_button.collidepoint(event.pos):
                    self.running = False

    def open_settings_screen(self):
        in_settings = True
        selected_option = 0  # 0 = DAS, 1 = ARR, 2 = Soft Drop Speed

        while in_settings:
            self.ui.draw_settings_screen(self.das_value, self.arr_value, self.soft_drop_speed, selected_option)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                    in_settings = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        in_settings = False
                    elif event.key == py.K_DOWN:
                        selected_option = (selected_option + 1) % 3
                    elif event.key == py.K_UP:
                        selected_option = (selected_option - 1) % 3
                    elif event.key == py.K_LEFT:
                        if selected_option == 0:
                            self.das_value = max(0, self.das_value - 1)
                        elif selected_option == 1:
                            self.arr_value = max(0, self.arr_value - 1)
                        elif selected_option == 2:
                            self.soft_drop_speed = max(1, self.soft_drop_speed - 1)
                    elif event.key == py.K_RIGHT:
                        if selected_option == 0:
                            self.das_value += 1
                        elif selected_option == 1:
                            self.arr_value += 1
                        elif selected_option == 2:
                            self.soft_drop_speed += 1
                elif event.type == py.MOUSEBUTTONDOWN:
                    if self.ui.save_button.collidepoint(event.pos):
                        # Cập nhật giá trị trong game và quay lại màn hình chính
                        self.game.update_settings(self.das_value, self.arr_value, self.soft_drop_speed)
                        in_settings = False
                    elif self.ui.back_button.collidepoint(event.pos):
                        in_settings = False

    def check_game_over(self):
        if self.game.is_game_over():
            self.game_over = True

    def reset_game(self):
        self.game = Game()
        self.ui = TetrisUI(self.game)
        self.service = TetrisService(self.game, self.ui)
        self.game_over = False
        self.game_started = True

if __name__ == "__main__":
    app = TetrisApp()
    app.run()
