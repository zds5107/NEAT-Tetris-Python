import pygame
from colors import Colors

class Board:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.board = [[0 for j in range(self.num_cols)] for i in range(self.num_rows) ]
        self.cell_size = 30
        self.colors = Colors.get_colors()

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.board[row][column]
                cell_rect = pygame.Rect(column*self.cell_size+1, row*self.cell_size+1, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.colors[cell_value],cell_rect)