from logic.Cell import Cell
from logic.Grid import Grid

class BackTracking:
    def __init__(self, grid_size):
        self.grid = Grid(grid_size)

    def solve(self, input_file):
        if not self.grid.read_grid(input_file):
            print("Invalid Sudoku grid.")
            return

        if self.solve_sudoku():
            print("Sudoku solution:")
            self.grid.print()
        else:
            print("No solution found.")

    def solve_sudoku(self):
        if self.grid.all_cells_fixed():
            return True

        pos = self.find_unassigned_cell()

        for val in range(1, self.grid.grid_size + 1):
            if self.is_safe(pos, val):
                self.grid.set_cell_val(pos, val)

                if self.solve_sudoku():
                    return True

                self.grid.set_cell_val(pos, 0)

        return False

    def find_unassigned_cell(self):
        for row in range(self.grid.grid_size):
            for col in range(self.grid.grid_size):
                cell = self.grid.get_cell((row, col))
                if not cell.fixed():
                    return (row, col)
        return None

    def is_safe(self, pos, val):
        return (
            self.is_safe_row(pos, val) and
            self.is_safe_col(pos, val) and
            self.is_safe_square(pos, val)
        )

    def is_safe_row(self, pos, val):
        for col in range(self.grid.grid_size):
            if self.grid.get_cell((pos[0], col)).get_val() == val:
                return False
        return True

    def is_safe_col(self, pos, val):
        for row in range(self.grid.grid_size):
            if self.grid.get_cell((row, pos[1])).get_val() == val:
                return False
        return True

    def is_safe_square(self, pos, val):
        square_size = int(self.grid.grid_size ** 0.5)
        square_start_row = pos[0] // square_size * square_size
        square_start_col = pos[1] // square_size * square_size

        for row in range(square_start_row, square_start_row + square_size):
            for col in range(square_start_col, square_start_col + square_size):
                if self.grid.get_cell((row, col)).get_val() == val:
                    return False
        return True


