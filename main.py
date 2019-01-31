# main.py
# Andrew Dinh
# Python 3.6.7

import requests
import json
import datetime
import numpy
import Functions

# API Keys
apiAV = 'O42ICUV58EIZZQMU'
# apiBarchart = 'a17fab99a1c21cd6f847e2f82b592838'
apiBarchart = 'f40b136c6dc4451f9136bb53b9e70ffa'
apiTiingo = '2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8'
apiTradier = 'n26IFFpkOFRVsB5SNTVNXicE5MPD'
# If you're going to take these API keys and abuse it, you should really reconsider your life priorities

'''
API Keys:
    Alpha Vantage API Key: O42ICUV58EIZZQMU
    Barchart API Key: a17fab99a1c21cd6f847e2f82b592838 
        Possible other one? f40b136c6dc4451f9136bb53b9e70ffa
        150 getHistory queries per day
    Tiingo API Key: 2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8
    Tradier API Key: n26IFFpkOFRVsB5SNTVNXicE5MPD
        Monthly Bandwidth = 5 GB
        Hourly Requests = 500
        Daily Requests = 20,000
        Symbol Requests = 500

    Mutual funds:
    Yes: Alpha Vantage, Tiingo
    No: IEX, Barchart
'''


class Stock:

    # GLOBAL VARIABLES
    timeFrame = []
    benchmarkDates = []
    benchmarkCloseValues = []
    benchmarkUnadjustedReturn = 0

    def __init__(self):
        # BASIC DATA
        self.name = ''  # Ticker symbol
        self.allDates = []
        self.allCloseValues = []
        self.dates = []
        self.closeValues = []
        self.datesMatchBenchmark = []
        self.closeValuesMatchBenchmark = []

        # CALCULATED RETURN
        self.unadjustedReturn = 0
        self.sortino = 0
        self.sharpe = 0
        self.treynor = 0
        self.alpha = 0
        self.beta = 0
        self.standardDeviation = 0
        self.negStandardDeviation = 0

        # INDICATOR VALUES
        self.expenseRatio = 0
        self.assetSize = 0
        self.turnover = 0
        self.persistence = []  # [Years, Months]

        # CALCULATED VALUES FOR INDICATORS
        self.correlation = 0
        self.regression = 0

    def setName(self, newName):
        self.name = newName

    def getName(self):
        return self.name

    def getAllDates(self):
        return self.allDates

    def getAllCloseValues(self):
        return self.allCloseValues

    def IEX(self):
        print('IEX')
        url = ''.join(
            ('https://api.iextrading.com/1.0/stock/', self.name, '/chart/5y'))
        #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
        print("\nSending request to:", url)
        f = requests.get(url)
        json_data = f.text
        if json_data == 'Unknown symbol' or f.status_code == 404:
            print("IEX not available")
            return 'Not available'
        loaded_json = json.loads(json_data)
        listIEX = []

        print("\nFinding all dates given")
        allDates = []
        for i in range(0, len(loaded_json), 1):  # If you want to do oldest first
            # for i in range(len(loaded_json)-1, -1, -1):
            line = loaded_json[i]
            date = line['date']
            allDates.append(date)
        listIEX.append(allDates)
        print(len(listIEX[0]), "dates")

        print("\nFinding close values for each date")
        values = []
        for i in range(0, len(loaded_json), 1):  # If you want to do oldest first
            # for i in range(len(loaded_json)-1, -1, -1):
            line = loaded_json[i]
            value = line['close']
            values.append(value)
        listIEX.append(values)
        print(len(listIEX[1]), "close values")

        return listIEX

    def AV(self):
        print('Alpha Vantage')
        listAV = []
        url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=',
                       self.name, '&outputsize=full&apikey=', apiAV))
        # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&apikey=demo

        print("\nSending request to:", url)
        print("(This will take a while)")
        f = requests.get(url)
        json_data = f.text
        loaded_json = json.loads(json_data)

        if len(loaded_json) == 1 or f.status_code == 404:
            print("Alpha Vantage not available")
            return 'Not available'

        dailyTimeSeries = loaded_json['Time Series (Daily)']
        listOfDates = list(dailyTimeSeries)
        # listAV.append(listOfDates)
        listAV.append(list(reversed(listOfDates)))

        print("\nFinding close values for each date")
        values = []
        for i in range(0, len(listOfDates), 1):
            temp = listOfDates[i]
            loaded_json2 = dailyTimeSeries[temp]
            #value = loaded_json2['4. close']
            value = loaded_json2['5. adjusted close']
            values.append(value)
        # listAV.append(values)
        listAV.append(list(reversed(values)))
        print(len(listAV[1]), "close values")

        return listAV

    def Tiingo(self):
        print('Tiingo')
        token = ''.join(('Token ', apiTiingo))
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        url = ''.join(('https://api.tiingo.com/tiingo/daily/', self.name))
        print("\nSending request to:", url)
        f = requests.get(url, headers=headers)
        loaded_json = f.json()
        if len(loaded_json) == 1 or f.status_code == 404:
            print("Tiingo not available")
            return 'Not available'

        listTiingo = []

        print("\nFinding first and last date")
        firstDate = loaded_json['startDate']
        lastDate = loaded_json['endDate']
        print(firstDate, '...', lastDate)

        print("\nFinding all dates given", end='')
        dates = []
        values = []
        url2 = ''.join((url, '/prices?startDate=',
                        firstDate, '&endDate=', lastDate))
        # https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1
        print("\nSending request to:", url2, '\n')
        requestResponse2 = requests.get(url2, headers=headers)
        loaded_json2 = requestResponse2.json()
        for i in range(0, len(loaded_json2)-1, 1):
            line = loaded_json2[i]
            dateWithTime = line['date']
            temp = dateWithTime.split('T00:00:00.000Z')
            date = temp[0]
            dates.append(date)

            value = line['close']
            values.append(value)
        listTiingo.append(dates)
        print(len(listTiingo[0]), "dates")

        print("Finding close values for each date")
        # Used loop from finding dates
        listTiingo.append(values)
        print(len(listTiingo[1]), "close values")

        return listTiingo

    def datesAndClose(self):
        print('\n', Stock.getName(self), sep='')

        # sourceList = ['AV', 'Tiingo', 'IEX'] # Change back to this later
        sourceList = ['Tiingo', 'IEX', 'AV']
        # Use each source until you get a value
        for j in range(0, len(sourceList), 1):
            source = sourceList[j]
            print('\nSource being used: ', source)

            if source == 'AV':
                datesAndCloseList = Stock.AV(self)
            elif source == 'Tiingo':
                datesAndCloseList = Stock.Tiingo(self)
            elif source == 'IEX':
                datesAndCloseList = Stock.IEX(self)

            if datesAndCloseList != 'Not available':
                break
            else:
                #print(sourceList[j], 'does not have data available')
                if j == len(sourceList)-1:
                    print('\nNo sources have data for', self.name)
                    return
                    # FIGURE OUT WHAT TO DO HERE

        # Convert dates to datetime
        allDates = datesAndCloseList[0]
        for j in range(0, len(allDates), 1):
            allDates[j] = Functions.stringToDate(allDates[j])
        datesAndCloseList[0] = allDates

        return datesAndCloseList

    def datesAndClose2(self):
        print('Shortening list to fit time frame')
        # Have to do this because if I just make dates = self.allDates & closeValues = self.allCloseValues, then deleting from dates & closeValues also deletes it from self.allDates & self.allCloseValues (I'm not sure why)
        dates = []
        closeValues = []
        for i in range(0, len(self.allDates), 1):
            dates.append(self.allDates[i])
            closeValues.append(self.allCloseValues[i])

        firstDate = datetime.datetime.now().date() - datetime.timedelta(
            days=self.timeFrame[0]*365) - datetime.timedelta(days=self.timeFrame[1]*30)
        print('\n', self.timeFrame[0], ' years and ',
              self.timeFrame[1], ' months ago: ', firstDate, sep='')
        closestDate = Functions.getNearest(dates, firstDate)
        if closestDate != firstDate:
            print('Closest date available for', self.name, ':', closestDate)
            firstDate = closestDate
        else:
            print(self.name, 'has a close value for', firstDate)

        # Remove dates in list up to firstDate
        while dates[0] != firstDate:
            dates.remove(dates[0])

        # Remove close values until list is same length as dates
        while len(closeValues) != len(dates):
            closeValues.remove(closeValues[0])

        datesAndCloseList2 = []
        datesAndCloseList2.append(dates)
        datesAndCloseList2.append(closeValues)

        print(len(dates), 'dates')
        print(len(closeValues), 'close values')

        return datesAndCloseList2

    def unadjustedReturn(self):
        unadjustedReturn = (float(self.closeValues[len(
            self.closeValues)-1]/self.closeValues[0])**(1/(self.timeFrame[0]+(self.timeFrame[1])*.1)))-1
        print('Annual unadjusted return:', unadjustedReturn)
        return unadjustedReturn

    def beta(self, benchmarkMatchDatesAndCloseValues):
        beta = numpy.corrcoef(self.closeValuesMatchBenchmark,
                              benchmarkMatchDatesAndCloseValues[1])[0, 1]
        print('Beta:', beta)
        return beta


def isConnected():
    import socket  # To check internet connection
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.andrewkdinh.com", 80))
        print('Internet connection is good!')
        return True
    except OSError:
        # pass
        print("No internet connection!")
    return False


def checkPackages():
    import importlib.util
    import sys

    packagesInstalled = True
    packages = ['requests', 'numpy']
    for i in range(0, len(packages), 1):
        package_name = packages[i]
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(
                package_name +
                " is not installed\nPlease type in 'pip install -r requirements.txt' to install all required packages")
            packagesInstalled = False
    return packagesInstalled


def benchmarkInit():
    # Treat benchmark like stock
    benchmarkTicker = ''
    while benchmarkTicker == '':
        benchmarks = ['S&P500', 'DJIA', 'Russell 3000', 'MSCI EAFE']
        benchmarksTicker = ['SPY', 'DJIA', 'VTHR', 'EFT']
        print('\nList of benchmarks:', benchmarks)

        # benchmark = str(input('Benchmark to compare to: '))
        benchmark = 'S&P500'

        for i in range(0, len(benchmarks), 1):
            if benchmark == benchmarks[i]:
                benchmarkTicker = benchmarksTicker[i]

        if benchmarkTicker == '':
            print('Benchmark not found. Please type in a benchmark from the list')

    print(benchmark, ' (', benchmarkTicker, ')', sep='')

    benchmark = Stock()
    benchmark.setName(benchmarkTicker)

    return benchmark


def stocksInit():
    listOfStocks = []

    # numberOfStocks = int(input('\nHow many stocks/mutual funds/ETFs would you like to analyze? '))
    numberOfStocks = 1

    print('\nHow many stocks/mutual funds/ETFs would you like to analyze? ', numberOfStocks)

    for i in range(0, numberOfStocks, 1):
        print('Stock', i + 1, ': ', end='')
        #stockName = str(input())

        stockName = 'FBGRX'
        print(stockName)

        listOfStocks.append(stockName)
        listOfStocks[i] = Stock()
        listOfStocks[i].setName(stockName)

    return listOfStocks


def timeFrameInit():
    print('\nPlease enter the time frame in years and months (30 days)')
    print("Years: ", end='')
    #years = int(input())
    years = 5
    print(years)
    print("Months: ", end='')
    #months = int(input())
    months = 0
    print(months)

    timeFrame = []
    timeFrame.append(years)
    timeFrame.append(months)
    return timeFrame


def dataMain(listOfStocks):
    print('\nGathering dates and close values')
    for i in range(0, len(listOfStocks), 1):

        datesAndCloseList = Stock.datesAndClose(listOfStocks[i])
        listOfStocks[i].allDates = datesAndCloseList[0]
        listOfStocks[i].allCloseValues = datesAndCloseList[1]

        # Clip list to fit time frame
        datesAndCloseList2 = Stock.datesAndClose2(listOfStocks[i])
        listOfStocks[i].dates = datesAndCloseList2[0]
        listOfStocks[i].closeValues = datesAndCloseList2[1]


def returnMain(benchmark, listOfStocks):
    print('\nCalculating unadjusted return, Sharpe ratio, Sortino ratio, and Treynor ratio\n')
    print(benchmark.name)
    benchmark.unadjustedReturn = Stock.unadjustedReturn(benchmark)

    # Make benchmark data global
    # Maybe remove this later
    Stock.benchmarkDates = benchmark.dates
    Stock.benchmarkCloseValues = benchmark.closeValues
    Stock.benchmarkUnadjustedReturn = benchmark.unadjustedReturn

    for i in range(0, len(listOfStocks), 1):
        print(listOfStocks[i].name)

        # Make sure each date has a value for both the benchmark and the stock
        list1 = []
        list2 = []
        list1.append(listOfStocks[i].dates)
        list1.append(listOfStocks[i].closeValues)
        list2.append(Stock.benchmarkDates)
        list2.append(Stock.benchmarkCloseValues)
        temp = Functions.removeExtraDatesAndCloseValues(list1, list2)
        listOfStocks[i].datesMatchBenchmark = temp[0][0]
        listOfStocks[i].closeValuesMatchBenchmark = temp[0][1]
        benchmarkMatchDatesAndCloseValues = temp[1]

        listOfStocks[i].unadjustedReturn = Stock.unadjustedReturn(
            listOfStocks[i])
        listOfStocks[i].beta = Stock.beta(
            listOfStocks[i], benchmarkMatchDatesAndCloseValues)


def main():
    # Test internet connection
    internetConnection = isConnected()
    if not internetConnection:
        return

    # Check that all required packages are installed
    packagesInstalled = checkPackages()
    if not packagesInstalled:
        return

    # Choose benchmark and makes it class Stock
    benchmark = benchmarkInit()
    # Add it to a list to work with other functions
    benchmarkAsList = []
    benchmarkAsList.append(benchmark)

    # Asks for stock(s) ticker and makes them class Stock
    listOfStocks = stocksInit()

    # Determine time frame [Years, Months]
    timeFrame = timeFrameInit()
    Stock.timeFrame = timeFrame  # Needs to be a global variable for all stocks

    # Gather data for benchmark and stock(s)
    dataMain(benchmarkAsList)
    dataMain(listOfStocks)

    # Calculate return for benchmark and stock(s)
    returnMain(benchmark, listOfStocks)


if __name__ == "__main__":
    main()


'''
from StockData import StockData
from StockReturn import Return

listOfStocksData = []
listOfStocksReturn = []
# numberOfStocks = int(input("How many stocks or mutual funds would you like to analyze? ")) # CHANGE BACK LATER
numberOfStocks = 1
for i in range(0, numberOfStocks, 1):
      print("Stock", i+1, ": ", end='')
      stockName = str(input())
      listOfStocksData.append(i)
      listOfStocksData[i] = StockData()
      listOfStocksData[i].setName(stockName)
    # print(listOfStocksData[i].name)

    # listOfStocksReturn.append(i)
    # listOfStocksReturn[i] = StockReturn()


# Decide on a benchmark
benchmarkTicker = ''
while benchmarkTicker == '':
    listOfBenchmarks = ['S&P500', 'DJIA', 'Russell 3000', 'MSCI EAFE']
    listOfBenchmarksTicker = ['SPY', 'DJIA', 'VTHR', 'EFT']
    print('\nList of benchmarks:', listOfBenchmarks)
    # benchmark = str(input('Benchmark to compare to: '))
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
    # StockReturn.main(listOfStocksReturn[i])


# Runs correlation or regression study
# print(listOfStocksData[0].name, listOfStocksData[0].absFirstLastDates, listOfStocksData[0].finalDatesAndClose)
indicatorFound = False
while indicatorFound == False:
    print("1. Expense Ratio\n2. Asset Size\n3. Turnover\n4. Persistence\nWhich indicator would you like to look at? ", end='')

    # indicator = str(input()) # CHANGE BACK TO THIS LATER
    indicator = 'Expense Ratio'
    print(indicator, end='')

    indicatorFound = True
    print('\n', end='')

    if indicator == 'Expense Ratio' or indicator == '1' or indicator == 'expense ratio':
        # from ExpenseRatio import ExpenseRatio
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

stockName = 'IWV'
stock1 = Stock(stockName)
print("Finding available dates and close values for", stock1.name)
StockData.main(stock1)
'''
