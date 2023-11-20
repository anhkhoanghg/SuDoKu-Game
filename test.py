from logic.Grid import Grid
from logic.BackTracking import BackTracking

if __name__ == "__main__":
    # Read the Sudoku puzzle from the file
    sudoku_file = "./solution/example1.txt"
    grid_size = 9

    sudoku_grid = Grid(grid_size)
    sudoku_solver = BackTracking(sudoku_grid)
    sudoku_solver.solve(sudoku_file)

