import pygame as py
import pygame_gui
from constants.tetris_constants import BACKGROUND_COLOR

class TetrisUI:
    def __init__(self, game):
        self.game = game
        self.manager = pygame_gui.UIManager((700, 700))  # Kích thước khớp với màn hình
        self.screen = py.display.set_mode((700, 700))
        py.display.set_caption("Trò chơi Tetris")

        # Định nghĩa trạng thái
        self.state = 'start'

        # Khởi tạo các phần tử UI
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=py.Rect((250, 250), (200, 50)),
            text='Bắt đầu trò chơi',
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=py.Rect((250, 320), (200, 50)),
            text='Thoát',
            manager=self.manager
        )
        self.play_again_button = None

        # Khởi tạo các surface cho các phần tử đồ họa
        self.title_font = py.font.Font(None, 40)
        self.background_surf = py.Surface((300, 600))
        self.background_surf.fill(BACKGROUND_COLOR)
        self.draw_surf = py.Surface((700, 700))
        self.draw_surf.fill(py.Color("#C77DFF"))
        self.draw_surf2 = py.Surface((300, 600), py.SRCALPHA)
        self.draw_surf2.fill(py.Color("#505050"))

        self.hold_surf = self.title_font.render("Hold", True, (255, 255, 255))
        self.hold_rect = py.Rect(10, 55, 170, 170)
        self.lines_clear_surf = self.title_font.render("Lines Clear", True, (255, 255, 255))
        self.lines_clear_rect = py.Rect(520, 55, 170, 60)

    def setup_game_over_screen(self):
        if self.play_again_button is None:
            self.play_again_button = pygame_gui.elements.UIButton(
                relative_rect=py.Rect((250, 250), (200, 50)),
                text='Chơi lại',
                manager=self.manager
            )
        # Reuse the exit button since it already exists
        self.exit_button.show()

    def draw_screen(self):
        self.screen.fill((0, 0, 0))  # Tô đen màn hình

        if self.state == 'start':
            self.start_button.show()
            self.exit_button.show()
        elif self.state == 'game_over':
            self.setup_game_over_screen()
            self.play_again_button.show()

        # Vẽ các phần tử đồ họa từ trò chơi
        self.screen.blit(self.draw_surf, (0, 0))
        self.screen.blit(self.background_surf, (200, 50))
        self.screen.blit(self.draw_surf2, (200, 50))

        # Vẽ khu vực "Hold"
        self.screen.blit(
            self.hold_surf,
            self.hold_surf.get_rect(
                centerx=self.hold_rect.centerx,
                centery=self.hold_rect.centery
            ),
        )
        py.draw.rect(self.screen, "#aa77d1", self.hold_rect, 0, 10)
        self.game.draw_hold_tetromino(self.screen)

        # Vẽ khu vực "Lines Cleared"
        py.draw.rect(self.screen, "#aa77d1", self.lines_clear_rect, 0, 10)
        line_clears_value = self.title_font.render(str(self.game.line_clears), True, (255, 255, 255))
        self.screen.blit(line_clears_value, self.lines_clear_rect.move(10, 10))

        # Cập nhật và vẽ các phần tử UI
        self.manager.draw_ui(self.screen)
        py.display.flip()

    def draw_game_elements(self):
        # Vẽ các thành phần của trò chơi
        self.screen.fill((0, 0, 0))
        py.draw.rect(self.screen, (150, 150, 150), (200, 50, 300, 600), 2)
        # Vẽ thêm các thành phần trò chơi (ví dụ: lưới, khối tetromino, v.v.)

    def handle_events(self, event):
        if event.type == py.QUIT:
            return False
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.state = 'playing'
                self.start_button.hide()
                self.exit_button.hide()
            elif event.ui_element == self.play_again_button:
                self.state = 'playing'
                self.play_again_button.hide()
                self.exit_button.hide()
            elif event.ui_element == self.exit_button:
                return False

        return True
