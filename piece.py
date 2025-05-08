import pygame
from colors import Colors

class Piece:
    def __init__(self, id):
        self.cell_size = 30
        self.id= id
        self.color = Colors.get_colors()[id]
        self.rotate_state=0
        self.lr_align=False

    def draw(self, screen):
        for cord in self.cords:
                piece_rect = pygame.Rect(cord[0]*self.cell_size+1, cord[1]*self.cell_size+1, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.color ,piece_rect)

    def rotate(self):

        newcords = self.cords[:]
        xn = newcords[1][0]
        yn = newcords[1][1]

        for i in range(4):
            newX = newcords[i][0] - xn
            newY = newcords[i][1] - yn
            newcords[i] = [-1*newY+xn, newX+yn]

        return newcords