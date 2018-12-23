# main.py
# Andrew Dinh
# Python 3.6.1
# Description: 
'''
Asks users for mutual funds/stocks to compare
Asks to be compared (expense ratio, turnover, market capitalization, or persistence)
Asks for time period (Possibly: 1 year, 5 years, 10 years)
Makes the mutual funds as class Stock
Gets data from each API
Compare and contrast dates and end changeOverTime for set time period
  NOTES: Later can worry about getting close values to make a graph or something
Gives correlation value using equation at the end (from 0 to 1)

FIRST TESTING WITH EXPENSE RATIO
'''

from StockData import Stock

listOfStocks = []
numberOfStocks = int(input("How many stocks or mutual funds would you like to analyze? "))
for i in range(0, numberOfStocks, 1):
  print("Stock", i+1, ": ", end='')
  stockName = str(input())
  listOfStocks.append(i)
  listOfStocks[i] = Stock()
  listOfStocks[i].setName(stockName)
  #print(listOfStocks[i].name)

for i in range(0, numberOfStocks, 1):
  print("\n")
  print(listOfStocks[i].name)
  Stock.main(listOfStocks[i])

#print(listOfStocks[0].name, listOfStocks[0].absFirstLastDates, listOfStocks[0].finalDatesAndClose)
print("\nWhich indicator would you like to look at? \n1. Expense Ratio")
indicator = str(input)
'''
stockName = 'IWV'
stock1 = Stock(stockName)
print("Finding available dates and close values for", stock1.name)
Stock.main(stock1)
'''