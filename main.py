import random
from constant import *
from logic.Cell import Cell
from logic.Grid import Grid
from logic.letters_transform import *
from logic.AntColony import AntSolver
from logic.AntColony import ACO_solve
from logic.BFS_solver import BFS_solve
from logic.DFS_solver import DFS_solve
from logic.UCS_solver import UCS_solve
from logic.Heuristic_solvers import a_star_solve
from sudoku import show_sudoku, generate_random_sudoku



# board = [[7, 8, 5, 4, 3, 9, 1, 2, 6],
#         [6, 1, 2, 8, 7, 5, 3, 4, 9],
#         [4, 9, 3, 6, 2, 1, 5, 7, 8],
#         [8, 5, 7, 9, 4, 3, 2, 6, 1],
#         [2, 6, 1, 7, 5, 8, 9, 3, 4],
#         [9, 3, 4, 1, 6, 0, 7, 0, 5],
#         [5, 7, 8, 3, 9, 4, 6, 1, 2],
#         [1, 2, 6, 5, 8, 7, 4, 9, 3],
#         [3, 4, 9, 2, 1, 6, 8, 5, 7]]
board = [[0,3,0,0,0,1,5,0,0], 
      [0,0,0,5,0,0,0,8,4],
      [0,0,5,0,0,7,0,6,0],
      [0,0,0,0,0,0,0,0,0],
      [0,8,0,2,0,0,0,7,0],
      [0,0,0,8,5,0,0,0,9],
      [0,0,3,0,9,4,0,0,7],
      [0,0,4,0,0,0,0,0,8],
      [5,0,6,0,1,0,0,0,0]]
grid = [['C','.','G','.','.','.','.','A','.'],
        ['.','.','.','H','.','E','.','.','F'],
        ['I','.','.','.','G','.','.','.','D'],
        ['.','.','H','.','E','.','.','.','.'],
        ['B','.','.','F','.','H','.','.','C'],
        ['.','.','.','.','I','.','E','.','.'],
        ['H','.','.','.','A','.','.','.','G'],
        ['F','.','.','I','.','D','.','.','.'],
        ['.','C','.','.','.','.','I','.','H']]
# t = to_letters(grid)
# show_sudoku(t)
# gr = Grid(grid_size=GRID_SIZE)
# gr.read_grid(board=grid)
# gr.propagate_constraints_all_cells()
# gr.deduce_vals_all_cells()
# msg = ''
# if gr.not_solvable():
#     msg = "Sudoku not solvable"
# if gr.all_cells_fixed():
#     msg = "Sudoku solved"
# print(msg)
# solver = AntSolver(grid=gr, global_pher_update=GLOBAL_PHER_UPDATE, best_pher_evaporation=BEST_PHER_EVAPORATION, num_of_ants=NUM_OF_ANTS)
# s = solver.solve(LOCAL_PHER_UPDATE, GREEDINESS)
# t = to_letters(s.turn_2d_array())
# show_sudoku(t)
# if s.is_valid():
#     print("Perfect")
# else:
#     print("ACO not good")
p = generate_random_sudoku("hard")
# s, nodee, timee = BFS_solve(board=p)
s, nodee, timee = DFS_solve(board=p)
# show_sudoku(s)
print("ssss")







