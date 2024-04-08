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
import time


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
    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal screen
    cell: Cell
    for row in boardData:
        for cell in row:
            if cell.alive:
                color_code = f"\033[33m"
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

def countNeighbors(boardData, cell_x:int, cell_y:int) -> int:
    neighborCount = 0
    if boardData[cell_x][cell_y] is None:
        # print("No cell at " + str(cell_x) + ":" + str(cell_y))
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
        f = open("demofile2.txt", "a")
        f.write("Neighbors for " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount) + "\n")
        f.close()
    return neighborCount

def analyzeCell(boardData,cell_x,cell_y):
    outCell = Cell(boardData[cell_x][cell_y].red,boardData[cell_x][cell_y].green,boardData[cell_x][cell_y].blue,False)
    neighborCount = countNeighbors(boardData,cell_x,cell_y)
    # print("Cell count for " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount))
    f = open("demofile2.txt", "a")
    if neighborCount > 0:
        f.write(" Cell count for " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount) + "\n")
    # f.close()
    if not boardData[cell_x][cell_y].alive:
        if neighborCount == 3:
            # Revive Cell
            # print(" Reviving cell at " + str(cell_x) + ":" + str(cell_y))
            f.write("  Reviving dead cell at " + str(cell_x) + ":" + str(cell_y) + "-> neighbors:" + str(neighborCount) + "\n")
            outCell.alive = True
        # else:
            # print(" Dead cell staying dead")
            # f.write("  Dead cell staying dead\n")
    else:
        f.write("Checking underpopulated at  " + str(cell_x) + ":" + str(cell_y) + "->" + str(neighborCount) + " vs " + str(2) + "[" + str(neighborCount<2) + "]\n")
        if neighborCount < 2: # Underpopulated
            f.write("  Underpopulated cell at " + str(cell_x) + ":" + str(cell_y) + "\n")
            outCell.alive = False
        
        if neighborCount > 3: # Overpopulated
            f.write("  Overpopulated cell at " + str(cell_x) + ":" + str(cell_y) + "\n")
            outCell.alive = False

        if neighborCount == 2 or neighborCount == 3: # Stable (adding since making default cell dead)
            f.write("  Stable cell at " + str(cell_x) + ":" + str(cell_y) + " with " + str(neighborCount) + "neighbors.\n")
            outCell.alive = True
    f.close()
    return outCell

def incrementBoard(boardData):
    outBoard = [[None for _ in range(32)] for _ in range(32)]
    for y in range(32):
        for x in range(32):
            outBoard[x][y] = analyzeCell(boardData,x,y)
    return outBoard

def prepBoard(boardData):
    # GAME_board = [[Cell(0,0,0,False) for _ in range(32)] for _ in range(32)]
    # Blinker
    boardData[5][10].alive = True
    boardData[6][10].alive = True
    boardData[7][10].alive = True

    # Toad
    boardData[13][4].alive = True
    boardData[13][5].alive = True
    boardData[13][6].alive = True
    boardData[14][3].alive = True
    boardData[14][4].alive = True
    boardData[14][5].alive = True

    # Beacon
    boardData[18][7].alive = True
    boardData[18][8].alive = True
    boardData[19][7].alive = True
    boardData[19][8].alive = True
    boardData[20][9].alive = True
    boardData[20][10].alive = True
    boardData[21][9].alive = True
    boardData[21][10].alive = True

    # Glider 1
    boardData[9][14].alive = True
    boardData[10][12].alive = True
    boardData[10][14].alive = True
    boardData[11][13].alive = True
    boardData[11][14].alive = True

    # Glider 2
    boardData[1][2].alive = True
    boardData[2][3].alive = True
    boardData[3][1].alive = True
    boardData[3][2].alive = True
    boardData[3][3].alive = True
    return boardData

def printLiveCells(boardData, debug=False):
    if not debug:
        return
    f = open("demofile2.txt", "a")
    f.write("Live Cells:\n")
    for y in range(32):
        for x in range(32):
            if boardData[x][y].alive:
                f.write(" Live Cell At " + str(x) + ":" + str(y) + "\n")
    f.close()

def main():
    f = open("demofile2.txt", "w")
    f.close()
    global GAME_board
    GAME_board = prepBoard(GAME_board)
    printBoard(GAME_board)
    # draw_board()
    printLiveCells(GAME_board,True)
    while True:
        GAME_board = incrementBoard(GAME_board)
        printLiveCells(GAME_board,True)
        printBoard(GAME_board)
        time.sleep(0.5)
        # return

if __name__ == "__main__":
    main()
