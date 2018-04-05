from __future__ import print_function
from random import shuffle
import time

LEN = 8
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
Players = ('X', 'O')

class Othello:
	def __init__(self):
		self.grid = []
		for y in range(LEN):
			self.grid.append(['.']*LEN)
		self.grid[4][4], self.grid[3][3] = Players[0], Players[0]
		self.grid[4][3], self.grid[3][4] = Players[1], Players[1]

		self.pr()

	def click(self, y, x):
		if self.grid[y][x] == '.':
			valid = False
			for d in DIRECTIONS:
				if self.turnToken(y+d.y, x+d.x, d, 0, False): valid = True

			if valid:
				self.grid[y][x] = Players[0]
				self.pr()
				time.sleep(1)
				self.opponentsTurn()

	def opponentsTurn(self):
		rand, rand2 = range(LEN), range(LEN)
		shuffle(rand)
		shuffle(rand2)
		for y in rand:
			for x in rand2:
				if self.grid[y][x] == '.':
					valid = False
					for d in DIRECTIONS:
						if self.turnToken(y+d.y, x+d.x, d, 1, False): valid = True
					if valid:
						self.grid[y][x] = Players[1]
						self.pr()
						self.endGame()
						return
		self.endGame()

	def turnToken(self, y, x, d, player, run):
		if y < LEN and y >= 0 and x < LEN and x >= 0:
			if self.grid[y][x] == Players[player]: return run
			elif self.grid[y][x] == Players[1-player]:
				if self.turnToken(y+d.y, x+d.x, d, player, True):
					self.grid[y][x] = Players[player]
					return True
		return False

	def endGame(self):
		playerTotal, oppTotal = 0, 0
		for row in self.grid:
			if row.count('.') > 0: return
			playerTotal += row.count(Players[0])
			oppTotal += row.count(Players[1])
		print("Game Over! Player Total: %d, CP Total: %d" % (playerTotal, oppTotal))

	def pr(self):
		print('   ', end='')
		for x in range(LEN): print(x, end='_')
		print()
		for y in range(LEN):
			if y < 10: print(y, end=' |')
			else: print(y, end='|')
			print(*self.grid[y])

o = Othello()

