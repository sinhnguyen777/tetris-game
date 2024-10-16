import pygame
from constants import *


class GameWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 300, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris v1.0.0")

        self.background_color = BLACK
        self.running = True

    def run(self):
        while self.running:
            self.handle_event()
            self.draw()

    def handle_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(self.background_color)
        pygame.display.update()
