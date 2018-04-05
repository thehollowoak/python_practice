import unittest

ONES = { 0:"", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten", 11:"eleven", 12:"twelve", 
		13:"thirteen", 14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen" }
TENS = { 2:"twenty", 3:"thirty", 4:"fourty", 5:"fifty", 6:"sixty", 7:"seventy", 8:"eighty", 9:"ninety"}
PLACES = { 1000000000: "billion", 1000000: "million", 1000:"thousand", 1:""}

def numbersToWords(num):
	words = ''
	for key, value in PLACES.items():
		if num >= key:
			n = num/key
			if n >= 100:
				words += ONES[n/100] + " hundered"
				n = n%100
				if n:
					words += " and "
			if n < 20:
				words += ONES[n]
			else:
				words += TENS[n/10]
				if n%10: words += " " + ONES[n%10]
			if value: words += " " + value + ", "
			num = num%key
	return words

def wordsToNumbers(word):
	num = 0
	words = word.replace(',', '').replace(' and ', ' ').split()
	for key, value in PLACES.items():
		placeIndex, n, i = 0, 0, 0
		if value in words: placeIndex = words.index(value)
		elif not value: placeIndex = len(words)
		else: continue
		if 'hundered' in words and words.index('hundered') < placeIndex:
			n += ONES.values().index(words[0]) * 100
			i += 2
		if words[i] in TENS.values():
			n += TENS.keys()[TENS.values().index(words[i])] * 10
			i += 1
		if i < placeIndex:
			n += ONES.values().index(words[i])
		num += n * key
		words = words[placeIndex+1:]
	return num


class TestStringMethods(unittest.TestCase):

    def test_numbersToWords(self):
        self.assertEqual(numbersToWords(578456198230), 'five hundered and seventy eight billion, four hundered and fifty six million, one hundered and ninety eight thousand, two hundered and thirty')

    def test_wordsToNumbers(self):
        self.assertEqual(wordsToNumbers('five hundered and seventy eight billion, four hundered and fifty six million, one hundered and ninety eight thousand, two hundered and thirty'), 578456198230)

if __name__ == '__main__':
    unittest.main()
