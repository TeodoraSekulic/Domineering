import pygame
from dominacija.constants import *
from dominacija.board import Board
import PySimpleGUI as sg

## pobednik prozor


## pocetni prozor
sg.theme("Default1")

layout = [
    [sg.Text("Please enter the number of rows and columns!")],
    [sg.Text("Rows", size=(15, 1)), sg.Input(key="-ROWS-")],
    [sg.Text("Columns", size=(15, 1)), sg.Input(key="-COLS-")],
    [
        sg.Radio("PvC", "RADIO1", key="-PvC-", default=False),
        sg.Radio("PvP", "RADIO1", key="-PvP-", default=True),
        sg.Submit(),
        sg.Cancel(),
    ],
]

window = sg.Window("Setup", layout)

# na osnovu pozicije kursora misa izracunava red i kolonu u tabeli, ili ako je kliknuto van tabele vraca -1
def getRowColFromMouse(pos, ROWS, COLS): 
    SquareSize = (WIDTH - FRAME) / (ROWS if ROWS > COLS else COLS) 
    x, y = pos
    if x > FRAME and x < FRAME + COLS * SquareSize and y <= ROWS * SquareSize:
        row = int(y // SquareSize)
        col = int((x - FRAME) // SquareSize)
    else:
        row = -1
        col = -1
    return row, col


def main(ROWS, COLS, PvP):
    if ROWS > COLS:
        width = COLS * (HEIGHT / ROWS) + FRAME
        height = HEIGHT
    else:
        height = ROWS * (WIDTH / COLS) + FRAME
        width = WIDTH
    WIN = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dominacija")
    run = True
    board = Board(ROWS, COLS, PvP)
    pygame.font.init()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # dogadjaj klik misom
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = getRowColFromMouse(pos, ROWS, COLS)
                if row != -1 and col != -1:
                    board.play(row, col) # funkcija dodaje plocicu u matricu
        board.draw(WIN) # funkcija iscrtava tablu i trenutno stanje
        pygame.display.update()

        # provera pobednika
        winner = board.checkWinner()
        if winner == "Horisontal":
            layout1 = [
                [sg.Text("Horisontal player won!", key="-WINNER-")],
            ]
            windowWinner = sg.Window("Winner", layout1)
            run = True
            while run:
                event, values = windowWinner.read()
                if event.__eq__("Cancel") or event == sg.WIN_CLOSED:
                    run = False
            windowWinner.close()
        elif winner == "Vertical":
            layout1 = [
                [sg.Text("Vertical player won!", key="-WINNER-")],
            ]
            windowWinner = sg.Window("Winner", layout1)
            run = True
            while run:
                event, values = windowWinner.read()
                if event.__eq__("Cancel") or event == sg.WIN_CLOSED:
                    run = False
            windowWinner.close()

    pygame.quit()


run = True
while run:
    event, values = window.read()

    if event.__eq__("Submit") and values["-ROWS-"] != "" and values["-COLS-"] != "":
        # print(values["-ROWS-"])
        ROWS = int(values["-ROWS-"])
        COLS = int(values["-COLS-"])
        SquareSize = WIDTH // ROWS
        PieceSize = WIDTH // ROWS - 15
        window.close()
        PvP = bool(values["-PvP-"])
        main(ROWS, COLS, PvP)

    if event.__eq__("Cancel") or event == sg.WIN_CLOSED:
        run = False

window.close()
