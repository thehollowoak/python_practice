from __future__ import print_function
from random import randint
from time import sleep
from thread import start_new_thread

LEN = 30
WID = 10
EMPTY = 13
SHOW = EMPTY+5
OFFSET = SHOW-10

class Tetramino:
	def __init__(self, map):
		self.height, self.width = len(map), len(map[0])
		self.map = map
		self.y, self.x = -1, -1

	def place(self, y, x):
		if x < 0: x = 0
		elif x > WID-self.width: x = WID-self.width

		self.y, self.x = y, x

	def fall(self, grid):
		if self.y >= LEN-self.height: return False
		if self.hasCollision(grid, self.y+1, self.x): return False

		self.y += 1
		return True

	def move(self, num, grid):
		if self.x+num < 0 or self.x+self.width+num > WID: return
		if self.hasCollision(grid, self.y, self.x+num): return

		self.x += num

	def rotate(self, grid):
		save, self.map = self.map, []
		for y in range(self.width):
			self.map.append([])
			for x in range(self.height):
				self.map[y].append(save[self.height-1-x][y])

		newY = self.y + self.height - self.width
		newX = self.x + self.width - self.height
		if newX > WID-self.height: newX = WID-self.height
		elif newX < 0: newX = 0

		if self.hasCollision(grid, newY, newX): self.map = save; return

		self.y, self.x = newY, newX
		self.height, self.width = self.width, self.height

	def hasCollision(self, grid, offsetY, offsetX):
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				if self.map[y][x] != Block.EMPTY and grid[offsetY+y][offsetX+x] != Block.EMPTY: return True
		return False

	def stop(self, grid):
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] != Block.EMPTY: grid[self.y+y][self.x+x] = self.map[y][x]

class Block:
    RED = '\033[1m\033[91mN\033[0m'
    YELLOW = '\033[1m\033[93mN\033[0m'
    GREEN = '\033[1m\033[92mN\033[0m'
    CYAN = '\033[1m\033[96mN\033[0m'
    BLUE = '\033[1m\033[94mN\033[0m'
    PURPLE = '\033[1m\033[95mN\033[0m'
    GRAY = '\033[1m\033[90mN\033[0m'
    EMPTY = '.'

colorArray = [Block.RED, Block.YELLOW, Block.GREEN, Block.CYAN, Block.BLUE, Block.PURPLE]

TETRAMINOS = [ Tetramino([[Block.RED, Block.EMPTY, Block.EMPTY],[Block.RED, Block.RED, Block.RED]]),
			   Tetramino([[Block.EMPTY, Block.YELLOW, Block.EMPTY],[Block.YELLOW, Block.YELLOW, Block.YELLOW]]),
			   Tetramino([[Block.EMPTY, Block.EMPTY, Block.GREEN],[Block.GREEN, Block.GREEN, Block.GREEN]]),
			   Tetramino([[Block.CYAN, Block.CYAN, Block.CYAN, Block.CYAN]]),
			   Tetramino([[Block.BLUE, Block.BLUE, Block.EMPTY],[Block.EMPTY, Block.BLUE, Block.BLUE]]),
			   Tetramino([[Block.EMPTY, Block.PURPLE, Block.PURPLE],[Block.PURPLE, Block.PURPLE, Block.EMPTY]]),
			   Tetramino([[Block.GRAY, Block.GRAY],[Block.GRAY, Block.GRAY]])]

class Tetris:
	def __init__(self):
		self.cont, self.paused = True, False
		self.start = 0
		self.save = TETRAMINOS[randint(0, 6)]
		self.grid = []
		for y in range(EMPTY):
			self.grid.append([Block.EMPTY]*WID)

		density = 6
		for y in range(EMPTY, LEN):
			self.grid.append([])
			if (y-EMPTY)%((LEN-EMPTY)/3) == 0: density -= 1
			self.addRow(y, density)

		start_new_thread(self.dropPieces, ())
		self.getInput()

	def addRow(self, y, density):
		for x in range(WID):
			if randint(1, density) != 1: space = colorArray[y%len(colorArray)]
			else: space = Block.EMPTY
			self.grid[y].append(space)
		
	def dropPieces(self):
		while self.cont:
			self.tetramino(randint(0, 6))
			if self.tet.y > 1: 
				self.start = self.tet.y - 13
				if self.start < 0: self.start = 0
				self.checkRows()
			else: self.cont = False

	def tetramino(self, num):
		self.tet = TETRAMINOS[num]
		self.tet.place(self.start, 4)
		self.pr()
		sleep(.8)

		while self.tet.fall(self.grid):
			self.pr()
			sleep(.8)
			while self.paused: sleep(1)
		else: self.tet.stop(self.grid)

	def checkRows(self):
		for y in range(LEN):
			fullRow = True
			for x in range(WID):
				if self.grid[y][x] == Block.EMPTY: fullRow = False
			if fullRow: self.removeRow(y)

	def removeRow(self, row):
		for y in range(row)[::-1]:
			for x in range(WID):
				self.grid[y+1][x] = self.grid[y][x]
		for x in range(WID):
			self.grid[0][x] = Block.EMPTY

	def switch(self):
		self.save, self.tet = self.tet, self.save
		self.tet.place(self.save.y, self.save.x)

	def getInput(self):
		while self.cont:
			option = raw_input("")
			if option == 'd': self.tet.move(1, self.grid)
			elif option == 'a' or option == 'q': self.tet.move(-1, self.grid)
			elif option == 'w': self.tet.rotate(self.grid)
			elif option == 's': 
				while self.tet.fall(self.grid): pass
			elif option == 'r': self.paused = not self.paused
			elif option == 'e': self.switch()
			self.pr()

	def pr(self):
		copy = [[i for i in row] for row in self.grid]
		if self.tet.y >= 0:
			for y in range(self.tet.height):
				for x in range(self.tet.width):
					if self.tet.map[y][x] != Block.EMPTY: copy[self.tet.y+y][self.tet.x+x] = self.tet.map[y][x]

		offset = self.start
		if self.tet.y > OFFSET + self.start: offset = self.tet.y - OFFSET
		if SHOW+offset > LEN: offset = LEN-SHOW
			 
		for y in range(offset, SHOW+offset):
			if y < 10: print(y, end=' |')
			else: print(y, end='|')
			print(*copy[y])
		print()

t = Tetris()

