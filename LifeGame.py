#  Conways Game Of Life in Python
#  THPDG 2024

# Rules Reference:
# Any live cell with fewer than two live neighbors dies, as if by underpopulation.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by overpopulation.
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

import os
import sys
import random
import i75Support


class Cell:
    def __init__(self, red=0, green=0, blue=0, alive=False):
        self.red = red
        self.green = green
        self.blue = blue
        self.alive = alive

    def __str__(self):
        if self.alive:
            return "X"
        return " "

GAME_board = [[Cell(0,0,0,False) for _ in range(32)] for _ in range(32)]
LED_board = [[Cell(0,0,0,False) for _ in range(32)] for _ in range(32)]

def printBoard(boardData):
    # os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    cell: Cell
    for row in boardData:
        for cell in row:
            if cell.alive:
                color_code = f"\033[31m"
            else:
                color_code = f"\033[30m"
            print(f"{color_code}█\033[0m", end='')  # Print colored block
        print()

def draw_board():
    # os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    for y in range(32):
        for x in range(32):
            cell = LED_board[x][y]
            # Convert RGB values to ANSI escape color codes
            color_code = f"\033[38;2;{cell.red};{cell.green};{cell.blue}m"
            print(f"{color_code}■\033[0m", end='')  # Print colored block
        print()  # Move to the next line after printing a row

def countNeighbors(boardData, cell:Cell, cell_x:int, cell_y:int) -> int:
    neighborCount = 0
    if cell is None:
        print("No cell at " + str(cell_x) + ":" + str(cell_y))
        return neighborCount
    
    for x in [cell_x-1,cell_x,cell_x+1]:
        for y in [cell_y-1,cell_y,cell_y+1]:
            if cell_x == x and cell_y == y:
                continue
            if x >= 32:
                continue
            if y >= 32:
                continue
            if boardData[x][y].alive:
                neighborCount += 1
    if neighborCount > 0:
        print("Neighbors for " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount))
    return neighborCount

def analyzeCell(boardData, cell:Cell,cell_x,cell_y):
    neighborCount = countNeighbors(boardData, cell,cell_x,cell_y)
    print("Cell count for " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount))
    if not cell.alive:
        if neighborCount == 3:
            # Revive Cell
            print(" Reviving cell at " + str(cell_x) + ":" + str(cell_y))
            cell.alive = True
        else:
            print("Dead cell staying dead")
    else:
        print("Checking underpopulated at  " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount) + " vs " + str(2) + "[" + str(neighborCount<2) + "]")
        if neighborCount < 2: # Underpopulated
            print(" Underpopulated cell at " + str(cell_x) + ":" + str(cell_y))
            cell.alive = False
        
        if neighborCount > 3: # Overpopulated
            print(" Overpopulated cell at " + str(cell_x) + ":" + str(cell_y))
            cell.alive = False
    return cell

def incrementBoard(boardData):
    cell: Cell
    outBoard = [[None for _ in range(32)] for _ in range(32)]
    for y in range(32):
        for x in range(32):
            cell = boardData[x][y]
            outBoard[x][y] = analyzeCell(boardData, cell,x,y)
    return outBoard

def prepBoard(boardData):
    # GAME_board = [[Cell(0,0,0,False) for _ in range(32)] for _ in range(32)]
    boardData[5][10].alive = True
    boardData[6][10].alive = True
    boardData[7][10].alive = True
    return boardData

def main():
    global GAME_board
    GAME_board = prepBoard(GAME_board)
    printBoard(GAME_board)
    # draw_board()

    while True:
        GAME_board = incrementBoard(GAME_board)
        printBoard(GAME_board)
        return

if __name__ == "__main__":
    main()
