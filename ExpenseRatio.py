# ExpenseRatio.py
# Andrew Dinh
# Python 3.6.1
# Description:
'''
Asks user for expense ratio of stock (I don't think there's an API for expense ratios)
Runs corrrelation study (I'm not sure if I want another class for this or not)
''' 

import numpy

def main(): # For testing purposes
	a = [1,4,6]
	b = [1,2,3]
	c = numpy.corrcoef(a, b)[0, 1]
	print(c)


if __name__ == "__main__":
  	main()
