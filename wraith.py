from __future__ import print_function
from random import choice

LEN = 7
CHOICES = 'O!#&=^.'
MAX_MOVES = 6
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

class WraithGame:
	def __init__(self):
		self.grid = []
		for y in range(LEN):
			self.grid.append([])
			for x in range(LEN):
				self.grid[y].append(choice(CHOICES))

		while self.findMatches():
			self.removeMatches()
		self.score = 0
		self.moves = MAX_MOVES
		self.pr()

	def click(self, row, x):
		self.moves -= 1
		for y in range(row)[::-1]:
			self.grid[y+1][x] = self.grid[y][x]
		self.grid[0][x] = choice(CHOICES)
		self.pr()

		while self.findMatches():
			if self.moves > MAX_MOVES: self.moves = MAX_MOVES
			self.pr()
			self.removeMatches()
			self.pr()
		if self.moves <= 0: print("Game Over")

	def pr(self):
		print('   ', end='')
		for x in range(LEN): print(x, end='_')
		print()
		for y in range(LEN):
			if y < 10: print(y, end=' |')
			else: print(y, end='|')
			print(*self.grid[y])

w = WraithGame()

