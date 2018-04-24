from __future__ import print_function
from random import randint
from random import randrange

EMPTY = ' '
WALL = '\033[1m\033[90m#\033[0m'
EXIT = '.'
Directions = [[1, 0], [0, 1], [0, -1], [-1, 0]]

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map = []
        self.map.append([WALL]*cols)
        for row in range(2, rows):
            if row%2 == 0: self.map.append([WALL]+[EMPTY]*(cols-2)+[WALL])
            else: self.map.append([WALL]+[EMPTY, WALL]*(cols/2))
        self.map.append([WALL]*cols)

        for i in range(rows*cols/5):
            row = randint(1, rows-2)
            col = randint(1, cols-2)
            if row%2 == col%2: 
                if col == cols-2: col -= 1
                else: col += 1
            if self.map[row][col] != WALL:
                self.map[row][col] = WALL
                if self.blocksPath(row, col, i):
                    self.map[row][col] = i
                
        self.markPath(1, 1, EMPTY)
        self.start = randrange(1, cols, 2)
        self.end = randrange(1, cols, 2)
        self.map[0][self.start] = EXIT
        self.map[rows-1][self.end] = EXIT
        # self.printMap()
    
    def blocksPath(self, row, col, i):
        paths = []
        for dir in Directions:
            if self.map[row+dir[0]][col+dir[1]] != WALL:
                paths.append([row+dir[0], col+dir[1]])

        # makes no dead ends
        for path in paths:
            walls = 0
            for dir in Directions:
                if self.map[path[0]+dir[0]][path[1]+dir[1]] == WALL: walls += 1
            if walls > 2: return True
        # # # # #
            
        self.markPath(paths[0][0], paths[0][1], i)
        return self.map[paths[0][0]][paths[0][1]] != self.map[paths[1][0]][paths[1][1]]
    
    def markPath(self, row, col, i):
        self.map[row][col] = i
        for dir in Directions:
            space = self.map[row+dir[0]][col+dir[1]]
            if space != WALL and space != i and space != EXIT:
                self.markPath(row+dir[0], col+dir[1], i)
            
    def printMap(self):
        for y in range(self.rows):
            print(*self.map[y])

class MazeSolver:

    def __init__(self, maze):
        self.start = maze.start
        self.end = maze.end
        self.map = [[i for i in row] for row in maze.map]
        self.solve()

    def solve(self):
        self.removeNumbers()
        self.countPath(len(self.map)-2, self.end, 1)
        # self.markPath(1, self.start)
        # self.printMap()

    def countPath(self, row, col, i):
        if self.map[row][col] > i: 
            self.map[row][col] = i
            for dir in Directions:
                if self.map[row+dir[0]][col+dir[1]] == EMPTY or type(self.map[row+dir[0]][col+dir[1]]) is int:
                    self.countPath(row+dir[0], col+dir[1], i+1)

    # def markPath(self, row, col):
    #     i = self.map[row][col]
    #     self.map[row][col] = self.PATH
    #     for dir in Directions:
    #         if self.map[row+dir[0]][col+dir[1]] < i:
    #             self.markPath(row+dir[0], col+dir[1])
    #             return

    def removeNumbers(self):
        for row in self.map:
            for x in range(len(row)):
                if type(row[x]) is int:
                    row[x] = EMPTY

    def printMap(self):
        for y in range(len(self.map)):
            print(*self.map[y])





