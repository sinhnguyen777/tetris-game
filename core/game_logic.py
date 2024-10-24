import random, copy

from core.grid import Grid
from core.tetrominos import (
    JTetromino,
    LTetromino,
    STetromino,
    TTetromino,
    OTetromino,
    ZTetromino,
    ITetromino,
)
from core.srs_logic import Zero_One, One_Two, Two_Three, Three_Zero, WallKick_180
from utils import randomize


class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = 0
        self.game_over = False
        self.lockdelay = False
        self.line_clears = 0
        self.das = 65
        self.arr = 10
        self.level = 1
        self.soft_drop_speed = 30
        self.tetrominos = [
            LTetromino(),
            JTetromino(),
            ZTetromino(),
            STetromino(),
            TTetromino(),
            OTetromino(),
            ITetromino(),
        ]
        self.current_queue = self.create_tetromino_queue()
        self.next_queue = self.create_tetromino_queue()
        self.current_tetromino = self.get_current_tetromino()
        self.hold_tetromino = None
        self.is_holding = False

    def update_settings(self, das_value, arr_value, soft_drop_speed, level):
        self.das = das_value
        self.arr = arr_value
        self.soft_drop_speed = soft_drop_speed
        self.level = level

    def is_game_over(self):
        for row in range(3):
            if self.grid.is_game_over(row):
                return True
        return False

    def create_tetromino_queue(self):
        current_tetromino_queue = copy.deepcopy(self.tetrominos)
        randomize(current_tetromino_queue)
        return current_tetromino_queue

    def get_current_tetromino(self):
        tetromino = self.current_queue.pop(0)
        self.current_queue.append(self.next_queue.pop(0))
        if len(self.next_queue) == 0:
            self.next_queue = self.create_tetromino_queue()
        tetromino.move(0, 1)
        if not self.tetromino_fits(tetromino):
            tetromino.move(0, -1)
        return tetromino

    def get_random_tetromino(self):
        if len(self.tetrominos) == 0:
            self.tetrominos = [
                LTetromino(),
                JTetromino(),
                STetromino(),
                ZTetromino(),
                OTetromino(),
                ITetromino(),
                TTetromino(),
            ]
        tetromino = random.choice(self.tetrominos)
        self.tetrominos.remove(tetromino)
        return tetromino

    def draw_current_queue(self, screen):
        for i in range(5):
            self.current_queue[i].draw(
                screen, 455, 250 + (self.current_queue[i].cell_size * 3 * i)
            )

    def set_hold_tetromino(self):
        if not self.is_holding:
            if self.hold_tetromino == None:
                self.hold_tetromino = copy.deepcopy(
                    self.tetrominos[self.current_tetromino.id - 1]
                )
                self.current_tetromino = self.get_current_tetromino()
            else:
                temp = copy.deepcopy(self.hold_tetromino)
                self.hold_tetromino = copy.deepcopy(
                    self.tetrominos[self.current_tetromino.id - 1]
                )
                self.current_tetromino = copy.deepcopy(self.tetrominos[temp.id - 1])
            self.is_holding = True

    def draw_hold_tetromino(self, screen):
        if self.hold_tetromino != None:
            if self.hold_tetromino.id == 6 or self.hold_tetromino.id == 7:
                self.hold_tetromino.draw(screen, -52, 170)
            else:
                self.hold_tetromino.draw(screen, -37, 170)

    def draw(self, screen):
        self.grid.draw(screen)
        self.tetromino_ghost().draw_ghost(screen)
        self.current_tetromino.draw(screen, 0, 0)

    def tetromino_ghost(self):
        tetromino = copy.deepcopy(self.current_tetromino)
        tiles = self.current_tetromino.cells
        ghost_offset = self.grid.num_rows - (
            tiles[self.current_tetromino.rotation_state][3].row + 1
        )
        for _ in range(ghost_offset):
            tetromino.move(0, 1)
            if self.tetromino_inside(tetromino) == False:
                tetromino.move(0, -1)
            elif self.tetromino_fits(tetromino) == False:
                tetromino.move(0, -1)
        return tetromino

    # chưa tối ưu

    def move_last_col_left(self):
        is_not_collision = True
        while is_not_collision:
            if self.move_left():
                is_not_collision = False

    def move_last_col_right(self):
        is_not_collision = True
        while is_not_collision:
            if self.move_right():
                is_not_collision = False

    def is_collision(self):
        if (
            self.tetromino_inside(self.current_tetromino) == False
            or self.tetromino_fits(self.current_tetromino) == False
        ):
            return True
        return False

    def move_left(self):
        self.current_tetromino.move(-1, 0)
        if self.is_collision():
            self.current_tetromino.move(1, 0)
            return True
        return False

    def move_right(self):
        self.current_tetromino.move(1, 0)
        if self.is_collision():
            self.current_tetromino.move(-1, 0)
            return True
        return False

    def move_down(self):
        self.current_tetromino.move(0, 1)
        if self.is_collision():
            self.current_tetromino.move(0, -1)
            self.lockdelay = True
            return True

    def lock_tetromino(self):
        self.lockdelay = False
        tiles = self.current_tetromino.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_tetromino.id
        self.current_tetromino = self.get_current_tetromino()
        if self.is_holding:
            self.is_holding = False
        self.line_clears += self.grid.clear_full_row()
        self.game_over = self.is_game_over()

    def tetromino_inside(self, tetromino):
        tiles = tetromino.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) == False:
                return False
        return True

    def tetromino_fits(self, tetromino):
        tiles = tetromino.get_cell_positions()
        for tile in tiles:
            if self.grid.is_cells_empty(tile.row, tile.col) == False:
                return False
        return True

    def is_rotate_valid(self, rotation_state, type):
        if type == "cw":
            if rotation_state == 0:
                srs_tests = Three_Zero()
            elif rotation_state == 1:
                srs_tests = Zero_One()
            elif rotation_state == 2:
                srs_tests = One_Two()
            elif rotation_state == 3:
                srs_tests = Two_Three()
        elif type == "ccw":
            if rotation_state == 0:
                srs_tests = Zero_One()
            elif rotation_state == 1:
                srs_tests = One_Two()
            elif rotation_state == 2:
                srs_tests = Two_Three()
            elif rotation_state == 3:
                srs_tests = Three_Zero()
        elif type == "180deg":
            srs_tests = WallKick_180()

        if self.current_tetromino.id != 7:
            test_offsets = srs_tests.offset["NormalTetromino"]
        else:
            test_offsets = srs_tests.offset["ITetromino"]

        for tetromino_offset in test_offsets.values():
            block = copy.deepcopy(self.current_tetromino)
            if type == "cw" or type == "180deg":
                block.move(tetromino_offset[0], tetromino_offset[1])
            elif type == "ccw":
                block.move(-tetromino_offset[0], -tetromino_offset[1])
            if self.tetromino_inside(block) and self.tetromino_fits(block):
                return tetromino_offset
        return False

    def rotate_cw(self):
        self.current_tetromino.rotate_cw()
        rotation_status = self.is_rotate_valid(
            self.current_tetromino.rotation_state, "cw"
        )
        if rotation_status != False:
            self.current_tetromino.move(rotation_status[0], rotation_status[1])
        else:
            self.current_tetromino.rotate_ccw()

    def rotate_ccw(self):
        self.current_tetromino.rotate_ccw()
        rotation_status = self.is_rotate_valid(
            self.current_tetromino.rotation_state, "ccw"
        )
        if rotation_status != False:
            self.current_tetromino.move(-rotation_status[0], -rotation_status[1])
        else:
            self.current_tetromino.rotate_cw()

    def rotate_180(self):
        self.current_tetromino.rotate_180()
        rotation_status = self.is_rotate_valid(
            self.current_tetromino.rotation_state, "180deg"
        )
        if rotation_status != False:
            self.current_tetromino.move(rotation_status[0], rotation_status[1])
        else:
            self.current_tetromino.rotate_180()

    def hard_drop(self):
        self.score += 2 * (
            self.tetromino_ghost().row_offset - self.current_tetromino.row_offset
        )
        self.current_tetromino.row_offset = self.tetromino_ghost().row_offset
        self.lock_tetromino()

    def soft_drop(self):
        self.current_tetromino.move(0, 1)
        if self.is_collision():
            self.current_tetromino.move(0, -1)
            self.lockdelay = True
        else:
            self.score += 1

    def instant_soft_drop(self):
        self.score += 1 * (
            self.tetromino_ghost().row_offset - self.current_tetromino.row_offset
        )
        self.current_tetromino.row_offset = self.tetromino_ghost().row_offset
        self.lockdelay = True
