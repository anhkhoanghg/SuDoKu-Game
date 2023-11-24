from sudoku import *
from logic.BFS_solver import BFS_solve
from logic.DFS_solver import DFS_solve
from logic.Grid import Grid
from logic.UCS_solver import UCS_solve

if __name__ == "__main__":
    print ("\n\nTesting on invalid 9x9 grid...")
    grid = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]]
    # grid = [['C','.','G','.','.','.','.','A','.'], 
    #         ['.','.','.','H','.','E','.','.','F'],
    #         ['I','.','.','.','G','.','.','.','D'],
    #         ['.','.','H','.','E','.','.','.','.'],
    #         ['B','.','.','F','.','H','.','.','C'],
    #         ['.','.','.','.','I','.','E','.','.'],
    #         ['H','.','.','.','A','.','.','.','G'],
    #         ['F','.','.','I','.','D','.','.','.'],
    #         ['.','C','.','.','.','.','I','.','H']]
    # show_sudoku(grid)
    t = BFS_solve(grid)
    
    complete_sudoku(grid)
    show_sudoku(t)
    

