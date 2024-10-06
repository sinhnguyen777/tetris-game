from repository.tetris_repository import TetrisRepository


class TetrisService:
    def __init__(self):
        self.tetris_repo = TetrisRepository()

    def start_game(self):
        # Logic để bắt đầu game
        self.tetris_repo.start_game()

    def pause_game(self):
        # Logic để tạm dừng game
        self.tetris_repo.pause_game()

    def get_game_state(self):
        # Lấy trạng thái game hiện tại
        return self.tetris_repo.get_game_state()
