import copy
import time
from logic.letters_transform import to_letters, to_numbers, check_if_letters
from queue import PriorityQueue

class SudokuHeuristic:
    @staticmethod
    def count_filled_cells(board):
        return sum(1 for row in board for cell in row if cell != 0)

    @staticmethod
    def heuristic(board):
        # Count the number of filled cells in the puzzle
        return SudokuHeuristic.count_filled_cells(board)
    
    
class AProblem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial) # Size of grid
        self.height = int(self.size/3) # Size of a quadrant

    def check_legal(self, state):
        exp_sum = sum(range(1, self.size+1))

        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != exp_sum):
                return False
            column_sum = 0
            for column in range(self.size):
                column_sum += state[column][row]
            if (column_sum != exp_sum):
                return False

        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):
                block_sum = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_sum += state[row + block_row][column + block_column]

                if (block_sum != exp_sum):
                    return False
        return True

    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    def get_spot(self, board, state):
        target_option_len = board
        row = 0
        while row < board:
            column = 0
            while column < board:
                if state[row][column] == 0:
                    options = self.filter_row(state, row)
                    options = self.filter_col(options, state, column)
                    options = self.filter_quad(options, state, row, column)
                    if len(options) < target_option_len:
                        target_option_len = len(options)
                        options = []
                        spotrow = row
                        spotcol = column
                column = column + 1
            row = row + 1                
        return spotrow, spotcol

    def filter_row(self, state, row):
        number_set = range(1, self.size+1) 
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    def filter_col(self, options, state, column):
        in_column = []
        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    def filter_quad(self, options, state, row, column):
        in_block = [] 
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.size, state) # Get first empty spot on board

        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state) 
            new_state[row][column] = number
            yield new_state
            
    def heuristic(self, state):
        return SudokuHeuristic.heuristic(state)

# class Node:
    
#     def __init__(self, state):
#         self.state = state

#     def expand(self, problem):
#         return [Node(state) for state in problem.actions(self.state)]

# def DFS(problem):
#     start = Node(problem.initial)
#     if problem.check_legal(start.state):
#         return start.state

#     stack = []
#     stack.append(start) 

#     while stack: 
#         node = stack.pop() 
#         if problem.check_legal(node.state):
#             return node.state
#         stack.extend(node.expand(problem)) 
#     return None

class ANode:
    def __init__(self, state, cost, heuristic):
        self.state = state
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def a_star(problem):
    start = ANode(problem.initial, 0, problem.heuristic(problem.initial))
    if problem.check_legal(start.state):
        return start.state, 0

    open_set = PriorityQueue()
    open_set.put(start)
    nodes_expanded = 0
    closed_set = set()

    while not open_set.empty():
        node = open_set.get()
        nodes_expanded += 1

        if problem.check_legal(node.state):
            return node.state, nodes_expanded

        closed_set.add(tuple(map(tuple, node.state)))

        for successor_state in problem.actions(node.state):
            successor = ANode(successor_state, node.cost + 1, problem.heuristic(successor_state))

            if tuple(map(tuple, successor.state)) not in closed_set:
                open_set.put(successor)

    return None, nodes_expanded

def a_star_solve(board):
    print("\nSolving with A*...")
    letters = False
    if check_if_letters(board):
        board = to_numbers(board)
        letters = True

    start_time = time.time()
    problem = AProblem(board)
    solution, nodes_expanded = a_star(problem)
    elapsed_time = time.time() - start_time

    if solution:
        if letters:
            solution = to_letters(solution)
        print("Found solution")
    else:
        print("No possible solutions")
        return False

    print("Nodes expanded: {}".format(nodes_expanded))
    print("Elapsed time: {:.6f} seconds".format(elapsed_time))
    return solution, nodes_expanded, elapsed_time


# def H_Solve(board):
#     print ("\nSolving with DFS and heuristics...")
#     letters = False
#     if check_if_letters(board): # Checks of the board contains letters instead of numbers
#         board = to_numbers(board) # Transforms letter puzzles to numeric puzzles
#         letters = True

#     start_time = time.time()
#     problem = Problem(board)
#     solution = DFS(problem)
#     elapsed_time = time.time() - start_time

#     if solution:
#         if letters:
#             solution = to_letters(solution) # Transforms back numeric puzzles to original letter puzzle type of true
#         print ("Found solution")
#         for row in solution:
#             print (row)
#     else:
#         print ("No possible solutions")

#     print ("Elapsed time: " + str(elapsed_time) + " seconds")