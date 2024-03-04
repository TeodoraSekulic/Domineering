import pygame
from .piece import Piece
from .constants import *
import PySimpleGUI as sg
import copy


class Board:
    def __init__(self, ROWS, COLS, PvP):
        self.board = []
        self.selected = None
        self.player = 0  # 0 vertikalni igrac, 1 horizontalni igrac
        self.COLS = COLS
        self.ROWS = ROWS
        self.PvP = PvP  # ako je true onda je PvP ako je false onda je PvC
        self.num = 1
        self.possibleTables= []
        self.create_board()

    def draw_squares(self, win):
        SquareSize = (WIDTH - FRAME) / (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        )
        win.fill(WHITE)
        pygame.draw.rect(
            win, GRAY, (FRAME, 0, self.COLS * SquareSize, self.ROWS * SquareSize), 2
        )
        for row in range(self.ROWS):
            for col in range(
                row % 2, self.COLS, 2
            ):  # da li red krece belom ili crnoom bojom
                pygame.draw.rect(
                    win,
                    GRAY,
                    (
                        col * SquareSize + FRAME,
                        row * SquareSize,
                        SquareSize,
                        SquareSize,
                    ),
                )

    # kreira matricu koja cuva stanje table
    def create_board(self):
        for row in range(self.ROWS):
            self.board.append([])
            for col in range(self.COLS):
                self.board[row].append(0)


    def draw(self, win):
        SquareSize = (WIDTH - FRAME) / (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        )
        self.draw_squares(win)
        textFont = pygame.font.SysFont("consolas", 15)
        for i in range(self.ROWS):
            text = textFont.render(str(self.ROWS - i), 1, BLACK)
            textRect = text.get_rect()
            textRect.center = ((FRAME // 2), i * SquareSize + SquareSize // 2)
            win.blit(text, textRect)
        for i in range(self.COLS):
            text = textFont.render(chr(97 + i), 1, BLACK)
            textRect = text.get_rect()
            textRect.center = (
                FRAME + i * SquareSize + SquareSize // 2,
                self.ROWS * SquareSize + FRAME // 2,
            )
            win.blit(text, textRect)

        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != 0 :
                    piece.draw(win)

    def play(self, row, col):

        SquareSize = (WIDTH - FRAME) / (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        )
        PieceSize = (WIDTH - FRAME) // (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        ) - SquareSize // 4

        # provera za vertikalno
        if checkVertical(self, row, col) == True:
            return
        # provera za horizontalno
        if checkHorizontal(self, row, col) == True:
            return
        if (
            # vertikalni igrac
            self.player == 0
            and self.board[row][col] == 0
            and self.board[row - 1][col] == 0
        ):
            piece = Piece(row - 1, col, RED, self.num, SquareSize, PieceSize)
            self.num += 1
            self.board[row][col] = piece
            self.board[row - 1][col] = piece
            self.player = 1
        elif (
            # horizontalni igrac
            self.player == 1
            and self.board[row][col] == 0
            and self.board[row][col + 1] == 0
        ):
            piece = Piece(row, col, LIGHTBLACK, self.num, SquareSize, PieceSize)
            self.num += 1
            self.board[row][col] = piece
            self.board[row][col + 1] = piece
            self.player = 0
        # print(self.board)

        # stampa sve poteze sledeceg igraca
        self.possibleTables=[[]]
        self.allAvailablePositions()
        print("------Next available tables------")
        if(len(self.possibleTables)>1):
            for i in range(len(self.possibleTables)-1):
                oneBoard=self.possibleTables.pop()
                print("------Next possible play------")
                for j in range(self.ROWS):
                    print(oneBoard[j])

    def checkWinner(self):
        if self.player == 0:  # 0 vertikalno
            freePlaces = 0
            havePlacesVertical = False
            for i in range(self.COLS):
                if havePlacesVertical == True:
                    break
                for j in range(self.ROWS - 1):
                    if self.board[j][i] == 0 and self.board[j + 1][i] == 0:
                        freePlaces += 1
                if freePlaces >= 1:
                    havePlacesVertical = True
                    break
                freePlaces = 0
            if havePlacesVertical == False:
                return "Horisontal"

        if self.player == 1:  # 1 horizontalno
            freePlaces = 0
            havePlacesHorisontal = False
            for i in range(self.ROWS):
                if havePlacesHorisontal == True:
                    break
                for j in range(self.COLS - 1):
                    if self.board[i][j] == 0 and self.board[i][j + 1] == 0:
                        freePlaces += 1
                if freePlaces >= 1:
                    havePlacesHorisontal = True
                    break
                freePlaces = 0
            if havePlacesHorisontal == False:
                return "Vertical"

    def allAvailablePositions(self):
        SquareSize = (WIDTH - FRAME) / (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        )
        PieceSize = (WIDTH - FRAME) // (
            self.ROWS if self.ROWS > self.COLS else self.COLS
        ) - SquareSize // 4
        
        if self.player == 0:  # 0 vertikalno
            for i in range(self.COLS):
                for j in range(self.ROWS - 1):
                    if self.board[j][i] == 0 and self.board[j + 1][i] == 0:
                        table=copy.deepcopy(self.board)

                        piece = Piece(j - 1, i, RED, self.num, SquareSize, PieceSize)
                        table[j][i] = piece
                        table[j+1][i] = piece

                        self.possibleTables.append(table)

        if self.player == 1:  # 1 horizontalno
            for i in range(self.ROWS):
                for j in range(self.COLS - 1):
                    if self.board[i][j] == 0 and self.board[i][j + 1] == 0:
                        table=copy.deepcopy(self.board)

                        piece = Piece(i, j, LIGHTBLACK, self.num, SquareSize, PieceSize)
                        table[i][j] = piece
                        table[i][j + 1] = piece

                        self.possibleTables.append(table)
        return


def checkVertical(self, row, col):
    if self.player == 0 and row == 0:
        return True
    return False


def checkHorizontal(self, row, col):
    if self.player == 1 and col + 1 == self.COLS:
        return True
    return False
