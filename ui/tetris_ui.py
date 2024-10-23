import pygame as py
import pygame_gui
from constants.tetris_constants import BACKGROUND_COLOR


class TetrisUI:
    def __init__(self, game):

        self.title_font = py.font.Font(None, 40)

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
