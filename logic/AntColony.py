from logic.Ant import Ant
from logic.letters_transform import to_letters, to_numbers, check_if_letters
from logic.Grid import Grid
import random
import copy
import time
from constant import *



class AntSolver:
    def __init__(self, grid, global_pher_update, best_pher_evaporation, num_of_ants):
        # Grid
        self.grid = grid

        self.global_pher_update = global_pher_update
        self.best_pher_evaporation = best_pher_evaporation
        self.num_of_ants = num_of_ants


        # Array of ants
        self.ants = [Ant() for i in range(self.num_of_ants)]

        # Initial pheromone matrix val
        self.initial_pher_val = 1 / self.grid.cell_cnt

        # Pheromone matrix
        self.pher_matrix = [
            [[self.initial_pher_val for _ in range(self.grid.grid_size)] for _ in
             range(self.grid.grid_size)]
            for _ in range(self.grid.grid_size)]

        self.solution = self.grid
        self.best_pher_to_add = 0
        self.explored_nodes = 0
        self.start_time = 0

    def reset_statistics(self):
        self.explored_nodes = 0
        self.start_time = time.time()

    def print_statistics(self):
        elapsed_time = time.time() - self.start_time
        print(f"Explored Nodes: {self.explored_nodes}")
        print(f"Time Taken: {elapsed_time:.4f} seconds")
        return self.explored_nodes

    def print_pher_matrix(self):
        print("Pheromone matrix:")

        for row_nr, row in enumerate(self.pher_matrix):
            print("row ", row_nr, ":")

            for col_nr, pher_vals in enumerate(row):
                print("col ", col_nr, ":", end="")

                for pher_val in pher_vals:
                    print("{0:.2f} ".format(pher_val), end="")

                print()

    def global_pher_matrix_update(self):
        for row in range(self.grid.grid_size):
            for col in range(self.grid.grid_size):
                sol_cell = self.solution.get_cell((row, col))

                # Update pheromone matrix
                if not sol_cell.failed():
                    self.pher_matrix[row][col][sol_cell.get_val() - 1] = self.pher_matrix[row][col][sol_cell.get_val() - 1] * \
                        (1 - self.global_pher_update) + self.global_pher_update * self.best_pher_to_add


    def solve(self, local_pher_update, greediness):
        solved = False
        cycle = 1
        self.reset_statistics()

        while not solved:
            for i in range(self.num_of_ants):
                # Randomly selected position where ant will start solving sudoku
                start_pos = (random.randint(0, self.grid.grid_size - 1), random.randint(0, self.grid.grid_size - 1))

                # Add ant
                self.ants[i] = Ant(self.pher_matrix, self.initial_pher_val, local_pher_update, greediness,
                                   copy.deepcopy(self.grid), start_pos)

            # Step with each ant by one cell until they fill all the cells on the grid
            for step in range(self.grid.cell_cnt):
                for ant in self.ants:
                    ant.step()
                    self.explored_nodes += 1

            # Find best performing ant
            best_ant_fixed_cnt = 0
            best_ant = None

            for idx, ant in enumerate(self.ants):
                num_fixed = ant.get_fixed_cnt()

                # Sudoku is solved
                if num_fixed == self.grid.cell_cnt:
                    self.solution = ant.grid
                    self.solution.print()
                    print(self.solution.fixed_cell_cnt, "fixed cells")
                    self.print_pher_matrix()
                    # self.print_statistics()
                    return self.solution

                # New best
                if num_fixed > best_ant_fixed_cnt:
                    best_ant = ant
                    best_ant_fixed_cnt = num_fixed

            pher_to_add = self.grid.cell_cnt / (self.grid.cell_cnt - best_ant_fixed_cnt)

            if pher_to_add > self.best_pher_to_add:
                self.solution = best_ant.grid
                self.best_pher_to_add = pher_to_add

            # Do global pheromone update
            self.global_pher_matrix_update()

            # Do best value evaporation
            self.best_pher_to_add *= (1 - self.best_pher_evaporation)
            self.solution.print()
            print(self.solution.fixed_cell_cnt, "fixed cells")
            self.print_pher_matrix()

            cycle += 1

        return self.solution

def ACO_solve(board):
    print("\nSolving with ACO...")
    start_time = time.time()

    letters = False
    if check_if_letters(board):
        board = to_numbers(board)
        letters = True
    gr = Grid(grid_size=GRID_SIZE)
    gr.read_grid(board=board)
    gr.propagate_constraints_all_cells()
    gr.deduce_vals_all_cells()
    if gr.not_solvable():
        print("Sudoku not solvable")
        return False
    solver = AntSolver(grid=gr, global_pher_update=GLOBAL_PHER_UPDATE, best_pher_evaporation=BEST_PHER_EVAPORATION, num_of_ants=NUM_OF_ANTS)
    s = solver.solve(LOCAL_PHER_UPDATE, GREEDINESS)
    explored_nodes = solver.print_statistics()
    elapsed_time = time.time() - start_time
    if s:
        solution = s.turn_2d_array()
        if letters == True:
            solution = to_letters(solution)
        else:
            pass
    return solution,explored_nodes ,elapsed_time


