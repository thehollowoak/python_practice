from __future__ import print_function
from time import sleep
from thread import start_new_thread
from mon import *
from maze import *

class color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

class MonTD:
	i = 0
	def __init__(self, rows, cols):
		self.maze = Maze(rows, cols)
		self.solver = MazeSolver(self.maze)
		self.mons = []
		self.enemyMons = [Mon(4,1), Mon(5,1), Mon(6,1), Mon(7,1)]
		self.printMap()
		start_new_thread(self.monsAttack, ())

	def marchMons(self):
		while True:
			self.printMap()
			sleep(1.2)
			for mon in self.enemyMons:
				if not hasattr(mon, 'x'):
					mon.y, mon.x = 0, self.maze.start
					break
				num = self.solver.map[mon.y][mon.x]
				for dir in Directions:
					if self.solver.map[mon.y+dir[0]][mon.x+dir[1]] < num:
						mon.y += dir[0]
						mon.x += dir[1]
						break
				for enemy in self.mons:
					if self.attack(mon, enemy): break

	def monsAttack(self):
		while True:
			sleep(.8)
			for mon in self.mons:
				for enemy in self.enemyMons:
					if hasattr(enemy, 'x'):
						if self.attack(mon, enemy): break

	def attack(self, mon, enemy):
		difY, difX = enemy.y-mon.y, enemy.x-mon.x
		if difY <= 1 and difY >= -1 and difX <= 1 and difX >= -1:
			mon.attack(enemy)
			if enemy.hp <= 0: self.faints(enemy)
			return True
		return False

	def faints(self, mon):
		if mon in self.mons: self.mons.remove(mon)
		elif mon in self.enemyMons: self.enemyMons.remove(mon)

	def placeMon(self, mon, row, col):
		if (row<=1 and col==self.maze.start) or (row>=self.maze.rows-2 and col==self.maze.end): return False
		self.maze.map[row][col] = EXIT

		if self.maze.map[row][col] != WALL:
			self.i += 1
			self.maze.markPath(1, self.maze.start, self.i)
			if self.maze.map[1][self.maze.start] != self.maze.map[self.maze.rows-2][self.maze.end]:
				self.maze.map[row][col] = self.i
				return False
			self.solver.map[row][col] = WALL
			self.solver.solve()

		# if mon already there, should return false or replace old mon?
		mon.y, mon.x = row, col
		self.mons.append(mon)
		self.printMap()
		return True

	def printMap(self):
		copy = [[removeNum(i) for i in row] for row in self.maze.map]
		for mon in self.mons:
			if mon.totalHp()/mon.hp < 2: c = color.GREEN
			elif mon.totalHp()/mon.hp < 3: c = color.YELLOW
			else: c = color.RED
			copy[mon.y][mon.x] = c + 'M' + color.END
		for mon in self.enemyMons:
			if hasattr(mon, 'x'):
				if mon.totalHp()/mon.hp < 2: c = color.GREEN
				elif mon.totalHp()/mon.hp < 3: c = color.YELLOW
				else: c = color.RED
				copy[mon.y][mon.x] = c + 'O' + color.END
		print()
		for y in range(self.maze.rows):
			print(*copy[y])

def removeNum(i):
	if type(i) is int: return ' '
	return i

m = MonTD(13,13)
# m.placeMon(Mon(1,1),)
# m.marchMons()



