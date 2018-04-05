def fizzbuzz(num):
	for x in range(1, num+1):
		if x%15 == 0:
			print("Fizzbuzz")
		elif x%3 == 0 or x%10 == 3 or int(x/10) == 3:
			print("Fizz")
		elif x%5 == 0 or int(x/10) == 5:
			print("Buzz")
		else:
			print(x)

fizzbuzz(35)
