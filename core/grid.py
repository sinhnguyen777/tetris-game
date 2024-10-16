class Grid:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_row_full(self, row):
        return all(cell != 0 for cell in self.grid[row])

    def clear_row(self, row):
        del self.grid[row]
        self.grid.insert(0, [0 for _ in range(self.cols)])
