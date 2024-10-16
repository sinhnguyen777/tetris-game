import pygame
from constants import *


class TetrisUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris v1.0.0")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_grid(self, grid):
        self.screen.fill(BLACK)

        for row in range(grid.rows):
            for col in range(grid.cols):
                pygame.draw.rect(
                    self.screen,
                    WHITE if grid.grid[row][col] else BLACK,
                    (col * 30, row * 30, 30, 30),
                    1,
                )
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def quit(self):
        pygame.quit()
