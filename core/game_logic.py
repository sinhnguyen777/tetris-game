class Game:
    def __init__(self):
        self.line_clears = 0
        self.current_tetromino = None
        self.grid = None  # Initialize grid object here

    def move_down(self):
        pass  # Logic for moving the current tetromino down

    def move_left(self):
        pass  # Logic for moving the tetromino left

    def move_right(self):

        pass  # Logic for moving the tetromino right

    def rotate_cw(self):
        pass  # Clockwise rotation

    def rotate_ccw(self):
        pass  # Counterclockwise rotation

    def hard_drop(self):
        pass  # Hard drop logic

    def draw_hold_tetromino(self, surface):
        pass  # Draw the current held tetromino

    def draw_current_queue(self, surface):
        pass  # Draw the queue of upcoming tetrominoes
