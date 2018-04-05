from __future__ import print_function
from random import randint

LEN = 4

class Direction:
	def __init__(self, y, x, end):
		self.y = y
		self.x = x
		self.end = end

UP = Direction(-1, 0, lambda row, col: row>0)
DOWN = Direction(1, 0, lambda row, col: row<LEN-1)
RIGHT = Direction(0, 1, lambda row, col: col<LEN-1)
LEFT = Direction(0, -1, lambda row, col: col>0)

class NumberGame:
	def __init__(self):
		self.score = 0
		self.grid = []
		for row in range(LEN):
			self.grid.append([' ']*LEN)
		self.addToGrid(LEN*LEN)

	def addToGrid(self, count):
		count = randint(1, count)
		num = randint(1,4)
		if num != 2: num = 1
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				if self.grid[row][col] == ' ': 
					if count <= 1: 
						self.grid[row][col] = num
						self.pr()
						return
					else: count -= 1

	def countEmptySpaces(self):
		count = 0
		for row in self.grid:
			count += row.count(' ')

		if count == 0:
			for row in range(LEN):
				for col in range(LEN):
					matchDown = row+1 < LEN and self.grid[row][col] == self.grid[row+1][col]
					matchRight = col+1 < LEN and self.grid[row][col] == self.grid[row][col+1]
					if matchDown or matchRight: return 0
			print("Game Over! Score: %d" % self.score)

		return count

	def turn(self, direction):
		copy = [row[:] for row in self.grid]
		reverse = -(direction.y + direction.x)

		for row in range(LEN)[::reverse]:
			for col in range(LEN)[::reverse]:
				if self.grid[row][col] != ' ':
					self.move(row, col, direction)

		for row in range(LEN):
			for col in range(LEN):
				if self.grid[row][col] == '.':
					self.grid[row][col] = ' '

		count = self.countEmptySpaces()
		if copy != self.grid: self.addToGrid(count)

	def move(self, row, col, dir):
		while dir.end(row, col):
			next = self.grid[row+dir.y][col+dir.x]
			if next == ' ' or next == '.':
				self.grid[row+dir.y][col+dir.x] = self.grid[row][col]
				self.grid[row][col] = ' '
				row += dir.y
				col += dir.x
				if next == '.': return
			elif next == self.grid[row][col]:
				self.grid[row+dir.y][col+dir.x] = next+1
				self.grid[row][col] = '.'
				self.score += 2**(next+1)
				return
			else: break

	def pr(self):
		print('+' + '-'*(3*LEN) + '+')
		for row in self.grid:
			prow = []
			for a in row:
				if len(str(a)) > 1: prow.append(str(a))
				else: prow.append(" " + str(a))
			print('|' + " ".join(prow) + ' |')
		print('+' + '-'*(3*LEN) + '+')

n = NumberGame()
user = raw_input("")
while user != 'exit':
	if user == 'w': n.turn(UP)
	elif user == 'd': n.turn(RIGHT)
	elif user == 's': n.turn(DOWN)
	elif user == 'a': n.turn(LEFT)
	user = raw_input("")
