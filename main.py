# https://github.com/andrewkdinh/fund-indicators
# Determine indicators of overperforming mutual funds
# Andrew Dinh
# Python 3.6.7

# Required
import requests
import json
import datetime
import Functions
import numpy as np

# Required for linear regression
import matplotlib.pyplot as plt
import sys

# Optional
import requests_cache
# https://requests-cache.readthedocs.io/en/lates/user_guide.html
requests_cache.install_cache(
    'requests_cache', backend='sqlite', expire_after=43200)  # 12 hours

# API Keys
apiAV = 'O42ICUV58EIZZQMU'
# apiBarchart = 'a17fab99a1c21cd6f847e2f82b592838'
apiBarchart = 'f40b136c6dc4451f9136bb53b9e70ffa'
apiTiingo = '2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8'
apiTradier = 'n26IFFpkOFRVsB5SNTVNXicE5MPD'
apiQuandl = 'KUh3U3hxke9tCimjhWEF'
# apiIntrinio = 'OmNmN2E5YWI1YzYxN2Q4NzEzZDhhOTgwN2E2NWRhOWNl'
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
    Quandl API Key: KUh3U3hxke9tCimjhWEF
    Intrinio API Key: OmNmN2E5YWI1YzYxN2Q4NzEzZDhhOTgwN2E2NWRhOWNl

    Mutual funds?
    Yes: Alpha Vantage, Tiingo
    No: IEX, Barchart

    Adjusted?
    Yes: Alpha Vantage, IEX
    No: Tiingo
'''


class Stock:

    # GLOBAL VARIABLES
    timeFrame = 0
    riskFreeRate = 0
    indicator = ''

    # BENCHMARK VALUES
    benchmarkDates = []
    benchmarkCloseValues = []
    benchmarkAverageAnnualReturn = 0
    benchmarkStandardDeviation = 0

    # INDICATOR VALUES
    indicatorCorrelation = []
    indicatorRegression = []

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
        self.averageAnnualReturn = 0
        self.annualReturn = []
        self.sharpe = 0
        self.sortino = 0
        self.treynor = 0
        self.alpha = 0
        self.beta = 0
        self.standardDeviation = 0
        self.downsideDeviation = 0
        self.kurtosis = 0
        self.skewness = 0  # Not sure if I need this
        self.linearRegression = []  # for y=mx+b, this list has [m,b]

        self.indicatorValue = ''

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
        # link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
        print("\nSending request to:", url)
        f = requests.get(url)
        Functions.fromCache(f)
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
        f = requests.get(url)
        Functions.fromCache(f)
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
            # value = loaded_json2['4. close']
            value = loaded_json2['5. adjusted close']
            values.append(float(value))
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
        Functions.fromCache(f)
        loaded_json = f.json()
        if len(loaded_json) == 1 or f.status_code == 404 or loaded_json['startDate'] == None:
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
        Functions.fromCache(requestResponse2)
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

        sourceList = ['AV', 'IEX', 'Tiingo']
        # sourceList = ['IEX', 'Tiingo', 'AV']
        # Use each source until you get a value
        for j in range(0, len(sourceList), 1):
            source = sourceList[j]
            print('\nSource being used:', source)

            if source == 'AV':
                datesAndCloseList = Stock.AV(self)
            elif source == 'Tiingo':
                datesAndCloseList = Stock.Tiingo(self)
            elif source == 'IEX':
                datesAndCloseList = Stock.IEX(self)

            if datesAndCloseList != 'Not available':
                break
            else:
                if j == len(sourceList)-1:
                    print('\nNo sources have data for', self.name)
                    print('Removing', self.name,
                          'from list of stocks to ensure compatibility later')
                    return 'Not available'

        # Convert dates to datetime
        allDates = datesAndCloseList[0]
        for j in range(0, len(allDates), 1):
            allDates[j] = Functions.stringToDate(allDates[j])
        datesAndCloseList[0] = allDates

        return datesAndCloseList

    def datesAndCloseFitTimeFrame(self):
        print('Shortening list to fit time frame')
        # Have to do this because if I just make dates = self.allDates & closeValues = self.allCloseValues, then deleting from dates & closeValues also deletes it from self.allDates & self.allCloseValues (I'm not sure why)
        dates = []
        closeValues = []
        for i in range(0, len(self.allDates), 1):
            dates.append(self.allDates[i])
            closeValues.append(self.allCloseValues[i])

        firstDate = datetime.datetime.now().date() - datetime.timedelta(
            days=self.timeFrame*365)
        print('\n', self.timeFrame, ' years ago: ', firstDate, sep='')
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

    def calcAverageAnnualReturn(self):  # pylint: disable=E0202
        # averageAnnualReturn = (float(self.closeValues[len(self.closeValues)-1]/self.closeValues[0])**(1/(self.timeFrame)))-1
        # averageAnnualReturn = averageAnnualReturn * 100
        averageAnnualReturn = sum(self.annualReturn)/self.timeFrame
        print('Average annual return:', averageAnnualReturn)
        return averageAnnualReturn

    def calcAnnualReturn(self):
        annualReturn = []

        # Calculate annual return in order from oldest to newest
        annualReturn = []
        for i in range(0, self.timeFrame, 1):
            firstDate = datetime.datetime.now().date() - datetime.timedelta(
                days=(self.timeFrame-i)*365)
            secondDate = datetime.datetime.now().date() - datetime.timedelta(
                days=(self.timeFrame-i-1)*365)

            # Find closest dates to firstDate and lastDate
            firstDate = Functions.getNearest(self.dates, firstDate)
            secondDate = Functions.getNearest(self.dates, secondDate)

            if firstDate == secondDate:
                print('Closest date is', firstDate,
                      'which is after the given time frame.')
                return 'Not available'

            # Get corresponding close values and calculate annual return
            for i in range(0, len(self.dates), 1):
                if self.dates[i] == firstDate:
                    firstClose = self.closeValues[i]
                elif self.dates[i] == secondDate:
                    secondClose = self.closeValues[i]
                    break

            annualReturnTemp = (secondClose/firstClose)-1
            annualReturnTemp = annualReturnTemp * 100
            annualReturn.append(annualReturnTemp)

        print('Annual return over the past',
              self.timeFrame, 'years:', annualReturn)
        return annualReturn

    def calcCorrelation(self, closeList):
        correlation = np.corrcoef(
            self.closeValuesMatchBenchmark, closeList)[0, 1]
        print('Correlation with benchmark:', correlation)
        return correlation

    def calcStandardDeviation(self):
        numberOfValues = self.timeFrame
        mean = self.averageAnnualReturn
        standardDeviation = (
            (sum((self.annualReturn[x]-mean)**2 for x in range(0, numberOfValues, 1)))/(numberOfValues-1))**(1/2)
        print('Standard Deviation:', standardDeviation)
        return standardDeviation

    def calcDownsideDeviation(self):
        numberOfValues = self.timeFrame
        targetReturn = self.averageAnnualReturn
        downsideDeviation = (
            (sum(min(0, (self.annualReturn[x]-targetReturn))**2 for x in range(0, numberOfValues, 1)))/(numberOfValues-1))**(1/2)
        print('Downside Deviation:', downsideDeviation)
        return downsideDeviation

    def calcKurtosis(self):
        numberOfValues = self.timeFrame
        mean = self.averageAnnualReturn
        kurtosis = (sum((self.annualReturn[x]-mean)**4 for x in range(
            0, numberOfValues, 1)))/((numberOfValues-1)*(self.standardDeviation ** 4))
        print('Kurtosis:', kurtosis)
        return kurtosis

    def calcSkewness(self):
        numberOfValues = self.timeFrame
        mean = self.averageAnnualReturn
        skewness = (sum((self.annualReturn[x]-mean)**3 for x in range(
            0, numberOfValues, 1)))/((numberOfValues-1)*(self.standardDeviation ** 3))
        print('Skewness:', skewness)
        return skewness

    def calcBeta(self):
        beta = self.correlation * \
            (self.standardDeviation/Stock.benchmarkStandardDeviation)
        print('Beta:', beta)
        return beta

    def calcAlpha(self):
        alpha = self.averageAnnualReturn - \
            (Stock.riskFreeRate+((Stock.benchmarkAverageAnnualReturn -
                                  Stock.riskFreeRate) * self.beta))
        print('Alpha:', alpha)
        return alpha

    def calcSharpe(self):
        sharpe = (self.averageAnnualReturn - Stock.riskFreeRate) / \
            self.standardDeviation
        print('Sharpe Ratio:', sharpe)
        return sharpe

    def calcSortino(self):
        sortino = (self.averageAnnualReturn - self.riskFreeRate) / \
            self.downsideDeviation
        print('Sortino Ratio:', sortino)
        return sortino

    def calcTreynor(self):
        treynor = (self.averageAnnualReturn - Stock.riskFreeRate)/self.beta
        print('Treynor Ratio:', treynor)
        return treynor

    def calcLinearRegression(self):
        dates = self.dates
        y = self.closeValues

        # First change dates to integers (days from first date)
        x = datesToDays(dates)

        x = np.array(x)
        y = np.array(y)

        # Estimate coefficients
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x

        # calculating regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1*m_x

        b = [b_0, b_1]

        formula = ''.join(
            ('y = ', str(round(float(b[0]), 2)), 'x + ', str(round(float(b[1]), 2))))
        print('Linear regression formula:', formula)

        # Stock.plot_regression_line(self, x, y, b)

        regression = []
        regression.append(b[0])
        regression.append(b[1])
        return regression

    def plot_regression_line(self, x, y, b):
        # plotting the actual points as scatter plot
        plt.scatter(self.dates, y, color="m",
                    marker="o", s=30)

        # predicted response vector
        y_pred = b[0] + b[1]*x

        # plotting the regression line
        plt.plot(self.dates, y_pred, color="g")

        # putting labels
        plt.title(self.name)
        plt.xlabel('Dates')
        plt.ylabel('Close Values')

        # function to show plot
        plt.show(block=False)
        for i in range(3, 0, -1):
            if i == 1:
                sys.stdout.write('Keeping plot open for ' +
                                 str(i) + ' second \r')
            else:
                sys.stdout.write('Keeping plot open for ' +
                                 str(i) + ' seconds \r')
            plt.pause(1)
            sys.stdout.flush()
        plt.close()


def datesToDays(dates):
    days = []
    firstDate = dates[0]
    days.append(0)
    for i in range(1, len(dates), 1):
        # Calculate days from first date to current date
        daysDiff = (dates[i]-firstDate).days
        days.append(daysDiff)
    return days


def isConnected():
    import socket  # To check internet connection
    print('Checking internet connection')
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
        print('\nList of benchmarks:')
        for i in range(0, len(benchmarks), 1):
            print(str(i+1) + '. ' +
                  benchmarks[i] + ' (' + benchmarksTicker[i] + ')')

        benchmark = str(input('Please choose a benchmark from the list: '))
        # benchmark = 'SPY' # TESTING

        if Functions.stringIsInt(benchmark) == True:
            if int(benchmark) <= len(benchmarks):
                benchmarkInt = int(benchmark)
                benchmark = benchmarks[benchmarkInt-1]
                benchmarkTicker = benchmarksTicker[benchmarkInt-1]
        else:
            for i in range(0, len(benchmarks), 1):
                if benchmark == benchmarks[i]:
                    benchmarkTicker = benchmarksTicker[i]
                    break
                if benchmark == benchmarksTicker[i] or benchmark == benchmarksTicker[i].lower():
                    benchmark = benchmarks[i]
                    benchmarkTicker = benchmarksTicker[i]
                    break

        if benchmarkTicker == '':
            print('Benchmark not found. Please use a benchmark from the list')

    print(benchmark, ' (', benchmarkTicker, ')', sep='')

    benchmark = Stock()
    benchmark.setName(benchmarkTicker)

    return benchmark


def stocksInit():
    listOfStocks = []

    isInteger = False
    while isInteger == False:
        temp = input('\nNumber of stocks to analyze (2 minimum): ')
        isInteger = Functions.stringIsInt(temp)
        if isInteger == True:
            numberOfStocks = int(temp)
        else:
            print('Please type an integer')

    # numberOfStocks = 5 # TESTING
    # print('How many stocks would you like to analyze? ', numberOfStocks)

    print('\nThis program can analyze stocks (GOOGL), mutual funds (VFINX), and ETFs (SPY)')
    print('For simplicity, all of them will be referred to as "stock"\n')

    # listOfGenericStocks = ['googl', 'aapl', 'vfinx', 'tsla', 'vthr']

    for i in range(0, numberOfStocks, 1):
        print('Stock', i + 1, end=' ')
        stockName = str(input('ticker: '))

        # stockName = listOfGenericStocks[i]
        # print(':', stockName)

        stockName = stockName.upper()
        listOfStocks.append(stockName)
        listOfStocks[i] = Stock()
        listOfStocks[i].setName(stockName)

    return listOfStocks


def timeFrameInit():
    isInteger = False
    while isInteger == False:
        print(
            '\nPlease enter the time frame in years (10 years or less recommended):', end='')
        temp = input(' ')
        isInteger = Functions.stringIsInt(temp)
        if isInteger == True:
            years = int(temp)
        else:
            print('Please type an integer')

    # years = 5 # TESTING
    # print('Years:', years)

    timeFrame = years
    return timeFrame


def dataMain(listOfStocks):
    print('\nGathering dates and close values')
    i = 0
    while i < len(listOfStocks):

        datesAndCloseList = Stock.datesAndClose(listOfStocks[i])
        if datesAndCloseList == 'Not available':
            del listOfStocks[i]
            if len(listOfStocks) == 0:
                print('No stocks to analyze. Ending program')
                exit()
        else:
            listOfStocks[i].allDates = datesAndCloseList[0]
            listOfStocks[i].allCloseValues = datesAndCloseList[1]

            # Clip list to fit time frame
            datesAndCloseList2 = Stock.datesAndCloseFitTimeFrame(
                listOfStocks[i])
            listOfStocks[i].dates = datesAndCloseList2[0]
            listOfStocks[i].closeValues = datesAndCloseList2[1]

            i += 1


def riskFreeRate():
    print('Quandl')
    url = ''.join(
        ('https://www.quandl.com/api/v3/datasets/USTREASURY/LONGTERMRATES.json?api_key=', apiQuandl))
    # https://www.quandl.com/api/v3/datasets/USTREASURY/LONGTERMRATES.json?api_key=KUh3U3hxke9tCimjhWEF

    print("\nSending request to:", url)
    f = requests.get(url)
    Functions.fromCache(f)
    json_data = f.text
    loaded_json = json.loads(json_data)
    riskFreeRate = (loaded_json['dataset']['data'][0][1])/100
    riskFreeRate = riskFreeRate * 100
    riskFreeRate = round(riskFreeRate, 2)
    print('Risk-free rate:', riskFreeRate, end='\n\n')

    if f.status_code == 404:
        print("Quandl not available")
        print('Returning 2.50 as risk-free rate', end='\n\n')
        # return 0.0250
        return 2.50

    return riskFreeRate


def returnMain(benchmark, listOfStocks):
    print('\nCalculating unadjusted return, Sharpe ratio, Sortino ratio, and Treynor ratio\n')
    print('Getting risk-free rate from current 10-year treasury bill rates', end='\n\n')
    Stock.riskFreeRate = riskFreeRate()
    print(benchmark.name, end='\n\n')
    benchmark.annualReturn = Stock.calcAnnualReturn(benchmark)
    if benchmark.annualReturn == 'Not available':
        print('Please use a lower time frame\nEnding program')
        exit()
    benchmark.averageAnnualReturn = Stock.calcAverageAnnualReturn(benchmark)
    benchmark.standardDeviation = Stock.calcStandardDeviation(benchmark)

    # Make benchmark data global
    Stock.benchmarkDates = benchmark.dates
    Stock.benchmarkCloseValues = benchmark.closeValues
    Stock.benchmarkAverageAnnualReturn = benchmark.averageAnnualReturn
    Stock.benchmarkStandardDeviation = benchmark.standardDeviation

    i = 0
    while i < len(listOfStocks):
        print('\n' + listOfStocks[i].name, end='\n\n')

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

        # Calculate everything for each stock
        listOfStocks[i].annualReturn = Stock.calcAnnualReturn(listOfStocks[i])
        if listOfStocks[i].annualReturn == 'Not available':
            print('Removing', listOfStocks[i].name, 'from list of stocks')
            del listOfStocks[i]
            if len(listOfStocks) == 0:
                print('No stocks to analyze. Ending program')
                exit()
        else:
            listOfStocks[i].averageAnnualReturn = Stock.calcAverageAnnualReturn(
                listOfStocks[i])
            listOfStocks[i].correlation = Stock.calcCorrelation(
                listOfStocks[i], benchmarkMatchDatesAndCloseValues[1])
            listOfStocks[i].standardDeviation = Stock.calcStandardDeviation(
                listOfStocks[i])
            listOfStocks[i].downsideDeviation = Stock.calcDownsideDeviation(
                listOfStocks[i])
            listOfStocks[i].kurtosis = Stock.calcKurtosis(
                listOfStocks[i])
            listOfStocks[i].skewness = Stock.calcSkewness(
                listOfStocks[i])
            listOfStocks[i].beta = Stock.calcBeta(listOfStocks[i])
            listOfStocks[i].alpha = Stock.calcAlpha(listOfStocks[i])
            listOfStocks[i].sharpe = Stock.calcSharpe(listOfStocks[i])
            listOfStocks[i].sortino = Stock.calcSortino(listOfStocks[i])
            listOfStocks[i].treynor = Stock.calcTreynor(listOfStocks[i])
            listOfStocks[i].linearRegression = Stock.calcLinearRegression(
                listOfStocks[i])

            i += 1

    print('\nNumber of stocks from original list that fit time frame:',
          len(listOfStocks))


def indicatorInit():
    # Runs correlation or regression study
    indicatorFound = False
    listOfIndicators = ['Expense Ratio',
                        'Market Capitalization', 'Turnover', 'Persistence']
    print('\n', end='')
    while indicatorFound == False:
        print('List of indicators:')
        for i in range(0, len(listOfIndicators), 1):
            print(str(i + 1) + '. ' + listOfIndicators[i])

        indicator = str(input('Choose an indicator from the list: '))

        # indicator = 'expense ratio' # TESTING

        if Functions.stringIsInt(indicator) == True:
            if int(indicator) <= 4:
                indicator = listOfIndicators[int(indicator)-1]
                indicatorFound = True
        else:
            indicatorFormats = [
                indicator.upper(), indicator.lower(), indicator.title()]
            for i in range(0, len(indicatorFormats), 1):
                for j in range(0, len(listOfIndicators), 1):
                    if listOfIndicators[j] == indicatorFormats[i]:
                        indicator = listOfIndicators[j]
                        indicatorFound = True
                        break

        if indicatorFound == False:
            print('Please choose an indicator from the list')

    return indicator


def calcIndicatorCorrelation(listOfIndicatorValues, listOfReturns):
    correlationList = []
    for i in range(0, len(listOfReturns), 1):
        correlation = np.corrcoef(
            listOfIndicatorValues, listOfReturns[i])[0, 1]
        correlationList.append(correlation)
    return correlationList


def calcIndicatorRegression(listOfIndicatorValues, listOfReturns):
    regressionList = []
    x = np.array(listOfIndicatorValues)
    for i in range(0, len(listOfReturns), 1):
        y = np.array(listOfReturns[i])

        # Estimate coefficients
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x

        # calculating regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1*m_x

        b = [b_0, b_1]

        regression = []
        regression.append(b[0])
        regression.append(b[1])
        regressionList.append(regression)

        # plot_regression_line(x, y, b, i)

    return regressionList


def plot_regression_line(x, y, b, i):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    listOfReturnStrings = ['Average Annual Return',
                           'Sharpe Ratio', 'Sortino Ratio', 'Treynor Ratio', 'Alpha']

    plt.title(Stock.indicator + ' and ' + listOfReturnStrings[i])
    if Stock.indicator == 'Expense Ratio':
        plt.xlabel(Stock.indicator + ' (%)')
    else:
        plt.xlabel(Stock.indicator)

    if i == 0:
        plt.ylabel(listOfReturnStrings[i] + ' (%)')
    else:
        plt.ylabel(listOfReturnStrings[i])

    # function to show plot
    plt.show(block=False)
    for i in range(2, 0, -1):
        if i == 1:
            sys.stdout.write('Keeping plot open for ' +
                             str(i) + ' second \r')
        else:
            sys.stdout.write('Keeping plot open for ' +
                             str(i) + ' seconds \r')
        plt.pause(1)
        sys.stdout.flush()
    sys.stdout.write(
        '                                                                         \r')
    sys.stdout.flush()
    plt.close()


def indicatorMain(listOfStocks):
    Stock.indicator = indicatorInit()
    print(Stock.indicator, end='\n\n')

    # indicatorValuesGenericExpenseRatio = [2.5, 4.3, 3.1, 2.6, 4.2] # TESTING

    listOfStocksIndicatorValues = []
    for i in range(0, len(listOfStocks), 1):
        indicatorValueFound = False
        while indicatorValueFound == False:
            if Stock.indicator == 'Expense Ratio':
                indicatorValue = str(
                    input(Stock.indicator + ' for ' + listOfStocks[i].name + ' (%): '))
            elif Stock.indicator == 'Persistence':
                indicatorValue = str(
                    input(Stock.indicator + ' for ' + listOfStocks[i].name + ' (years): '))
            elif Stock.indicator == 'Turnover':
                indicatorValue = str(input(
                    Stock.indicator + ' for ' + listOfStocks[i].name + ' in the last ' + str(Stock.timeFrame) + ' years: '))
            elif Stock.indicator == 'Market Capitalization':
                indicatorValue = str(
                    input(Stock.indicator + ' of ' + listOfStocks[i].name + ': '))
            else:
                print('Something is wrong. Indicator was not found. Ending program.')
                exit()

            if Functions.strintIsFloat(indicatorValue) == True:
                listOfStocks[i].indicatorValue = float(indicatorValue)
                indicatorValueFound = True
            else:
                print('Please enter a number')

        # listOfStocks[i].indicatorValue = indicatorValuesGenericExpenseRatio[i] # TESTING
        listOfStocksIndicatorValues.append(listOfStocks[i].indicatorValue)

    listOfReturns = []  # A list that matches the above list with return values [[averageAnnualReturn1, aAR2, aAR3], [sharpe1, sharpe2, sharpe3], etc.]
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].averageAnnualReturn)
    listOfReturns.append(tempListOfReturns)
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].sharpe)
    listOfReturns.append(tempListOfReturns)
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].sortino)
    listOfReturns.append(tempListOfReturns)
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].treynor)
    listOfReturns.append(tempListOfReturns)
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].alpha)
    listOfReturns.append(tempListOfReturns)

    # Create list of each indicator (e.g. expense ratio)
    listOfIndicatorValues = []
    for i in range(0, len(listOfStocks), 1):
        listOfIndicatorValues.append(listOfStocks[i].indicatorValue)

    Stock.indicatorCorrelation = calcIndicatorCorrelation(
        listOfIndicatorValues, listOfReturns)

    listOfReturnStrings = ['Average Annual Return',
                           'Sharpe Ratio', 'Sortino Ratio', 'Treynor Ratio', 'Alpha']
    print('\n', end='')
    for i in range(0, len(Stock.indicatorCorrelation), 1):
        print('Correlation with ' + Stock.indicator.lower() + ' and ' +
              listOfReturnStrings[i].lower() + ': ' + str(Stock.indicatorCorrelation[i]))

    Stock.indicatorRegression = calcIndicatorRegression(
        listOfIndicatorValues, listOfReturns)
    print('\n', end='')
    for i in range(0, len(Stock.indicatorCorrelation), 1):
        formula = ''.join(
            ('y = ', str(round(float(Stock.indicatorRegression[i][0]), 2)), 'x + ', str(round(float(Stock.indicatorRegression[i][1]), 2))))
        print('Linear regression equation for ' + Stock.indicator.lower() + ' and ' +
              listOfReturnStrings[i].lower() + ': ' + formula)


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

    # Choose indicator and calculate correlation with indicator
    indicatorMain(listOfStocks)

    exit()


if __name__ == "__main__":
    main()
