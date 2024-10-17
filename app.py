import pygame
from services import TetrisService
from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris v1.0.0")

    tetris_service = TetrisService()
    # tetris_service.start_game()

    # game loop (refresh app screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # refresh screen
        tetris_service.update_game()

        screen.fill((0, 0, 0))
        tetris_service.render(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
