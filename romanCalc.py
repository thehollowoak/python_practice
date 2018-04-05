import unittest
from collections import OrderedDict

def convertion(operation):
	def new(self, a, b, *others):
		a = self._expandOneLess(a)
		b = self._expandOneLess(b)
		answer = operation(self, a, b, *others)
		if others: answer = new(self, answer, *others)
		return self._combine(answer)
	return new

class RomanCalc:

	letters = ['L', 'X', 'V', 'I']
	convert = OrderedDict([('IIIII','V'), ('VV','X'), ('XXXXX','L')])
	oneLess = OrderedDict([('XXXX','XL'), ('VIIII','IX'), ('IIII','IV')])

	@convertion
	def plus(self, a, b, *others):
		return self._sort(a+b)

	@convertion
	def minus(self, a, b, *others):
		for each in b:
			a = self._borrow(a, each)
			a = a.replace(each, '', 1)
		return a

	@convertion
	def multiply(self, a, b, *others):
		multiplier = b.count('I') + b.count('V')*5 + b.count('X')*10 + b.count('L')*50
		a = a * multiplier
		return self._sort(a)

	@convertion
	def divide(self, a, b, *others):
		answer = ''
		divisor = b.count('I') + b.count('V')*5 + b.count('X')*10 + b.count('L')*50
		for letter in self.letters:
			if letter in a:
				if a.count(letter)%divisor == 0:
					answer += letter * (a.count(letter)/divisor)
				else:
					a = self._expand(a, letter)
		return answer


	def _sort(self, number):
		answer = ''
		for letter in self.letters:
			answer += letter * (number).count(letter)
		return answer

	def _borrow(self, answer, letter):
		if not letter in answer:
			nextLetter = self.letters[self.letters.index(letter)-1]
			answer = self._borrow(answer, nextLetter)
			replacement = self.convert.keys()[self.convert.values().index(nextLetter)]
			answer = answer.replace(nextLetter, replacement, 1)
		return self._sort(answer)

	def _expand(self, answer, letter):
		replacement = self.convert.keys()[self.convert.values().index(letter)]
		return answer.replace(letter, replacement)

	def _expandOneLess(self, number):
		for key, value in self.oneLess.items():
			number = number.replace(value, key)
		return number

	def _combine(self, answer):
		for key, value in self.convert.items():
			answer = answer.replace(key, value)
		for key, value in self.oneLess.items():
			answer = answer.replace(key, value)
		return answer


class TestStringMethods(unittest.TestCase):

	calc = RomanCalc()

	def test_add_concatinates(self):
		self.assertEqual(self.calc.plus('I', 'I'), 'II')
		self.assertEqual(self.calc.plus('II', 'I'), 'III')
		self.assertEqual(self.calc.plus('X', 'V'), 'XV')
		self.assertEqual(self.calc.plus('XX', 'X'), 'XXX')

	def test_add_ordersByValue(self):
		self.assertEqual(self.calc.plus('I', 'X'), 'XI')
		self.assertEqual(self.calc.plus('XI', 'X'), 'XXI')
		self.assertEqual(self.calc.plus('XI', 'V'), 'XVI')
		self.assertEqual(self.calc.plus('XII', 'VI'), 'XVIII')

	def test_add_combinesLettersToNextLetterUp(self):
		self.assertEqual(self.calc.plus('III', 'II'), 'V')
		self.assertEqual(self.calc.plus('V', 'V'), 'X')
		self.assertEqual(self.calc.plus('XVI', 'V'), 'XXI')
		self.assertEqual(self.calc.plus('XII', 'VIII'), 'XX')

	def test_add_combinesLettersToNextLetterUpMinusOne(self):
		self.assertEqual(self.calc.plus('II', 'II'), 'IV')
		self.assertEqual(self.calc.plus('I', 'VIII'), 'IX')
		self.assertEqual(self.calc.plus('XVI', 'III'), 'XIX')
		self.assertEqual(self.calc.plus('XXV', 'XXI'), 'XLVI')

	def test_add_understandsASmallerLetterBeforeABiggerLetter(self):
		self.assertEqual(self.calc.plus('IV', 'I'), 'V')
		self.assertEqual(self.calc.plus('IX', 'VI'), 'XV')
		self.assertEqual(self.calc.plus('IV', 'V'), 'IX')
		self.assertEqual(self.calc.plus('XLII', 'XIV'), 'LVI')

	def test_add_moreThanTwoNumbersAtOnce(self):
		self.assertEqual(self.calc.plus('I', 'I', 'I'), 'III')
		self.assertEqual(self.calc.plus('IX', 'VI', 'IV'), 'XIX')
		self.assertEqual(self.calc.plus('IV', 'V', 'III', 'XII'), 'XXIV')
		self.assertEqual(self.calc.plus('XVIII', 'XIV', 'XXII', 'III', 'IV'), 'LXI')


	def test_subtract_removesLetters(self):
		self.assertEqual(self.calc.minus('II', 'I'), 'I')
		self.assertEqual(self.calc.minus('III', 'II'), 'I')
		self.assertEqual(self.calc.minus('XX', 'X'), 'X')
		self.assertEqual(self.calc.minus('XVI', 'XI'), 'V')

	def test_subtract_turnsBiggerLettersIntoSmallerLetters(self):
		self.assertEqual(self.calc.minus('V', 'II'), 'III')
		self.assertEqual(self.calc.minus('X', 'V'), 'V')
		self.assertEqual(self.calc.minus('X', 'VII'), 'III')
		self.assertEqual(self.calc.minus('X', 'II'), 'VIII')

	def test_subtract_understandsASmallerLetterBeforeABiggerLetter(self):
		self.assertEqual(self.calc.minus('IV', 'II'), 'II')
		self.assertEqual(self.calc.minus('X', 'IV'), 'VI')
		self.assertEqual(self.calc.minus('IX', 'VII'), 'II')
		self.assertEqual(self.calc.minus('L', 'X'), 'XL')

	def test_subtract_moreThanTwoNumbersAtOnce(self):
		self.assertEqual(self.calc.minus('IV', 'II', 'I'), 'I')
		self.assertEqual(self.calc.minus('X', 'I', 'V', 'I'), 'III')
		self.assertEqual(self.calc.minus('LIV', 'IX', 'II', 'V'), 'XXXVIII')


	def test_multiply(self):
		self.assertEqual(self.calc.multiply('II', 'I'), 'II')
		self.assertEqual(self.calc.multiply('X', 'II'), 'XX')
		self.assertEqual(self.calc.multiply('VI', 'III'), 'XVIII')
		self.assertEqual(self.calc.multiply('XI', 'V'), 'LV')

	def test_multiply_understandsASmallerLetterBeforeABiggerLetter(self):
		self.assertEqual(self.calc.multiply('II', 'IV'), 'VIII')
		self.assertEqual(self.calc.multiply('IX', 'II'), 'XVIII')
		self.assertEqual(self.calc.multiply('VII', 'II'), 'XIV')

	def test_multiply_moreThanTwoNumbersAtOnce(self):
		self.assertEqual(self.calc.multiply('II', 'IV', 'II'), 'XVI')
		self.assertEqual(self.calc.multiply('IV', 'II', 'V', 'II'), 'LXXX')


	def test_divide(self):
		self.assertEqual(self.calc.divide('II', 'II'), 'I')
		self.assertEqual(self.calc.divide('X', 'II'), 'V')
		self.assertEqual(self.calc.divide('VI', 'III'), 'II')
		self.assertEqual(self.calc.divide('LII', 'XIII'), 'IV')

	def test_divide_understandsASmallerLetterBeforeABiggerLetter(self):
		self.assertEqual(self.calc.divide('IV', 'II'), 'II')
		self.assertEqual(self.calc.divide('XVI', 'IV'), 'IV')

	def test_divide_moreThanTwoNumbersAtOnce(self):
		self.assertEqual(self.calc.divide('XVI', 'II', 'IV'), 'II')
		self.assertEqual(self.calc.divide('LVI', 'IV', 'II'), 'VII')


if __name__ == '__main__':
	unittest.main()