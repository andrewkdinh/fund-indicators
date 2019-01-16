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

from StockData import StockData

listOfStocks = []
numberOfStocks = int(input("How many stocks or mutual funds would you like to analyze? "))
for i in range(0, numberOfStocks, 1):
  	print("Stock", i+1, ": ", end='')
  	stockName = str(input())
  	listOfStocks.append(i)
  	listOfStocks[i] = StockData()
  	listOfStocks[i].setName(stockName)
  	#print(listOfStocks[i].name)

sumOfListLengths = 0
for i in range(0, numberOfStocks, 1):
  	print(listOfStocks[i].name)
  	StockData.main(listOfStocks[i])
  	# Count how many stocks are available
  	temp = StockData.returnAllLists(listOfStocks[i])
  	sumOfListLengths = sumOfListLengths + len(temp)

if sumOfListLengths == 0:
    print("No sources have data for given stocks")
    exit()

# Find return over time using either Jensen's Alpha, Sharpe Ratio, Sortino Ratio, or Treynor Ratio
#from StockReturn import Return


# Runs correlation or regression study
#print(listOfStocks[0].name, listOfStocks[0].absFirstLastDates, listOfStocks[0].finalDatesAndClose)
indicatorFound = False
while indicatorFound == False:
	print("\n1. Expense Ratio\n2. Asset Size\n3. Turnover\n4. Persistence\nWhich indicator would you like to look at? ", end='')
	indicator = str(input())
	indicatorFound = True

	if indicator == 'Expense Ratio' or indicator == '1' or indicator == 'expense ratio':
        #from ExpenseRatio import ExpenseRatio
		print('\nExpense Ratio')

	elif indicator == 'Asset Size' or indicator == '2' or indicator == 'asset size':
		print('\nAsset Size')

	elif indicator == 'Turnover' or indicator == '3' or indicator == 'turnover':
		print('\nTurnover')

	elif indicator == 'Persistence' or indicator == '4' or indicator == 'persistence':
		print('\nPersistence')

	else:
		indicatorFound = False
		print('\nInvalid input, please enter indicator again')

'''
stockName = 'IWV'
stock1 = Stock(stockName)
print("Finding available dates and close values for", stock1.name)
StockData.main(stock1)
'''
