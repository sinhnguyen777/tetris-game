import sys, os
import pygame as py
from position import Position

sys.path.append(os.path.abspath(os.path.join("constants")))

import constants as cs


class Tetromino:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.col_offset = 0
        self.row_offset = 0
        self.colors = cs.Colors.get_color()
        self.ghost_colors = cs.Ghost_Colors.get_color()

    def move(self, col, row):
        self.col_offset += col
        self.row_offset += row

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(
                position.row + self.row_offset, position.col + self.col_offset
            )
            moved_tiles.append(position)
        return moved_tiles

    def rotate_cw(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def rotate_ccw(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1

    def rotate_180(self):
        for _ in range(2):
            self.rotation_state += 1
            if self.rotation_state == len(self.cells):
                self.rotation_state = 0

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = py.Rect(
                tile.col * self.cell_size + offset_x,
                (tile.row - 3) * self.cell_size + offset_y,
                self.cell_size - 1,
                self.cell_size - 1,
            )
            py.draw.rect(screen, self.colors[self.id], tile_rect)

    def draw_ghost(self, screen):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = py.Rect(
                tile.col * self.cell_size,
                (tile.row - 3) * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1,
            )
            py.draw.rect(screen, self.ghost_colors[self.id], tile_rect)
