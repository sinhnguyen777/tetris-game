import random


class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.position = [0, 0]

    def rotate(self):
        pass  # Logic to rotate the piece


def random_tetromino():
    shapes = ["I", "O", "T", "S", "Z", "J", "L"]
    return Tetromino(random.choice(shapes))
