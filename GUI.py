# GUI.py
import pygame
from board import board2
import time
from random import sample
pygame.font.init()


class Grid:
    board = board2
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)


    def solve_gui(self):
        found = next_empty(self.model)
        if not found:##base case, if can't find a val thats empty, game over, yay
            return True
        else:
            row, col = found##sets vals of next empty coordinate

        for i in range(1, 10):##loops through all possible values in sudoku 1-9
            if valid_board(self.model, i, (row, col)):##checks validity of current value
                self.model[row][col] = i##if works, sets that position with value i
                self.cubes[row][col].set(i)##update all other values
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(75)

                if self.solve_gui():##recursively try to solve board with new value added, you will either get every sol, or something wont be valid
                    return True

                self.model[row][col] = 0##now back track and say the last element must be wrong, so set it to 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(75)

        return False##when not valid, returns false, so will send you back to line 129


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val



def next_empty(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid_board(b, var, pos): ##b is board, var is number we place at certain position pos. pos = [row, col]
    
    #check row
    for i in range(len(b)):
        if(b[pos[0]][i] == var and pos[1] != i): ##checks each element in row to see if == num. if pos checking is the one just inserted, won't need to check
            return False

    #check col
    for i in range(len(b)):
        if(b[i][pos[1]] == var and pos[0] != i): ##checks each element in col to see if == num. if pos checking is the one just inserted, won't need to check
            return False

    #check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3): ##box's y coord * 3 gives it back in terms of pos, each box is 3x3, so range is from starting y val to y val + 3
        for j in range(box_x * 3, box_x * 3 + 3): ##box's x coord * 3 gives it back in terms of pos, each box is 3x3, so range is from starting x val to x val + 3
            if(b[i][j] == var and (i,j) != pos):
                return False

    return True

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
        win.fill((255,255,255))
        board.draw()
        pygame.display.update()


main()
pygame.quit()
