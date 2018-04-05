from __future__ import print_function
from random import randint

class Minesweeper:
	def __init__(self, rows, cols):
		self.answer_grid = []
		self.player_grid = []
		for y in range(rows):
			self.answer_grid.append([])
			self.player_grid.append([])
			for x in range(cols):
				if randint(1,4) == 1: 
					self.answer_grid[y].append(9)
				else:
					self.answer_grid[y].append(0)
				self.player_grid[y].append('.')
		for y in range(rows):
			for x in range(cols):
				if self.answer_grid[y][x] > 8:
					self.around(y, x, self.add)
		for y in range(rows):
			for x in range(cols):
				if self.answer_grid[y][x] > 8:
					self.answer_grid[y][x] = '*'
		self.pr()

	def around(self, y, x, func):
		for a in range(-1, 2):
			for b in range(-1, 2):
				if y+a >= 0 and y+a < len(self.answer_grid) and x+b >= 0 and x+b < len(self.answer_grid[y]):
					func(y+a, x+b)

	def click(self, y, x):
		self.player_grid[y][x] = self.answer_grid[y][x]
		if self.player_grid[y][x] == 0:
			self.around(y, x, self.spreadZeros)
		self.pr()
		if self.answer_grid[y][x] == '*': print("You lose!")
		elif self.player_grid == self.answer_grid: print("You win!")

	def mark(self, y, x):
		self.player_grid[y][x] = '*'
		self.pr()
		if self.player_grid == self.answer_grid: print("You win!")

	def pr(self):
		print('   ', end='')
		for x in range(len(self.player_grid[0])):
			if x < 10: print(x, end='__')
			else: print(x, end='_')
		print()
		for y in range(len(self.player_grid)):
			if y < 10: print(y, end=' |')
			else: print(y, end='|')
			print(*self.player_grid[y])

	def add(self, y, x):
		self.answer_grid[y][x] += 1

	def spreadZeros(self, y, x):
		if self.player_grid[y][x] == '.':
			self.player_grid[y][x] = self.answer_grid[y][x]
			if self.answer_grid[y][x] == 0:
				self.around(y, x, self.spreadZeros)





