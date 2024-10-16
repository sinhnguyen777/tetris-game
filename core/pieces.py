import random


class Pieces:
    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "L": [[1, 0, 0], [1, 1, 1]],
        "J": [[0, 0, 1], [1, 1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "Z": [[1, 1, 0], [0, 1, 1]],
    }

    def __init__(self) -> None:
        self.shape = random.choice(list(self.SHAPES.values()))
        self.x = 0
        self.y = 0

    def rotate(self):
        self.shape = list(map(list, zip(*self.shape[::-1])))
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
