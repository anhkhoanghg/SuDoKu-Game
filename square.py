import pygame

screen = pygame.display.set_mode((720, 720))
# Margins
# left margin
lm = 230
# top margin
tm = 200


class Square:

    def __init__(self,  row, column, w, h, value):
        self.row = row
        self.temp_value = 0
        self.column = column
        self.value = value
        self.w = w
        self.h = h
        self.clicked = False

    # Square Styling
    def render(self, scr):
        font = pygame.font.SysFont("Arial", 50)
        temp_font = pygame.font.SysFont("Arial", 40)
        separation = self.w / 9
        x = self.column * separation + lm
        y = self.row * separation + tm
        if self.temp_value != 0 and self.value == 0:
            output = temp_font.render(str(self.temp_value), 1, (255, 255, 255))
            scr.blit(output, (
                x + (separation / 5 - output.get_width() / 2.8), y + (separation / 1.4 - output.get_height() / 1)))
        elif self.value != 0:
            output = font.render(str(self.value), 1, (0, 0, 0))
            scr.blit(output, (
                x + (separation / 2.1 - output.get_width() / 2), y + (separation / 2.1 - output.get_height() / 2)))
        if self.clicked:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, separation, separation), 4)

    # Sets a value for the square
    def set_value(self, value):
        self.value = value

    # Sets a temporary value to the square (not commited)
    def set_temp_value(self, temp_value):
        self.temp_value = temp_value