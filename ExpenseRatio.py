# ExpenseRatio.py
# Andrew Dinh
# Python 3.6.1
# Description:
'''
Asks user for expense ratio of stock (I don't think there's an API for expense ratios)
Runs corrrelation study (I'm not sure if I want another class for this or not)
''' 

import numpy
#import urllib2, re
from urllib.request import urlopen
import re

def main(): # For testing purposes
  '''
	a = [1,2,3]
	b = [2,4,6]
	c = numpy.corrcoef(a, b)[0, 1]
	print(c)
  '''
  #http://finance.yahoo.com/q/pr?s=spy+profile
  stockSymbols = [ "VDIGX", "VFIAX" ]
  expenses = [ [ "Fund", "Most Recent Expense Ratio" ] ]
  for stockSymbol in stockSymbols:
      page = urlopen("http://finance.yahoo.com/q/pr?s=" + stockSymbol + "+profile" )
      data = str(page.read())
      row = re.findall("Annual Report Expense Ratio.*?</tr>", data)
      if len(row) > 0:
          ER = re.findall("<td.*?>(\d+\.\d+).*?</td>", row[0] )[0]
          expenses.append( [ stockSymbol, ER ] )
      else:
          print(stockSymbol, "does not appear to be a fund with an expense ratio")
  print("\n".join( i[0] + "," + i[1] for i in expenses))



if __name__ == "__main__":
  	main()
