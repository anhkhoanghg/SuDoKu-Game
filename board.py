import pygame
from sudoku import (
    complete_sudoku,
    is_valid_board as is_valid,
    generate_random_sudoku,
    show_sudoku,
    is_empty,
)
from square import Square

import time

tm = 20
lm = 20
prev_val = None


class Board(Square):
    m2 = [
        [8, 1, 0, 0, 3, 0, 0, 2, 7],
        [0, 6, 2, 0, 5, 0, 0, 9, 0],
        [0, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 6, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 2, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 5, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 2, 0, 0, 1, 0, 7, 5, 0],
        [3, 8, 0, 0, 7, 0, 0, 4, 2],
    ]

    m1 = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]

    def __init__(self, rows, columns, w, h, board):
        self.board = board
        self.rows = rows
        self.columns = columns
        # Each square has a set value
        self.squares = [
            [
                Square(
                    i,
                    j,
                    w,
                    h,
                    self.board[i][j],
                    True if self.board[i][j] > 0 else False,
                )
                for j in range(columns)
            ]
            for i in range(rows)
        ]
        self.w = w
        self.h = h
        self.model = self.board
        self.clicked = False
        # Separation between one square and the next one
        self.sep = w / 9

    def insert(self, value):
        # Inserts the value into the current square
        row, column = self.clicked
        if self.squares[row][column].value == 0:
            self.squares[row][column].set_value(value)
            self.update_board()
            # checks if It's correct
            if is_valid(self.board, value, (row, column)) and complete_sudoku(
                self.board.copy()
            ):
                print(show_sudoku(self.board))
                return True
            # Resets the value
            else:
                self.squares[row][column].set_value(0)
                self.squares[row][column].set_temp_value(0)
                self.update_board()
                # print(show_sudoku(self.board))
                return False

    def is_empty_game(self):
        # Checks if a number was inserted in that same position
        output = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    output.append((i, j))
        return output

    def insert2(self, value, row, column):
        # Inserts the value into the current square

        if self.squares[row][column].value == 0:
            self.squares[row][column].set_value(value)
            self.update_board()
            # checks if It's correct
            if is_valid(self.board, value, (row, column)) and complete_sudoku(
                self.board
            ):
                return True
            # Resets the value
            else:
                self.squares[row][column].set_value(0)
                self.squares[row][column].set_temp_value(0)
                self.update_board()
                return False

    def complete_GUI(self, empty):
        while empty:
            # print(empty)
            y, x = empty[0]
            for i in range(1, 10):
                self.board[y][x] = i
                self.insert2(i, y, x)
                self.update_board()
            return 0

    # Updates the values of each square
    def update_board(self):
        self.board = [
            [self.squares[i][j].value for j in range(self.columns)]
            for i in range(self.rows)
        ]

    # If another square is clicked, the previous one will stop returning self.clicked = True.
    def clicked_handler(self, row, column):
        global prev_val
        # Resets all to False
        if prev_val != None:
            prev_val.clicked = False

        prev_val = self.squares[row][column]
        # States that the specific square has been clicked
        self.squares[row][column].clicked = True
        self.clicked = (row, column)

    # Sets a temporary value (Displays what the user is considering to add but hasn't fully commited).
    def temp(self, value):
        row, column = self.clicked
        self.squares[row][column].set_temp_value(value)

    # If all the values have been filled in, the user has won
    def victory_state(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.squares[i][j].value == 0:
                    return False
        return True

    # pos = a tuple with a position for what is being clicked, and prevents output out of the specified dimensions
    def click(self, p):
        if p[0] - lm < self.w and p[1] - tm < self.h:
            sep = self.sep
            # parsing required to make it more convenient for the square position

            x = int((p[0] + -lm) // sep)
            y = int((p[1] + -tm) // sep)
            if y < 0:
                return None
            return (y, x)
        # clicked out of the specified bounds
        return None

    def render(self, win):
        sep = self.sep
        for i in range(self.rows + 1):
            t = 1
            # specifies the thickness of each line
            if not i % 3:
                t = 3
            pygame.draw.line(
                win, (0, 0, 0), (lm, i * sep + tm), (self.w + lm, i * sep + tm), t
            )
            pygame.draw.line(
                win, (0, 0, 0), (i * sep + lm, tm), (i * sep + lm, self.h + tm), t
            )
        # Renders each square with render(window) from the Square class
        for i in range(self.rows):
            for j in range(self.columns):
                self.squares[i][j].render(win)

    # No value makes the square empty
    def clear(self):
        row, column = self.clicked
        if self.squares[row][column].value == 0:
            self.squares[row][column].set_temp_value(0)

