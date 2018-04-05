from random import randint

r = 'red'
o = 'orange'
y = 'yellow'
g = 'green'
b = 'blue'
p = 'purple'
colors = [r, o, y, g, b, p]

class Mastermind:
	def __init__(self, choices, length):
		self.length = length
		self.choices = choices
		self.new()

	def new(self):
		self.answer = []
		for x in range(self.length):
			self.answer.append(colors[randint(0, self.choices-1)])

	def guess(self, guess):
		correct, misplaced = 0, 0
		unmatchedAnswers, unmatchedGuesses = [], []

		for x in range(self.length):
			if guess[x] == self.answer[x]: correct += 1
			else:
				unmatchedGuesses.append(guess[x])
				unmatchedAnswers.append(self.answer[x])

		for color in unmatchedGuesses:
			if color in unmatchedAnswers:
				misplaced += 1
				unmatchedAnswers.remove(color)

		print ("Correct: %d, Misplaced: %d" % (correct, misplaced))

m = Mastermind(6, 5)