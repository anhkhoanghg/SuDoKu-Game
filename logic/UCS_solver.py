import copy
import time
import heapq
from logic.letters_transform import to_letters, to_numbers, check_if_letters

class UCSProblem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial) # Size of grid
        self.height = int(self.size/3) # Size of a quadrant

    def check_legal(self, state):
        total = sum(range(1, self.size+1))

        for row in range(self.size):
            if (len(state[row]) != self.size) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.size):
                column_total += state[column][row]

            if (column_total != total):
                return False

        for column in range(0,self.size,3):
            for row in range(0,self.size,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True

    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

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
        row, column = self.get_spot(self.size, state)
        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state, 1 

class UCSNode:
    def __init__(self, state, cost):
        self.state = state
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

def UCS(problem):
    start = UCSNode(problem.initial, 0)
    if problem.check_legal(start.state):
        return start.state, 0  

    heap = []
    heapq.heappush(heap, start)
    nodes_expanded = 0

    while heap:
        node = heapq.heappop(heap)
        nodes_expanded += 1

        if problem.check_legal(node.state):
            return node.state, nodes_expanded

        for successor, cost in problem.actions(node.state):
            heapq.heappush(heap, UCSNode(successor, node.cost + cost))

    return None, nodes_expanded

def UCS_solve(board):
    print("\nSolving with UCS...")
    letters = False
    if check_if_letters(board):
        board = to_numbers(board)
        letters = True

    start_time = time.time()
    problem = UCSProblem(board)
    solution, nodes_expanded = UCS(problem)
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