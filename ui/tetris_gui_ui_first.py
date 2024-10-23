import pygame as py
import pygame_gui

class TetrisUI:
    def __init__(self, game):
        self.game = game
        self.manager = pygame_gui.UIManager((800, 600))
        self.screen = py.display.set_mode((800, 600))
        py.display.set_caption("Tetris")

        self.state = 'start'

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=py.Rect((300, 250), (200, 50)),
            text='Bắt đầu',
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=py.Rect((300, 320), (200, 50)),
            text='Thoát',
            manager=self.manager
        )
        self.play_again_button = None

    def setup_game_over_screen(self):
        if self.play_again_button is None:
            self.play_again_button = pygame_gui.elements.UIButton(
                relative_rect=py.Rect((300, 250), (200, 50)),
                text='Chơi lại',
                manager=self.manager
            )
        if self.exit_button is None:
            self.exit_button = pygame_gui.elements.UIButton(
                relative_rect=py.Rect((300, 320), (200, 50)),
                text='Thoát',
                manager=self.manager
            )

    def draw_screen(self):
        self.screen.fill((0, 0, 0))

        if self.state == 'start':
            self.start_button.show()
            self.exit_button.show()
        elif self.state == 'game_over':
            self.setup_game_over_screen()
            self.play_again_button.show()
            self.exit_button.show()

        self.manager.draw_ui(self.screen)
        py.display.flip()

    def draw_game_elements(self):
        self.screen.fill((0, 0, 0))
        py.draw.rect(self.screen, (150, 150, 150), (200, 50, 300, 600), 2)

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
