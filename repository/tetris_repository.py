class TetrisRepository:
    def __init__(self):
        self.game_state = "stopped"  # Trạng thái của game (dừng, đang chạy, tạm dừng)

    def start_game(self):
        self.game_state = "running"
        print("Game bắt đầu! Trạng thái hiện tại:", self.game_state)

    def pause_game(self):
        if self.game_state == "running":
            self.game_state = "paused"
            print("Game tạm dừng! Trạng thái hiện tại:", self.game_state)
        else:
            print("Game chưa được bắt đầu hoặc đã tạm dừng.")

    def get_game_state(self):
        return self.game_state
