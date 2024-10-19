BASIC_ROTATION = (0, 0)


class Zero_One:
    def __init__(self):
        self.offset = {
            "NormalTetromino": {
                0: BASIC_ROTATION,
                1: (-1, 0),
                2: (-1, -1),
                3: (0, 2),
                4: (-1, 2),
            },
            "ITetromino": {
                0: BASIC_ROTATION,
                1: (-2, 0),
                2: (1, 0),
                3: (-2, 1),
                4: (1, -2),
            },
        }


class One_Two:
    def __init__(self):
        self.offset = {
            "NormalTetromino": {
                0: BASIC_ROTATION,
                1: (1, 0),
                2: (1, 1),
                3: (0, -2),
                4: (1, -2),
            },
            "ITetromino": {
                0: BASIC_ROTATION,
                1: (-1, 0),
                2: (2, 0),
                3: (-1, -2),
                4: (2, 1),
            },
        }


class Two_Three:
    def __init__(self):
        self.offset = {
            "NormalTetromino": {
                0: BASIC_ROTATION,
                1: (1, 0),
                2: (1, -1),
                3: (0, 2),
                4: (1, 2),
            },
            "ITetromino": {
                0: BASIC_ROTATION,
                1: (2, 0),
                2: (-1, 0),
                3: (2, -1),
                4: (-1, 2),
            },
        }


class Three_Zero:
    def __init__(self):
        self.offset = {
            "NormalTetromino": {
                0: BASIC_ROTATION,
                1: (-1, 0),
                2: (-1, 1),
                3: (0, -2),
                4: (-1, -2),
            },
            "ITetromino": {
                0: BASIC_ROTATION,
                1: (1, 0),
                2: (-2, 0),
                3: (1, 2),
                4: (-2, -1),
            },
        }


class WallKick_180:
    def __init__(self):
        self.offset = {
            "NormalTetromino": {0: BASIC_ROTATION, 1: (0, -1), 2: (1, 0), 3: (-1, 0)},
            "ITetromino": {0: BASIC_ROTATION, 1: (0, -1), 2: (1, 0), 3: (-1, 0)},
        }
