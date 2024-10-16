# import sys, os

# sys.path.append(os.path.abspath(os.path.join("services")))

# import services as ts

from services.tetris_service import TetrisService


def main():
    tetris_service = TetrisService()
    tetris_service.start_game()


if __name__ == "__main__":
    main()
