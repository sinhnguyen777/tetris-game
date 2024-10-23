import numpy
import pygame
from constants import Colors


class Grid:
    def __init__(self):
        self.num_cols = 10
        self.num_rows = 23
        self.cell_size = 30
        self.line_clears = 0
        self.grid = numpy.zeros((self.num_rows, self.num_cols), dtype=int)
        self.colors = Colors.get_color()

    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=" ")
            print()

    def is_game_over(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] != 0:
                return True
        return False

    def is_inside(self, row, col):
        if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
            return True
        return False

    def is_cells_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False

    def is_row_full(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True

    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    def move_row_down(self, row, num_rows):
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_row(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def draw(self, screen):
        for row in range(self.num_rows - 3):
            for col in range(self.num_cols):
                cell_value = self.grid[row + 3][col]
                cell_rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1,
                )
                if cell_value == 0:
                    cell_border_color = "#505050"
                else:
                    cell_border_color = self.colors[cell_value]
                cell_border_rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, cell_border_color, cell_border_rect, width=1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
