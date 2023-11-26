import os
import pygame
from sudoku import generate_random_sudoku, show_sudoku
import tkinter as tk
from tkinter import messagebox
import time
from board import Board
from logic.AntColony import ACO_solve
from logic.BFS_solver import BFS_solve
from logic.DFS_solver import DFS_solve
from logic.UCS_solver import UCS_solve
from logic.Heuristic_solvers import a_star_solve


class Game(Board):
    # screen = pygame.display.set_mode((600, 600))
    # pygame.display.set_caption("9x1 Sudoku")
    # Allows to deselect the boxes
    prev_val = None

    def __init__(self):
        pygame.init()
        self.running, self.playing, self.counting = True, False, True
        # Difficulty menu state
        self.difficulty_state = False
        # Start section state
        self.start_state = False
        self.w, self.h = 900, 780
        self.display = pygame.Surface((self.w, self.h))
        self.window = pygame.display.set_mode((self.w, self.h))
        self.font = "8-BIT WONDER.TTF"
        self.black_font = (0, 0, 0)
        self.white_font = (255, 255, 255)
        self.board = Board(9, 9, 540, 540, Board.m1)
        self.chances = 6
        self.strikes = 0
        self.key = None
        self.menu_state = True
        # General cursor
        # avoid multiple menu selections in a row
        self.transition = False
        self.empty = None
        self.menu_bg_color = (176, 190, 197, 1)

    # Renders the window where the game takes place
    def redraw_window(self, time):
        lm = 10
        pos = pygame.mouse.get_pos()

        self.window.fill(self.menu_bg_color)
        pygame.draw.circle(self.window, (0, 0, 0, 1), (self.w - 50, 50), 30)
        pygame.draw.rect(
            self.window,
            (0, 0, 0, 1),
            pygame.Rect(self.w - 80, 50, 60, 50 * (self.chances - 1)),
        )
        pygame.draw.circle(
            self.window, (0, 0, 0, 1), (self.w - 50, 50 * (self.chances - 1) + 50), 30
        )
        fnt = pygame.font.SysFont("comicsans", 40)
        fnt2 = pygame.font.SysFont("comicsans", 40)
        # Create counting time
        time = pygame.font.SysFont("comicsans", 32).render("Time" + self.format_time(time), 1, (76, 175, 80, 1))
        # Create solve button
        solve_button = pygame.font.SysFont("comicsans", 40).render("Solve game by algorithm", 1, (0, 0, 0, 255))
        button_width = solve_button.get_width() + 60
        button_height = solve_button.get_height() + 20

        solve_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        background_button_color = (255, 255, 255)
        pygame.draw.rect(solve_button_surface, background_button_color, (0, 0, button_width, button_height), border_radius=10)

        border_color = (0, 0, 0)
        pygame.draw.rect(solve_button_surface, border_color, (0, 0, button_width, button_height), border_radius=10, width=2)
        if (    
            pos[0] > 200 and pos[0] < 200 + button_width and
            pos[1] > 655 and pos[1] < 655 + button_height
        ):
            pygame.draw.rect(solve_button_surface, (76, 175, 80), (0, 0, button_width, button_height), border_radius=10)

        # Create menu
        menu = fnt.render("M = Back to Menu", 1, (255, 255, 255, 1))
        # complete = fnt.render("Press C to complete the board", 1, (0, 0, 0, 1))
        pygame.draw.circle(self.window, (0, 0, 0, 1), (110, 920), 80)
        pygame.draw.circle(self.window, (0, 0, 0, 1), (int(self.w // 1.11), 920), 80)
        pygame.draw.rect(self.window, (0, 0, 0, 1), pygame.Rect(100, 840, 880, 160))
        # render into window
        self.window.blit(solve_button_surface, (200, 655))
        self.window.blit(solve_button, (230, 660))
        self.window.blit(time, (635, 25))
        self.window.blit(menu, (self.w // 1.65, 900))
        # self.window.blit(complete, (160, 20))
        error = fnt2.render("X ", 2, (255, 0, 0))
        chance = fnt2.render("X ", 2, (76, 175, 80, 1))
        position = []
        position2 = []
        # Updates the chances and strikes
        for i in range(self.chances):
            position2.append((self.w - 65, 10 + (i * 50) + lm))
            self.window.blit(chance, position2[i])
        for i in range(self.strikes):
            position.append((self.w - 65, 10 + (i * 50) + lm))
            self.window.blit(error, position[i])
        self.board.render(self.window)

    # Renders main menu
    def render_menu(self):
        # self.w // 2 x centered
        pos = pygame.mouse.get_pos()
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 55)
        # fnt2 = pygame.font.SysFont("8-BIT-WONDER", 35)
        # fn3 = pygame.font.SysFont("8-BIT-WONDER", 105)
        # Sudoku = fn3.render("Sudoku", 1, (255, 255, 255, 255))
        MainMenu = pygame.font.SysFont("8-BIT-WONDER", 75).render("Evil Sudoku", 1, (255, 255, 255, 255))
        Start = fnt.render("Start ", 1, (255, 255, 255, 255))
        Difficulty = fnt.render("Difficulty ", 1, (255, 255, 255, 255))
        Quit = fnt.render("Quit ", 1, (255, 255, 255, 255))

        if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 110 + 195) and (
            pos[1] > self.h // 2 + 85 - 130 and pos[1] < self.h // 2 + 85 - 130 + 60
        ):
            Start = fnt.render("Start", 1, (76, 175, 80, 1))  # 266 59
        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 240) and (
            pos[1] > self.h // 2 + 2 * 85 - 130
            and pos[1] < self.h // 2 + 2 * 85 - 130 + 60
        ):
            Difficulty = fnt.render("Difficulty", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 67 and pos[0] < self.w // 2 - 110 + 165) and (
            pos[1] > self.h // 2 + 3 * 85 - 130
            and pos[1] < self.h // 2 + 3 * 85 - 130 + 60
        ):
            Quit = fnt.render("Quit", 1, (76, 175, 80, 1))
        # self.window.blit(Sudoku, (self.w // 2 - 105, 40))
        self.window.blit(MainMenu, (self.w // 2 - 170, 125))
        self.window.blit(Start, (self.w // 2 - 70, self.h // 2 + y_const - 130))
        self.window.blit(
            Difficulty, (self.w // 2 - 110, self.h // 2 + 2 * y_const - 130)
        )
        self.window.blit(Quit, (self.w // 2 - 67, self.h // 2 + 3 * y_const - 130))

    # renders difficulty menu
    def render_difficulty(self):
        pos = pygame.mouse.get_pos()
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 55)
        Difficulty = pygame.font.SysFont("8-BIT-WONDER", 75).render("Choose number of chances ", 1, (255, 255, 255, 255))
        if self.chances == 10:
            ten_Chances = fnt.render("10 Chances ", 1, (76, 175, 80, 1))
        else:
            ten_Chances = fnt.render("10 Chances ", 1, (255, 255, 255, 255))
        if self.chances == 6:
            six_Chances = fnt.render("6 Chances ", 1, (76, 175, 80, 1))
        else:
            six_Chances = fnt.render("6 Chances ", 1, (255, 255, 255, 255))
        if self.chances == 3:
            three_Chances = fnt.render("3 Chances ", 1, (76, 175, 80, 1))
        else:
            three_Chances = fnt.render("3 Chances ", 1, (255, 255, 255, 255))
        MainMenu = fnt.render("Back ", 1, (255, 255, 255, 255))

        if (pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 320) and (
            pos[1] > self.h // 2 + 85 - 130 and pos[1] < self.h // 2 + 85 - 130 + 60
        ):
            ten_Chances = fnt.render("10 Chances ", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 290) and (
            pos[1] > self.h // 2 + 2 * 85 - 130
            and pos[1] < self.h // 2 + 2 * 85 - 130 + 60
        ):
            six_Chances = fnt.render("6 Chances ", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 290) and (
            pos[1] > self.h // 2 + 3 * 85 - 130
            and pos[1] < self.h // 2 + 3 * 85 - 130 + 60
        ):
            three_Chances = fnt.render("3 Chances ", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 315) and (
            pos[1] > self.h // 2 + 4 * 85 - 130
            and pos[1] < self.h // 2 + 4 * 85 - 130 + 60
        ):
            MainMenu = fnt.render("Back", 1, (76, 175, 80, 1))

        self.window.blit(Difficulty, (self.w // 2 - 350, 125))
        self.window.blit(ten_Chances, (self.w // 2 - 120, self.h // 2 + y_const - 130))
        self.window.blit(
            six_Chances, (self.w // 2 - 110, self.h // 2 + 2 * y_const - 130)
        )
        self.window.blit(
            three_Chances, (self.w // 2 - 110, self.h // 2 + 3 * y_const - 130)
        )
        self.window.blit(MainMenu, (self.w // 2 - 110, self.h // 2 + 4 * y_const - 130))

    # renders start
    def render_start(self):
        pos = pygame.mouse.get_pos()
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 55)
        Select = pygame.font.SysFont("8-BIT-WONDER", 75).render("Select difficulty ", 1, (255, 255, 255, 255))  # 378, 60
        # map1 = fnt.render("Sudoku 1 ", 1, (255, 255, 255, 255))  # 266 59
        # map2 = fnt.render("Sudoku 2 ", 1, (255, 255, 255, 255))  # 266 59
        # random = fnt.render("Random ", 1, (255, 255, 255, 255))  # 235 59
        
        easyLevel = fnt.render("Easy", 1, (255, 255, 255, 255))  # 266 59
        mediumLevel = fnt.render("Medium", 1, (255, 255, 255, 255))  # 266 59
        hardLevel = fnt.render("Hard", 1, (255, 255, 255, 255))  # 235 59
        expertLevel = fnt.render("Expert", 1, (255, 255, 255, 255))  # 235 59
        MainMenu = fnt.render("Back", 1, (255, 255, 255, 255))

        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 260) and (
            pos[1] > self.h // 2 + 85 - 200 and pos[1] < self.h // 2 + 85 - 200 + 60
        ):
            easyLevel = fnt.render("Easy", 1, (76, 175, 80, 1))  # 266 59
            # 76, 175, 80, 1)
        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 260) and (
            pos[1] > self.h // 2 + 85 * 2 - 200
            and pos[1] < self.h // 2 + 2 * 85 - 200 + 60
        ):
            mediumLevel = fnt.render("Medium", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 235) and (
            pos[1] > self.h // 2 + 85 * 3 - 200
            and pos[1] < self.h // 2 + 3 * 85 - 200 + 60
        ):
            hardLevel = fnt.render("Hard", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 310) and (
            pos[1] > self.h // 2 + 85 * 4 - 200
            and pos[1] < self.h // 2 + 4 * 85 - 200 + 60
        ):
            expertLevel = fnt.render("Expert", 1, (76, 175, 80, 1))
        if (pos[0] > self.w // 2 - 110 and pos[0] < self.w // 2 - 110 + 310) and (
            pos[1] > self.h // 2 + 85 * 5 - 200
            and pos[1] < self.h // 2 + 5 * 85 - 200 + 60
        ):
            MainMenu = fnt.render("Back", 1, (76, 175, 80, 1))
        self.window.blit(Select, (self.w // 2 - 200, 125))
        self.window.blit(easyLevel, (self.w // 2 - 70, self.h // 2 + y_const - 200))
        self.window.blit(mediumLevel, (self.w // 2 - 70, self.h // 2 + 2 * y_const - 200))
        self.window.blit(hardLevel, (self.w // 2 - 70, self.h // 2 + 3 * y_const - 200))
        self.window.blit(expertLevel, (self.w // 2 - 70, self.h // 2 + 4 * y_const - 200))
        self.window.blit(MainMenu, (self.w // 2 - 70, self.h // 2 + 5 * y_const - 200))

    # Stops all loops
    def close_game(self):
        self.menu_state = False
        self.running = False
        self.difficulty_state = False
        self.playing = False
        self.start_state = False

    # Displays time spent in a game
    def format_time(self, secs):
        sec = secs % 60
        
        minute = secs // 60
        time = " " + str(minute) + ":" + (str(sec) if (sec >= 10) else "0" + str(sec))
        return time

    # Manages all user inputs/ events for the playing mode
    def main_event_handler(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.START_KEY = 1

                # Back to menu
                if e.key == pygame.K_m and self.playing:
                    self.playing = False
                    self.menu_state = True

                # Inserting temporary value handler
                if e.key == pygame.K_1:
                    self.key = 1
                    self.menu_state = False
                    self.difficulty_state = False
                    self.playing = True
                if e.key == pygame.K_2:
                    self.key = 2
                if e.key == pygame.K_3:
                    self.key = 3
                if e.key == pygame.K_4:
                    self.key = 4
                if e.key == pygame.K_5:
                    self.key = 5
                if e.key == pygame.K_6:
                    self.key = 6
                if e.key == pygame.K_7:
                    self.key = 7
                if e.key == pygame.K_8:
                    self.key = 8
                if e.key == pygame.K_9:
                    self.key = 9
                if e.key == pygame.K_DELETE:
                    self.board.clear()
                    self.key = None
                # Completes Sudoku if C is pressed
                if e.key == pygame.K_c:
                    if self.playing == True:
                        while self.empty:
                            self.board.complete_GUI(self.empty)
                            if self.empty:
                                self.empty.pop(0)
                                
                        if self.board.victory_state():
                            pygame.display.update()
                            print("Game over")
                            result = messagebox.askokcancel("Game over", "You win the game. Back to menu?")
                            if result:
                                print("Back to menu")
                                self.counting = False
                                self.playing = False
                                self.menu_state = True
                                self.strikes = 0
                            else:
                                self.counting = False
                                print("Review the game")

                            
                if e.key == pygame.K_RETURN:
                    # Enter while playing handler
                    if self.playing == True:
                        i, j = self.board.clicked
                        if self.board.squares[i][j].temp_value != None:
                            if self.board.insert(self.board.squares[i][j].temp_value):
                                print("Success")
                            else:
                                print("Wrong")
                                self.strikes += 1
                            self.key = None
                            if self.board.victory_state():
                                pygame.display.update()
                                print("Game over")
                                result = messagebox.askokcancel("Game over", "You win the game. Back to menu?")
                                if result:
                                    print("Back to menu")
                                    self.counting = False
                                    self.playing = False
                                    self.menu_state = True
                                    self.strikes = 0
                                else:
                                    self.counting = False
                                    print("Review the game")
                                # Go into the start menu

                        self.transition = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.playing:
                    clicked = self.board.click(pos)
                    if clicked:
                        self.board.clicked_handler(clicked[0], clicked[1])
                        self.key = None
                # (self.w // 2 - 110, self.h // 2 + y_const - 130)
                if self.menu_state:
                    if (
                        pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 110 + 195
                    ) and (
                        pos[1] > self.h // 2 + 85 - 130
                        and pos[1] < self.h // 2 + 85 - 130 + 60
                    ):
                        self.menu_state = False
                        pos = (0, 0)
                        self.start_state = True
                    if (
                        pos[0] > self.w // 2 - 130 and pos[0] < self.w // 2 - 110 + 240
                    ) and (
                        pos[1] > self.h // 2 + 2 * 85 - 130
                        and pos[1] < self.h // 2 + 2 * 85 - 130 + 60
                    ):
                        self.menu_state = False
                        pos = (0, 0)
                        self.difficulty_state = True
                    if (
                        pos[0] > self.w // 2 - 67 and pos[0] < self.w // 2 - 110 + 165
                    ) and (
                        pos[1] > self.h // 2 + 3 * 85 - 130
                        and pos[1] < self.h // 2 + 3 * 85 - 130 + 60
                    ):
                        self.menu_state = False
                        self.running = False
                if self.difficulty_state:
                    if (
                        pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 320
                    ) and (
                        pos[1] > self.h // 2 + 85 - 130
                        and pos[1] < self.h // 2 + 85 - 130 + 60
                    ):
                        self.chances = 10
                    if (
                        pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 290
                    ) and (
                        pos[1] > self.h // 2 + 2 * 85 - 130
                        and pos[1] < self.h // 2 + 2 * 85 - 130 + 60
                    ):
                        self.chances = 6
                    if (
                        pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 290
                    ) and (
                        pos[1] > self.h // 2 + 3 * 85 - 130
                        and pos[1] < self.h // 2 + 3 * 85 - 130 + 60
                    ):
                        self.chances = 3
                    if (
                        pos[0] > self.w // 2 - 120 and pos[0] < self.w // 2 - 110 + 315
                    ) and (
                        pos[1] > self.h // 2 + 4 * 85 - 130
                        and pos[1] < self.h // 2 + 4 * 85 - 130 + 60
                    ):
                        self.difficulty_state = False
                        self.pos = None
                        self.menu_state = True
                if self.start_state:
                    print(pos)
                    if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 70 + 260) and (
                        pos[1] > self.h // 2 + 85 - 200 and pos[1] < self.h // 2 + 85 - 200 + 60):
                        random_sudoku = generate_random_sudoku("easy")
                        print("easy")
                        # solution, nodes_expand, time = ACO_solve(random_sudoku)
                        # show_sudoku(t)
                        self.board = Board(9, 9, 600, 600, random_sudoku)
                        self.empty = self.board.is_empty_game()
                        self.strikes = 0
                        self.start_state = False
                        self.counting = True
                        self.playing = True
                    if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 70 + 260) and (
                        pos[1] > self.h // 2 + 85 * 2 - 200 and pos[1] < self.h // 2 + 2 * 85 - 200 + 60):
                        random_sudoku = generate_random_sudoku("medium")
                        print("medium")
                        # t, _, _ = ACO_solve(random_sudoku)
                        # show_sudoku(t)
                        self.board = Board(9, 9, 600, 600, random_sudoku)
                        self.empty = self.board.is_empty_game()
                        self.strikes = 0
                        self.start_state = False
                        self.counting = True
                        self.playing = True
                    if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 70 + 235) and (
                        pos[1] > self.h // 2 + 85 * 3 - 200 and pos[1] < self.h // 2 + 3 * 85 - 200 + 60):
                        random_sudoku = generate_random_sudoku("hard")
                        print("hard")
                        # t, _, _ = ACO_solve(random_sudoku)
                        # show_sudoku(t)
                        self.board = Board(9, 9, 600, 600, random_sudoku)
                        self.empty = self.board.is_empty_game()
                        self.strikes = 0
                        self.start_state = False
                        self.counting = True
                        self.playing = True
                    if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 70 + 310) and (
                        pos[1] > self.h // 2 + 85 * 4 - 200 and pos[1] < self.h // 2 + 4 * 85 - 200 + 60):
                        random_sudoku = generate_random_sudoku("expert")
                        print("expert")
                        # t, _, _ = ACO_solve(random_sudoku)
                        # show_sudoku(t)
                        self.board = Board(9, 9, 600, 600, random_sudoku)
                        self.empty = self.board.is_empty_game()
                        self.strikes = 0
                        self.start_state = False
                        self.counting = True
                        self.playing = True
                    if (pos[0] > self.w // 2 - 70 and pos[0] < self.w // 2 - 70 + 310) and (
                        pos[1] > self.h // 2 + 85 * 5 - 200 and pos[1] < self.h // 2 + 5 * 85 - 200 + 60):
                        self.start_state = False
                        self.menu_state = True

    # Manages different states
    def state_handler(self):
        pygame.display.set_caption("9x9 Sudoku")
        self.key = None
        self.strikes = 0
        # General Loop
        while self.running:
            if self.playing:
                start = time.time()
                # Playing state loop
                while self.playing:
        
                    if self.counting:
                        play_time = round(time.time() - start)
                    
                    self.main_event_handler()
                    if self.board.clicked and self.key != None:
                        self.board.temp(self.key)
                    if self.chances <= self.strikes:
                        self.playing = False
                        self.menu_state = True
                        self.strikes = 0
                        pygame.display.update()
                    self.redraw_window(play_time)
                    pygame.display.update()
            # Main menu loop
            elif self.menu_state:
                while self.menu_state:
                    self.render_menu()
                    self.main_event_handler()

                    pygame.display.update()
            # Difficulty menu loop
            elif self.difficulty_state:
                while self.difficulty_state:
                    self.render_difficulty()
                    self.main_event_handler()

                    pygame.display.update()
            # Start loop
            elif self.start_state:
                while self.start_state:
                    self.render_start()
                    self.main_event_handler()

                    pygame.display.update()


g = Game()
g.state_handler()
