import pygame as py
from constants.tetris_constants import BACKGROUND_COLOR

class TetrisUI:
    def __init__(self, game):
        self.title_font = py.font.Font(None, 40)
        self.large_font = py.font.Font(None, 80)

        self.hold_surf = self.title_font.render("Hold", True, (255, 255, 255))
        self.hold_rect = py.Rect(10, 55, 170, 170)
        self.lines_clear_surf = self.title_font.render(
            "Lines Clear", True, (255, 255, 255)
        )
        self.lines_clear_rect = py.Rect(520, 55, 170, 60)
        self.next_surf = self.title_font.render("Next", True, (255, 255, 255))
        self.next_rect = py.Rect(520, 165, 170, 485)

        py.display.set_caption("Tetris")
        self.screen = py.display.set_mode((700, 700))

        self.background_surf = py.Surface((300, 600))
        self.background_surf.fill((26, 31, 40))
        self.draw_surf = py.Surface((700, 700))
        self.draw_surf.fill(py.Color("#C77DFF"))
        self.draw_surf2 = py.Surface((300, 600), py.SRCALPHA)
        self.draw_surf2.fill(py.Color("#505050"))
        self.game = game

        self.start_button = py.Rect(200, 300, 300, 50)
        self.exit_button = py.Rect(200, 500, 300, 50)
        self.settings_button = py.Rect(200, 400, 300, 50)
        self.save_button = py.Rect(200, 500, 300, 50)
        self.back_button = py.Rect(200, 600, 300, 50)

    def draw_screen(self):
        self.screen.blit(self.draw_surf, (0, 0))
        self.screen.blit(self.background_surf, (200, 50))
        self.screen.blit(self.draw_surf2, (200, 50))

        # Hold section
        self.screen.blit(
            self.hold_surf,
            self.hold_surf.get_rect(
                centerx=self.hold_rect.centerx,
                centery=self.hold_rect.centery
                - self.hold_rect.size[1] / 2
                - self.hold_surf.get_height() / 2,
            ),
        )
        py.draw.rect(self.draw_surf, "#aa77d1", self.hold_rect, 0, 10)
        self.game.draw_hold_tetromino(self.draw_surf)

        # Lines cleared section
        py.draw.rect(self.draw_surf, "#aa77d1", self.lines_clear_rect, 0, 10)
        line_clears_value = self.title_font.render(
            str(self.game.line_clears), True, (255, 255, 255)
        )
        self.screen.blit(
            line_clears_value,
            line_clears_value.get_rect(
                centerx=self.lines_clear_rect.centerx,
                centery=self.lines_clear_rect.centery,
            ),
        )

        # Next section
        self.screen.blit(
            self.next_surf,
            self.next_surf.get_rect(
                centerx=self.next_rect.centerx,
                centery=self.next_rect.centery
                - self.next_rect.size[1] / 2
                - self.next_surf.get_height() / 2,
            ),
        )
        py.draw.rect(self.draw_surf, "#aa77d1", self.next_rect, 0, 10)
        self.game.draw_current_queue(self.draw_surf)

        py.display.update()

    def draw_game_elements(self):
        self.game.draw(self.draw_surf2) 
        py.display.update()

    def draw_button(self, text, rect, color):
        py.draw.rect(self.screen, color, rect, 0, 5)
        button_text = self.title_font.render(text, True, (255, 255, 255))
        self.screen.blit(
            button_text,
            button_text.get_rect(center=(rect.centerx, rect.centery))
        )
        return rect

    def draw_start_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        py.draw.rect(self.screen, (0, 128, 255), self.start_button)
        py.draw.rect(self.screen, (0, 128, 255), self.exit_button)
        py.draw.rect(self.screen, (0, 128, 255), self.settings_button)

        start_text = self.title_font.render("Start Game", True, (255, 255, 255))
        self.screen.blit(start_text, start_text.get_rect(center=self.start_button.center))
        
        exit_text = self.title_font.render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, exit_text.get_rect(center=self.exit_button.center))
        
        settings_text = self.title_font.render("Settings", True, (255, 255, 255))
        self.screen.blit(settings_text, settings_text.get_rect(center=self.settings_button.center))
        py.display.flip()

    def draw_settings_screen(self, das_value, arr_value, soft_drop_speed, selected_option, current_input):
        self.screen.fill(BACKGROUND_COLOR)
        options = ["DAS", "ARR", "Soft Drop Speed"]
        values = [das_value, arr_value, soft_drop_speed]

        for i, option in enumerate(options):
            if i == selected_option and current_input:
                display_value = current_input
            else:
                display_value = str(values[i])
            
            color = (255, 0, 0) if i == selected_option else (255, 255, 255)
            option_text = self.title_font.render(f"{option}: {display_value}", True, color)
            self.screen.blit(option_text, (200, 200 + i * 100))

        py.draw.rect(self.screen, (0, 128, 0), self.save_button)
        py.draw.rect(self.screen, (128, 0, 0), self.back_button)

        save_text = self.title_font.render("Save", True, (255, 255, 255))
        self.screen.blit(save_text, save_text.get_rect(center=self.save_button.center))
        back_text = self.title_font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        py.display.flip()



    def draw_game_over_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        game_over_surf = self.large_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(
            game_over_surf,
            game_over_surf.get_rect(center=(self.screen.get_width() // 2, 200))
        )

        restart_button_rect = py.Rect(250, 350, 200, 50)
        exit_button_rect = py.Rect(250, 420, 200, 50)
        self.restart_button = self.draw_button("Restart", restart_button_rect, "#4CAF50")
        self.exit_button = self.draw_button("Exit", exit_button_rect, "#F44336")

        py.display.update()