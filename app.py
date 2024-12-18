import pygame as py
from core import Game
from services import TetrisService
from ui import TetrisUI
from constants import COUNTDOWN_TIMER


class TetrisApp:
    def __init__(self):
        py.init()
        self.game = Game()
        self.ui = TetrisUI(self.game)
        self.service = TetrisService(self.game, self.ui)
        self.is_countdown = False
        self.countdown_value = 3
        self.running = True
        self.game_started = False
        self.game_over = False

        # Cài đặt mặc định (sử dụng giá trị từ game ban đầu)
        self.das_value = self.game.das
        self.arr_value = self.game.arr
        self.soft_drop_speed = self.game.soft_drop_speed
        self.level = self.game.level
        self.current_input = ""  # Biến để lưu trữ đầu vào từ người dùng

    def run(self):
        clock = py.time.Clock()
        while self.running:
            if not self.game_started:
                self.ui.draw_start_screen()
                self.handle_start_screen_events()
            elif self.game_over:
                self.ui.draw_game_over_screen()
                self.handle_game_over_events()
            elif self.service.game_paused:
                self.ui.draw_pause_screen()
                self.handle_pause_events()
            else:
                self.ui.draw_screen()
                self.ui.draw_game_elements()
                if self.is_countdown:
                    self.ui.draw_countdown_screen(self.countdown_value)
                    self.handle_countdown()
                else:
                    self.service.handle_events()
                py.display.update()
                self.check_game_over()
            clock.tick(60)

    def handle_countdown(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            if event.type == COUNTDOWN_TIMER:
                self.countdown_value -= 1
                if self.countdown_value == 0:
                    self.is_countdown = False
                    self.countdown_value = 3
                    py.time.set_timer(COUNTDOWN_TIMER, 0)

    def handle_start_screen_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if self.ui.start_button.collidepoint(event.pos):
                    self.reset_game()
                    self.game_started = True
                    self.is_countdown = True
                    py.time.set_timer(COUNTDOWN_TIMER, 1000)
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
                    self.is_countdown = True
                    py.time.set_timer(COUNTDOWN_TIMER, 1000)
                elif self.ui.exit_button.collidepoint(event.pos):
                    self.running = False

    def handle_pause_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if self.ui.resume_button.collidepoint(event.pos):
                    self.service.game_paused = False
                    self.is_countdown = True
                    py.time.set_timer(COUNTDOWN_TIMER, 1000)
                elif self.ui.back_menu_button.collidepoint(event.pos):
                    self.game_started = False
                    self.game_over = False
                    self.service.game_paused = False

    def open_settings_screen(self):
        in_settings = True
        selected_option = 0  
        original_values = [self.das_value, self.arr_value, self.soft_drop_speed, self.level]

        while in_settings:
            self.ui.draw_settings_screen(
                self.das_value,
                self.arr_value,
                self.soft_drop_speed,
                self.level,
                selected_option,
                self.current_input,
            )
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                    in_settings = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.das_value, self.arr_value, self.soft_drop_speed, self.level = (
                            original_values
                        )
                        in_settings = False
                    elif event.key == py.K_DOWN:
                        if self.current_input:
                            self.current_input = "" 
                        selected_option = (selected_option + 1) % 4  # Cycle through 4 options
                    elif event.key == py.K_UP:
                        if self.current_input:
                            self.current_input = "" 
                        selected_option = (selected_option - 1) % 4  # Cycle through 4 options
                    elif event.key == py.K_BACKSPACE:
                        self.current_input = self.current_input[:-1]
                    elif event.key == py.K_RETURN:
                        if self.current_input.isdigit():
                            value = int(self.current_input)
                            if selected_option == 0:
                                self.das_value = value
                            elif selected_option == 1:
                                self.arr_value = value
                            elif selected_option == 2:
                                self.soft_drop_speed = value
                            elif selected_option == 3:  # Handle "Level" adjustment
                                if 1 <= value <= 15:  # Ensure the level is within bounds
                                    self.level = value
                            original_values = [
                                self.das_value,
                                self.arr_value,
                                self.soft_drop_speed,
                                self.level,
                            ]
                        self.current_input = ""
                    else:
                        if event.unicode.isdigit():
                            self.current_input += event.unicode
                elif event.type == py.MOUSEBUTTONDOWN:
                    if self.ui.save_button.collidepoint(event.pos):
                        self.game.update_settings(
                            self.das_value, self.arr_value, self.soft_drop_speed, self.level
                        )
                        in_settings = False
                    elif self.ui.back_button.collidepoint(event.pos):
                        self.das_value, self.arr_value, self.soft_drop_speed, self.level = (
                            original_values
                        )
                        in_settings = False


    def check_game_over(self):
        if self.game.game_over:
            self.game_over = True

    def reset_game(self):
        self.game = Game()
        self.game.update_settings(self.das_value, self.arr_value, self.soft_drop_speed, self.level)
        self.ui = TetrisUI(self.game)
        self.service = TetrisService(self.game, self.ui)
        self.game_over = False
        self.game_started = True


if __name__ == "__main__":
    app = TetrisApp()
    app.run()
