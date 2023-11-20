import random

current_sudoku = []

sudokus = [[[7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]],

           [[8, 1, 0, 0, 3, 0, 0, 2, 7],
            [0, 6, 2, 0, 5, 0, 0, 9, 0],
            [0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 9, 0, 6, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 2, 0, 0, 0, 4],
            [0, 0, 8, 0, 0, 5, 0, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 2, 0, 0, 1, 0, 7, 5, 0],
            [3, 8, 0, 0, 7, 0, 0, 4, 2]]]

# prints the sudoku board
def show_sudoku(game_board):
    for i in range(len(game_board)):
        if (not i % 3 and i != 0) or (i == 0):
            print("----------------------------")
        for j in range(len(game_board[i])):
            if not j % 3 and j != 0:
                print(" | ", end="")
            if j == 0:
                print("| ", end=" ")
            if j == len(game_board[i]) - 1:
                print(game_board[i][j], end="")
                print(" |")
            else:
                print(str(game_board[i][j]) + " ", end="")
    print("----------------------------")

# Looks for the 0 values in the sudoku
def is_empty(game_board):
    # Checks if a number was inserted in that same position
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            if game_board[i][j] == 0:
                return (i, j)
    return False

# n = number or input and p = position in the board in terms of the row and column
def is_valid(game_board, n, p):
    # Check the rows
    for i in range(len(game_board[0])):
        if game_board[p[0]][i] == n and p[1] != i:
            return False

    # Check the Columns
    for i in range(len(game_board)):
        if game_board[i][p[1]] == n and p[0] != i:
            return False
    # Check the Columns
    box_x = p[1] // 3
    box_y = p[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if game_board[i][j] == n and (i, j) != p:
                return False
    return True


def complete_sudoku(game_board):
    empty = is_empty(game_board)
    if empty is False:
        return 1
    else:
        y, x = empty
        for i in range(1, 10):

            if is_valid(game_board, i, (y, x)):
                game_board[y][x] = i

                if complete_sudoku(game_board):
                    return 1
            # Backtracks if not is_valid
            game_board[y][x] = 0

        return 0


# generates a random sudoku
def generate_random_sudoku():
    #Empty board
    rand_sudoku = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    values_list = []
    filled_box = 0
    empty_box = 0
    while filled_box < 55:
        for a in values_list:
            rand_sudoku[a[0]][a[1]] = 0
        rand_sudoku[0][0] = random.randint(1, 9)
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 8)
        v = random.randint(1, 9)
        filled_box += 1
        rand_sudoku[r1][r2] = v
        values_list.append((r1, r2))
        #Backtracking
        if is_valid(rand_sudoku, rand_sudoku[r1][r2], (r1, r2)) == False:
            rand_sudoku[r1][r2] = 0
            values_list.remove((r1, r2))
            filled_box -= 1
    if complete_sudoku(rand_sudoku) != True:
        for a in values_list:
            rand_sudoku[a[0]][a[1]] = 0
        return generate_random_sudoku()
    #Sets a random amount of filled squares
    rand = random.randint(42, 50)
    while empty_box < rand:
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 8)
        if rand_sudoku[r1][r2] == 0:
            empty_box -= 1
        rand_sudoku[r1][r2] = 0
        empty_box += 1
    show_sudoku(rand_sudoku)
    return rand_sudoku

# print('incomplete sudoku\n')
# show_sudoku(sudokus[0])
# print('\ncompleted sudoku\n')
# complete_sudoku(sudokus[0])
# show_sudoku(sudokus[0])
# print('\nrandomly generated sudoku\n')
# s = generate_random_sudoku()
# print('\ncompleted randomly generated sudoku\n')
# complete_sudoku(s)
# show_sudoku(s)