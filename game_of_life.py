from __future__ import print_function
from random import randint
import time

class Direction:
	def __init__(self, y, x):
		self.y = y
		self.x = x

UP = Direction(-1, 0)
DOWN = Direction(1, 0)
RIGHT = Direction(0, 1)
LEFT = Direction(0, -1)
UPPER_RIGHT = Direction(-1, 1)
UPPER_LEFT = Direction(-1, -1)
LOWER_LEFT = Direction(1, -1)
LOWER_RIGHT = Direction(1, 1)
DIRECTIONS = [UP, DOWN, RIGHT, LEFT, UPPER_LEFT, UPPER_RIGHT, LOWER_RIGHT, LOWER_LEFT]

class color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    HIGHLIGHT = '\033[7m'
    END = '\033[0m'

class GameOfLife:
	def __init__(self, length):
		self.length = length
		self.grid = []
		self.copy = []
		for y in range(self.length):
			self.grid.append([' ']*length)
			self.copy.append([' ']*length)
		
		for y in range(length/4, 3*length/4):
			for x in range(length/4, length/2):
				if randint(1,3) == 1: 
					self.grid[y][x] = color.RED + '*' + color.END
					self.grid[y][length-1-x] = color.RED + '*' + color.END

		while True:
			self.pr(self.grid)
			if self.propigate(self.copy, self.grid): break
			time.sleep(.8)
			self.pr(self.copy)
			if self.propigate(self.grid, self.copy): break
			time.sleep(.8)

	def propigate(self, grid, copy):
		same = True
		for y in range(self.length):
			for x in range(self.length):
				save = grid[y][x]
				liveCells = 0

				for d in DIRECTIONS:
					if y+d.y < self.length and y+d.y >= 0 and x+d.x < self.length and x+d.x >= 0:
						if '*' in copy[y+d.y][x+d.x]: liveCells += 1

				if copy[y][x] == ' ':
					if liveCells == 3: grid[y][x] = color.RED + '*' + color.END
					else: grid[y][x] = ' '
				elif liveCells < 2 or liveCells > 3: grid[y][x] = ' '
				elif color.RED in copy[y][x]: grid[y][x] = color.YELLOW + '*' + color.END
				elif color.YELLOW in copy[y][x]: grid[y][x] = color.GREEN + '*' + color.END
				elif color.GREEN in copy[y][x]: grid[y][x] = color.CYAN + '*' + color.END
				else: grid[y][x] = color.PURPLE + '*' + color.END

				if grid[y][x] != save: same = False
		return same

	def pr(self, grid):
		for y in range(self.length):
			print(*grid[y])
		print()

g = GameOfLife(30)

