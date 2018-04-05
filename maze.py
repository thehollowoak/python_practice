from random import randint

class Maze:
    EMPTY = '  '
    WALL = '# '
    Directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map = []
        self.map.append([self.WALL]*cols)
        for row in range(2, rows):
            if row%2 == 0: self.map.append([self.WALL]+[self.EMPTY]*(cols-2)+[self.WALL])
            else: self.map.append([self.WALL]+[self.EMPTY, self.WALL]*(cols/2))
        self.map.append([self.WALL]*cols)

        for i in range(rows*cols/3):
            row = randint(1, rows-2)
            col = randint(1, cols-2)
            if row%2 == col%2: 
                if col == cols-2: col -= 1
                else: col += 1
            if self.map[row][col] != self.WALL:
                self.map[row][col] = self.WALL
                if self.blocksPath(row, col, i):
                    self.map[row][col] = i
                
        self.markPath(1, 1, self.EMPTY)
        self.printMap()
    
    def blocksPath(self, row, col, i):
        paths = []
        for dir in self.Directions:
            if self.map[row+dir[0]][col+dir[1]] != self.WALL:
                paths.append([row+dir[0], col+dir[1]])
            
        self.markPath(paths[0][0], paths[0][1], i)
        return self.map[paths[0][0]][paths[0][1]] != self.map[paths[1][0]][paths[1][1]]
    
    def markPath(self, row, col, i):
        self.map[row][col] = i
        for dir in self.Directions:
            if self.map[row+dir[0]][col+dir[1]] != self.WALL and self.map[row+dir[0]][col+dir[1]] != i:
                self.markPath(row+dir[0], col+dir[1], i)
            
    def printMap(self):
        for row in self.map:
            print(''.join(row))



