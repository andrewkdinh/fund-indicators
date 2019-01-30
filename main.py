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
from StockReturn import Return

listOfStocksData = []
listOfStocksReturn = []
#numberOfStocks = int(input("How many stocks or mutual funds would you like to analyze? ")) # CHANGE BACK LATER
numberOfStocks = 1
for i in range(0, numberOfStocks, 1):
  	print("Stock", i+1, ": ", end='')
  	stockName = str(input())
  	listOfStocksData.append(i)
  	listOfStocksData[i] = StockData()
  	listOfStocksData[i].setName(stockName)
	# print(listOfStocksData[i].name)

	#listOfStocksReturn.append(i)
	#listOfStocksReturn[i] = StockReturn()


# Decide on a benchmark
benchmarkTicker = ''
while benchmarkTicker == '':
	listOfBenchmarks = ['S&P500', 'DJIA', 'Russell 3000', 'MSCI EAFE']
	listOfBenchmarksTicker = ['SPY', 'DJIA', 'VTHR', 'EFT']
	print('\nList of benchmarks:', listOfBenchmarks)
	#benchmark = str(input('Benchmark to compare to: '))
	benchmark = 'S&P500'

	for i in range(0,len(listOfBenchmarks), 1):
		if benchmark == listOfBenchmarks[i]:
			benchmarkTicker = listOfBenchmarksTicker[i]
			i = len(listOfBenchmarks)

	if benchmarkTicker == '':
		print('Benchmark not found. Please type in a benchmark from the list')

print('\n', benchmark, ' (', benchmarkTicker, ')', sep='')

benchmarkName = str(benchmark)
benchmark = StockData()
benchmark.setName(benchmarkName)
StockData.main(benchmark)

benchmarkReturn = Return()
Return.mainBenchmark(benchmarkReturn, benchmark)

timeFrame = Return.returnTimeFrame(benchmarkReturn)
print('Time Frame [years, months]:', timeFrame)

sumOfListLengths = 0
for i in range(0, numberOfStocks, 1):
  	print('\n', listOfStocksData[i].name, sep='')
  	StockData.main(listOfStocksData[i])
  	# Count how many stocks are available
  	sumOfListLengths = sumOfListLengths + len(StockData.returnAllLists(listOfStocksData[i]))

if sumOfListLengths == 0:
    print("No sources have data for given stocks")
    exit()

# Find return over time using either Jensen's Alpha, Sharpe Ratio, Sortino Ratio, or Treynor Ratio
for i in range(0, numberOfStocks, 1):
	print('\n', listOfStocksData[i].name, sep='')
	#StockReturn.main(listOfStocksReturn[i])


# Runs correlation or regression study
# print(listOfStocksData[0].name, listOfStocksData[0].absFirstLastDates, listOfStocksData[0].finalDatesAndClose)
indicatorFound = False
while indicatorFound == False:
	print("1. Expense Ratio\n2. Asset Size\n3. Turnover\n4. Persistence\nWhich indicator would you like to look at? ", end='')
	
	#indicator = str(input()) # CHANGE BACK TO THIS LATER
	indicator = 'Expense Ratio'
	print(indicator, end='')

	indicatorFound = True
	print('\n', end='')

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
		print('Invalid input, please enter indicator again')

'''
stockName = 'IWV'
stock1 = Stock(stockName)
print("Finding available dates and close values for", stock1.name)
StockData.main(stock1)
'''
