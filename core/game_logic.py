from grid import Grid
from tetrominos import *
import random, copy


class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = 0
        self.game_over = False
        self.line_clears = 0
        self.das = 65
        self.arr = 0
        self.soft_drop_speed = 1
        self.tetrominos = [
            LTetromino(),
            JTetromino(),
            STetromino(),
            ZTetromino(),
            OTetromino(),
            ITetromino(),
            TTetromino(),
        ]
        self.current_queue = self.create_tetromino_queue()
        self.next_queue = self.create_tetromino_queue()
        self.current_tetromino = self.get_current_tetromino()
        # self.next_tetromino = self.get_random_tetromino()

    def is_game_over(self):
        for row in range(3):
            if self.grid.is_game_over(row):
                return True
        return False

    def randomize(self, arr):
        for i in range(len(arr) - 1, 0, -1):
            j = random.randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def create_tetromino_queue(self):
        current_tetromino_queue = copy.deepcopy(self.tetrominos)
        self.randomize(current_tetromino_queue)
        return current_tetromino_queue

    def get_current_tetromino(self):
        tetromino = self.current_queue.pop(0)
        self.current_queue.append(self.next_queue.pop(0))
        if len(self.next_queue) == 0:
            self.next_queue = self.create_tetromino_queue()
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
                screen, 255, 230 + (self.current_queue[i].cell_size * 3 * i)
            )

    # def draw_next_tetromino(self, screen):
    #     if self.next_tetromino.id == 6 or self.next_tetromino.id == 7:
    #         self.next_tetromino.draw(screen, 255, 250)
    #     else:
    #         self.next_tetromino.draw(screen, 270, 250)

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
            tetromino.move(1, 0)
            if self.tetromino_inside(tetromino) == False:
                tetromino.move(-1, 0)
            elif self.tetromino_fits(tetromino) == False:
                tetromino.move(-1, 0)
        return tetromino

    # chưa tối ưu

    def move_last_col_left(self):
        while not self.move_left():
            break

    def move_last_col_right(self):
        while not self.move_right():
            break

    def move_left(self):
        self.current_tetromino.move(0, -1)
        if (
            self.tetromino_inside(self.current_tetromino) == False
            or self.tetromino_fits(self.current_tetromino) == False
        ):
            self.current_tetromino.move(0, 1)
            return True

    def move_right(self):
        self.current_tetromino.move(0, 1)
        if (
            self.tetromino_inside(self.current_tetromino) == False
            or self.tetromino_fits(self.current_tetromino) == False
        ):
            self.current_tetromino.move(0, -1)
            return True

    def move_down(self):
        self.current_tetromino.move(1, 0)
        if (
            self.tetromino_inside(self.current_tetromino) == False
            or self.tetromino_fits(self.current_tetromino) == False
        ):
            self.current_tetromino.move(-1, 0)
            self.lock_tetromino()

    def lock_tetromino(self):
        tiles = self.current_tetromino.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_tetromino.id
        self.current_tetromino = self.get_current_tetromino()
        # self.current_tetromino = self.next_tetromino
        # self.next_tetromino = self.get_random_tetromino()
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
        return

    def is_rotate_valid(self):
        if self.tetromino_inside(self.current_tetromino) == False:
            tiles = self.current_tetromino.get_cell_positions()
            for tile in tiles:
                if tile.col < 0:
                    self.current_tetromino.move(0, 1)
                if tile.col > self.grid.num_cols - 1:
                    self.current_tetromino.move(0, -1)
                if tile.row > self.grid.num_rows - 1:
                    self.current_tetromino.move(-1, 0)
        if self.tetromino_fits(self.current_tetromino) == False:
            tiles = self.current_tetromino.get_cell_positions()
            if self.grid.grid[tiles[3].row][tiles[3].col] != 0:
                self.current_tetromino.move(-1, 0)
            else:
                # undo_rotate chưa hoàn chỉnh
                self.current_tetromino.undo_rotate()

    def rotate_cw(self):
        self.current_tetromino.rotate_cw()
        self.is_rotate_valid()

    def rotate_ccw(self):
        self.current_tetromino.rotate_ccw()
        self.is_rotate_valid()

    def rotate_180(self):
        self.current_tetromino.rotate_180()
        self.is_rotate_valid()

    def hard_drop(self):
        self.score += 2 * (
            self.tetromino_ghost().row_offset - self.current_tetromino.row_offset
        )
        self.current_tetromino.row_offset = self.tetromino_ghost().row_offset
        self.lock_tetromino()

    def soft_drop(self):
        self.current_tetromino.move(1, 0)
        if (
            self.tetromino_inside(self.current_tetromino) == False
            or self.tetromino_fits(self.current_tetromino) == False
        ):
            self.current_tetromino.move(-1, 0)
            # self.lock_tetromino()
        else:
            self.score += 1
