import pygame
from .constants import *

class Piece():

    OUTLINE=1
    def __init__(self, row, col, color, num, SquareSize, PieceSize):
        self.row=row
        self.col=col
        self.color=color
        self.num=num
        self.SquareSize=SquareSize
        self.PieceSize=PieceSize
        self.x=0
        self.y=0
        self.calc_position()

    # izracunava x i y koordinatu gde treba da se iscrta plocica
    def calc_position(self):
        self.x=self.SquareSize*self.col+FRAME
        self.y=self.SquareSize*self.row

    # iscrtava plocicu na tabli 
    def draw(self, win):
        PADDING=(self.SquareSize-self.PieceSize)/2
        textFont=pygame.font.SysFont("consolas", 15)
        text=textFont.render(str(self.num), 5, WHITE)
        textRect = text.get_rect()
        if self.color==RED:
            pygame.draw.rect(win, self.color, (self.x+PADDING, self.y+PADDING*2, self.PieceSize, self.PieceSize*2), 0, 15)
            pygame.draw.rect(win, (180,81,44), (self.x+PADDING, self.y+PADDING*2, self.PieceSize, self.PieceSize*2), 2, 15)
            textRect.center = ((self.x+self.SquareSize//2), self.y+self.SquareSize)
            win.blit(text,textRect)
        else:
            pygame.draw.rect(win, self.color, (self.x+PADDING*2, self.y+PADDING, self.PieceSize*2, self.PieceSize), 0, 15)
            pygame.draw.rect(win, BLACK, (self.x+PADDING*2, self.y+PADDING, self.PieceSize*2, self.PieceSize), 2, 15)
            textRect.center = ((self.x+self.SquareSize), self.y+self.SquareSize//2)
            win.blit(text, textRect)
        

    def __repr__(self):
        if(self.color==RED):
            return str('V')
        else:
            return str('H')