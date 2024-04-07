#  Conways Game Of Life in Python
#  THPDG 2024

import os
import sys
import random
import i75Support

GAME_board = [[[1, 0, 0] for _ in range(32)] for _ in range(32)]
LED_board = [[[255, 255, 255] for _ in range(32)] for _ in range(32)]

def printBoard(boardData):
    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    for row in boardData:
        for r,g,b in row:
            if r:
                color_code = f"\033[31m"
            else:
                color_code = f"\033[30m"
            print(f"{color_code}█\033[0m", end='')  # Print colored block
        print()

def draw_board():
    # os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    for y in range(32):
        for x in range(32):
            r, g, b = LED_board[x][y]
            # Convert RGB values to ANSI escape color codes
            color_code = f"\033[38;2;{r};{g};{b}m"
            print(f"{color_code}■\033[0m", end='')  # Print colored block
        print()  # Move to the next line after printing a row

def countNeighbors(boardData, cell) -> int:
    neighborCount = 0
    if cell is None:
        return neighborCount
    if cell.value == 0:
        return neighborCount
    if boardData[cell.x-1][cell.y].value == 1:
        neighborCount += 1
    if boardData[cell.x+1][cell.y].value == 1:
        neighborCount += 1
    if boardData[cell.x][cell.y-1].value == 1:
        neighborCount += 1
    if boardData[cell.x][cell.y+1].value == 1:
        neighborCount += 1
    return neighborCount

def analyzeCell(cell):
    pass


def main():
    printBoard(GAME_board)
    # draw_board()

if __name__ == "__main__":
    main()
