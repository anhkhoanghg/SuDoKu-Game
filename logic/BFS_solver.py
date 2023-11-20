from queue import Queue
import copy
import time
from logic.letters_transform import to_letters, to_numbers, check_if_letters

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.size = len(initial) # Size of a grid
        self.height = int(self.size/3) # Size of a quadrant

    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column   

    def actions(self, state):
        number_set = range(1, self.size+1) 
        in_column = [] 
        in_block = [] 

        row,column = self.get_spot(self.size, state) 

        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)

        for column_index in range(self.size):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)

        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)

        for number in options:
            yield number, row, column      

    def result(self, state, action):

        play = action[0]
        row = action[1]
        column = action[2]

        new_state = copy.deepcopy(state)
        new_state[row][column] = play

        return new_state

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

class Node:

    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, action)

def BFS(problem):
    node = Node(problem.initial)
    if problem.check_legal(node.state):
        return node, 0 

    frontier = Queue()
    frontier.put(node)
    nodes_expanded = 0  

    while frontier.qsize() != 0:
        node = frontier.get()
        nodes_expanded += 1  

        for child in node.expand(problem):
            if problem.check_legal(child.state):
                return child, nodes_expanded

            frontier.put(child)

    return None, nodes_expanded

def BFS_solve(board):
    print ("\nSolving with BFS...")
    letters = False
    if check_if_letters(board):
        board = to_numbers(board) 
        letters = True

    start_time = time.time()

    problem = Problem(board)
    solution, nodes_expanded = BFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        if letters:
            solution.state = to_letters(solution.state) 
        print ("Found solution")
    else:
        print ("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time) + " seconds")
    print ("Node_Expanded: " + str(nodes_expanded) + " nodes")
    return solution.state
    
    