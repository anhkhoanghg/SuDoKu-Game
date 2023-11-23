import random
from constant import *
from logic.Cell import Cell
from logic.Grid import Grid
from logic.letters_transform import *
from logic.AntColony import AntSolver
from sudoku import show_sudoku

board = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]]
t = to_letters(board)
show_sudoku(t)
gr = Grid(grid_size=GRID_SIZE)
gr.read_grid(board=board)
gr.propagate_constraints_all_cells()
gr.deduce_vals_all_cells()
msg = ''
if gr.not_solvable():
    msg = "Sudoku not solvable"
if gr.all_cells_fixed():
    msg = "Sudoku solved"
print(msg)
solver = AntSolver(grid=gr, global_pher_update=GLOBAL_PHER_UPDATE, best_pher_evaporation=BEST_PHER_EVAPORATION, num_of_ants=NUM_OF_ANTS)
s = solver.solve(LOCAL_PHER_UPDATE, GREEDINESS)
t = to_letters(s.turn_2d_array())
show_sudoku(t)
if s.is_valid():
    print("Perfect")
else:
    print("ACO not good")







