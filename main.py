# https://github.com/andrewkdinh/fund-indicators
# Determine indicators of overperforming mutual funds
# Andrew Dinh
# Python 3.6.7

# Required
from bs4 import BeautifulSoup
import requests
import json
import datetime
import Functions
import numpy as np
import re
import os.path

# Required for linear regression
import matplotlib.pyplot as plt
import sys

# Optional
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import time
import random
import requests_cache
requests_cache.install_cache(
    'cache', backend='sqlite', expire_after=43200)  # 12 hours

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
    timeFrame = 0  # Months
    riskFreeRate = 0
    indicator = ''

    # BENCHMARK VALUES
    benchmarkDates = []
    benchmarkCloseValues = []
    benchmarkAverageMonthlyReturn = 0
    benchmarkStandardDeviation = 0

    # INDICATOR VALUES
    indicatorCorrelation = []
    indicatorRegression = []
    persTimeFrame = 0

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
        self.averageMonthlyReturn = 0
        self.monthlyReturn = []
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
        if json_data == 'Unknown symbol' or f.status_code != 200:
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

        if len(loaded_json) == 1 or f.status_code != 200 or len(loaded_json) == 0:
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
        if len(loaded_json) == 1 or f.status_code != 200 or loaded_json['startDate'] == None:
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

        # Determine if close value list has value of zero
        # AKA https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=RGN&outputsize=full&apikey=O42ICUV58EIZZQMU
        for i in datesAndCloseList[1]:
            if i == 0:
                print('Found close value of 0. This is likely something like ticker RGN (Daily Time Series with Splits and Dividend Events)')
                print('Removing', self.name,
                      'from list of stocks to ensure compability later')
                return 'Not available'

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
            days=self.timeFrame*30)
        print('\n', self.timeFrame, ' months ago: ', firstDate, sep='')
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

    def calcAverageMonthlyReturn(self):  # pylint: disable=E0202
        # averageMonthlyReturn = (float(self.closeValues[len(self.closeValues)-1]/self.closeValues[0])**(1/(self.timeFrame)))-1
        # averageMonthlyReturn = averageMonthlyReturn * 100
        averageMonthlyReturn = sum(self.monthlyReturn)/self.timeFrame
        print('Average monthly return:', averageMonthlyReturn)
        return averageMonthlyReturn

    def calcMonthlyReturn(self):
        monthlyReturn = []

        # Calculate monthly return in order from oldest to newest
        monthlyReturn = []
        for i in range(0, self.timeFrame, 1):
            firstDate = datetime.datetime.now().date() - datetime.timedelta(
                days=(self.timeFrame-i)*30)
            secondDate = datetime.datetime.now().date() - datetime.timedelta(
                days=(self.timeFrame-i-1)*30)

            # Find closest dates to firstDate and lastDate
            firstDate = Functions.getNearest(self.dates, firstDate)
            secondDate = Functions.getNearest(self.dates, secondDate)

            if firstDate == secondDate:
                print('Closest date is', firstDate,
                      'which is after the given time frame.')
                return 'Not available'

            # Get corresponding close values and calculate monthly return
            for i in range(0, len(self.dates), 1):
                if self.dates[i] == firstDate:
                    firstClose = self.closeValues[i]
                elif self.dates[i] == secondDate:
                    secondClose = self.closeValues[i]
                    break

            monthlyReturnTemp = (secondClose/firstClose)-1
            monthlyReturnTemp = monthlyReturnTemp * 100
            monthlyReturn.append(monthlyReturnTemp)

        # print('Monthly return over the past', self.timeFrame, 'months:', monthlyReturn)
        return monthlyReturn

    def calcCorrelation(self, closeList):
        correlation = np.corrcoef(
            self.closeValuesMatchBenchmark, closeList)[0, 1]
        print('Correlation with benchmark:', correlation)
        return correlation

    def calcStandardDeviation(self):
        numberOfValues = self.timeFrame
        mean = self.averageMonthlyReturn
        standardDeviation = (
            (sum((self.monthlyReturn[x]-mean)**2 for x in range(0, numberOfValues, 1)))/(numberOfValues-1))**(1/2)
        print('Standard Deviation:', standardDeviation)
        return standardDeviation

    def calcDownsideDeviation(self):
        numberOfValues = self.timeFrame
        targetReturn = self.averageMonthlyReturn
        downsideDeviation = (
            (sum(min(0, (self.monthlyReturn[x]-targetReturn))**2 for x in range(0, numberOfValues, 1)))/(numberOfValues-1))**(1/2)
        print('Downside Deviation:', downsideDeviation)
        return downsideDeviation

    def calcKurtosis(self):
        numberOfValues = self.timeFrame
        mean = self.averageMonthlyReturn
        kurtosis = (sum((self.monthlyReturn[x]-mean)**4 for x in range(
            0, numberOfValues, 1)))/((numberOfValues-1)*(self.standardDeviation ** 4))
        print('Kurtosis:', kurtosis)
        return kurtosis

    def calcSkewness(self):
        numberOfValues = self.timeFrame
        mean = self.averageMonthlyReturn
        skewness = (sum((self.monthlyReturn[x]-mean)**3 for x in range(
            0, numberOfValues, 1)))/((numberOfValues-1)*(self.standardDeviation ** 3))
        print('Skewness:', skewness)
        return skewness

    def calcBeta(self):
        beta = self.correlation * \
            (self.standardDeviation/Stock.benchmarkStandardDeviation)
        print('Beta:', beta)
        return beta

    def calcAlpha(self):
        alpha = self.averageMonthlyReturn - \
            (Stock.riskFreeRate+((Stock.benchmarkAverageMonthlyReturn -
                                  Stock.riskFreeRate) * self.beta))
        print('Alpha:', alpha)
        return alpha

    def calcSharpe(self):
        sharpe = (self.averageMonthlyReturn - Stock.riskFreeRate) / \
            self.standardDeviation
        print('Sharpe Ratio:', sharpe)
        return sharpe

    def calcSortino(self):
        sortino = (self.averageMonthlyReturn - self.riskFreeRate) / \
            self.downsideDeviation
        print('Sortino Ratio:', sortino)
        return sortino

    def calcTreynor(self):
        treynor = (self.averageMonthlyReturn - Stock.riskFreeRate)/self.beta
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

    def scrapeYahooFinance(self):
        # Determine if ETF, Mutual fund, or stock
        print('Determining if Yahoo Finance has data for', self.name, end=": ")
        url = ''.join(('https://finance.yahoo.com/quote/',
                       self.name, '?p=', self.name))
        if requests.get(url).history:
            print('No')
            return 'Not available'
        else:
            print('Yes')

        stockType = ''
        url2 = ''.join(('https://finance.yahoo.com/lookup?s=', self.name))
        print('Sending request to:', url2)
        raw_html = requests.get(url2).text

        soup2 = BeautifulSoup(raw_html, 'html.parser')
        # Type (Stock, ETF, Mutual Fund)
        r = soup2.find_all(
            'td', attrs={'class': 'data-col4 Ta(start) Pstart(20px) Miw(30px)'})
        t = soup2.find_all('a', attrs={'class': 'Fw(b)'})  # Name and class
        z = soup2.find_all('td', attrs={
                           'class': 'data-col1 Ta(start) Pstart(10px) Miw(80px)'})  # Name of stock
        listNames = []
        for i in t:
            if len(i.text.strip()) < 6:
                listNames.append(i.text.strip())
        for i in range(0, len(listNames), 1):
            if listNames[i] == self.name:
                break
        r = r[i].text.strip()
        z = z[i].text.strip()
        print('Name:', z)

        if r == 'ETF':
            stockType = 'ETF'
        elif r == 'Stocks':
            stockType = 'Stock'
        elif r == 'Mutual Fund':
            stockType = 'Fund'
        else:
            print('Could not determine fund type')
            return 'Not available'
        print('Type:', stockType)

        if Stock.indicator == 'Expense Ratio':
            if stockType == 'Stock':
                print(
                    self.name, 'is a stock, and therefore does not have an expense ratio')
                return 'Not available'

            url = ''.join(('https://finance.yahoo.com/quote/',
                           self.name, '?p=', self.name))
            # https://finance.yahoo.com/quote/SPY?p=SPY
            print('Sending request to:', url)
            raw_html = requests.get(url).text
            soup = BeautifulSoup(raw_html, 'html.parser')

            r = soup.find_all('span', attrs={'class': 'Trsdu(0.3s)'})
            if r == []:
                print('Something went wrong with scraping expense ratio')
                return('Not available')

            if stockType == 'ETF':
                for i in range(len(r)-1, 0, -1):
                    s = r[i].text.strip()
                    if s[-1] == '%':
                        break
            elif stockType == 'Fund':
                count = 0  # Second in set
                for i in range(0, len(r)-1, 1):
                    s = r[i].text.strip()
                    if s[-1] == '%' and count == 0:
                        count += 1
                    elif s[-1] == '%' and count == 1:
                        break

            if s[-1] == '%':
                expenseRatio = float(s.replace('%', ''))
            else:
                print('Something went wrong with scraping expense ratio')
                return 'Not available'
            print(str(expenseRatio) + '%')
            return expenseRatio

        elif Stock.indicator == 'Market Capitalization':
            url = ''.join(('https://finance.yahoo.com/quote/',
                           self.name, '?p=', self.name))
            # https://finance.yahoo.com/quote/GOOGL?p=GOOGL
            raw_html = requests.get(url).text
            soup = BeautifulSoup(raw_html, 'html.parser')
            r = soup.find_all(
                'span', attrs={'class': 'Trsdu(0.3s)'})
            if r == []:
                print('Something went wrong with scraping market capitalization')
                return 'Not available'
            marketCap = 0
            for t in r:
                s = t.text.strip()
                if s[-1] == 'B':
                    print(s, end='')
                    s = s.replace('B', '')
                    marketCap = float(s) * 1000000000  # 1 billion
                    break
                elif s[-1] == 'M':
                    print(s, end='')
                    s = s.replace('M', '')
                    marketCap = float(s) * 1000000  # 1 million
                    break
                elif s[-1] == 'K':
                    print(s, end='')
                    s = s.replace('K', '')
                    marketCap = float(s) * 1000  # 1 thousand
                    break
            if marketCap == 0:
                print('\nSomething went wrong with scraping market capitalization')
                return 'Not available'
            marketCap = int(marketCap)
            print(' =', marketCap)
            return marketCap

        elif Stock.indicator == 'Turnover':
            if stockType == 'Stock':
                print(self.name, 'is a stock, and therefore does not have turnover')
                return 'Not available'

            if stockType == 'Fund':
                url = ''.join(('https://finance.yahoo.com/quote/',
                               self.name, '?p=', self.name))
                # https://finance.yahoo.com/quote/SPY?p=SPY
                print('Sending request to', url)
                raw_html = requests.get(url).text
                soup = BeautifulSoup(raw_html, 'html.parser')

                r = soup.find_all(
                    'span', attrs={'class': 'Trsdu(0.3s)'})
                if r == []:
                    print('Something went wrong without scraping turnover')
                    return 'Not available'
                turnover = 0
                for i in range(len(r)-1, 0, -1):
                    s = r[i].text.strip()
                    if s[-1] == '%':
                        turnover = float(s.replace('%', ''))
                        break
            if stockType == 'ETF':
                url = ''.join(('https://finance.yahoo.com/quote/',
                               self.name, '/profile?p=', self.name))
                # https://finance.yahoo.com/quote/SPY/profile?p=SPY
                print('Sending request to', url)
                raw_html = requests.get(url).text
                soup = BeautifulSoup(raw_html, 'html.parser')

                r = soup.find_all(
                    'span', attrs={'class': 'W(20%) D(b) Fl(start) Ta(e)'})
                if r == []:
                    print('Something went wrong without scraping turnover')
                    return 'Not available'
                turnover = 0
                for i in range(len(r)-1, 0, -1):
                    s = r[i].text.strip()
                    if s[-1] == '%':
                        turnover = float(s.replace('%', ''))
                        break

            if turnover == 0:
                print('Something went wrong with scraping turnover')
                return 'Not available'
            print(str(turnover) + '%')
            return turnover

    def indicatorManual(self):
        indicatorValueFound = False
        while indicatorValueFound == False:
            if Stock.indicator == 'Expense Ratio':
                indicatorValue = str(
                    input(Stock.indicator + ' for ' + self.name + ' (%): '))
            elif Stock.indicator == 'Persistence':
                indicatorValue = str(
                    input(Stock.indicator + ' for ' + self.name + ' (years): '))
            elif Stock.indicator == 'Turnover':
                indicatorValue = str(input(
                    Stock.indicator + ' for ' + self.name + ' in the last ' + str(Stock.timeFrame) + ' years: '))
            elif Stock.indicator == 'Market Capitalization':
                indicatorValue = str(
                    input(Stock.indicator + ' of ' + self.name + ': '))
            else:
                print('Something is wrong. Indicator was not found. Ending program.')
                exit()

            if Functions.strintIsFloat(indicatorValue) == True:
                indicatorValueFound = True
                return float(indicatorValue)
            else:
                print('Please enter a number')

    def calcPersistence(self):
        persistenceFirst = (sum(self.monthlyReturn[i] for i in range(
            0, Stock.persTimeFrame, 1))) / Stock.persTimeFrame
        persistenceSecond = self.averageMonthlyReturn
        persistence = persistenceSecond-persistenceFirst
        print('Change in average monthly return:', persistence)
        return persistence


def datesToDays(dates):
    days = []
    firstDate = dates[0]
    days.append(0)
    for i in range(1, len(dates), 1):
        # Calculate days from first date to current date
        daysDiff = (dates[i]-firstDate).days
        days.append(daysDiff)
    return days


def benchmarkInit():
    # Treat benchmark like stock
    benchmarkTicker = ''
    benchmarks = ['S&P500', 'DJIA', 'Russell 3000', 'MSCI EAFE']
    benchmarksTicker = ['SPY', 'DJIA', 'VTHR', 'EFT']
    print('\nList of benchmarks:')
    for i in range(0, len(benchmarks), 1):
        print(str(i+1) + '. ' +
              benchmarks[i] + ' (' + benchmarksTicker[i] + ')')
    while benchmarkTicker == '':

        benchmark = str(input('Please choose a benchmark from the list: '))
        # benchmark = 'SPY' # TESTING

        if Functions.stringIsInt(benchmark) == True:
            if int(benchmark) <= len(benchmarks) and int(benchmark) > 0:
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

    print('\nThis program can analyze stocks (GOOGL), mutual funds (VFINX), and ETFs (SPY)')
    print('For simplicity, all of them will be referred to as "stock"')

    found = False
    while found == False:
        print('\nMethods:')
        method = 0
        methods = ['Read from a file', 'Enter manually',
                   'U.S. News popular funds (~35)', 'Kiplinger top-performing funds (50)', 'TheStreet top-rated mutual funds (20)']
        for i in range(0, len(methods), 1):
            print(str(i+1) + '. ' + methods[i])
        while method == 0 or method > len(methods):
            method = str(input('Which method? '))
            if Functions.stringIsInt(method) == True:
                method = int(method)
                if method == 0 or method > len(methods):
                    print('Please choose a valid method')
            else:
                method = 0
                print('Please choose a number')
        print('')

        if method == 1:
            defaultFiles = ['.gitignore', 'LICENSE', 'main.py', 'Functions.py',
                            'README.md', 'requirements.txt', 'cache.sqlite', '_test_runner.py']  # Added by repl.it for whatever reason
            stocksFound = False
            print('Files in current directory (not including default files): ')
            listOfFilesTemp = [f for f in os.listdir() if os.path.isfile(f)]
            listOfFiles = []
            for files in listOfFilesTemp:
                if files[0] != '.' and any(x in files for x in defaultFiles) != True:
                    listOfFiles.append(files)
            for i in range(0, len(listOfFiles), 1):
                if listOfFiles[i][0] != '.':
                    print(str(i+1) + '. ' + listOfFiles[i])
            while stocksFound == False:
                fileName = str(input('What is the file number/name? '))
                if Functions.stringIsInt(fileName) == True:
                    if int(fileName) < len(listOfFiles)+1 and int(fileName) > 0:
                        fileName = listOfFiles[int(fileName)-1]
                        print(fileName)
                if Functions.fileExists(fileName) == True:
                    listOfStocks = []
                    file = open(fileName, 'r')
                    n = file.read()
                    file.close()
                    s = re.findall(r'[^,;\s]+', n)
                    for i in s:
                        if str(i) != '' and Functions.hasNumbers(str(i)) == False:
                            listOfStocks.append(str(i).upper())
                    stocksFound = True
                else:
                    print('File not found')
            for i in range(0, len(listOfStocks), 1):
                stockName = listOfStocks[i].upper()
                listOfStocks[i] = Stock()
                listOfStocks[i].setName(stockName)

            for k in listOfStocks:
                print(k.name, end=' ')
            print('\n' + str(len(listOfStocks)) + ' stocks total')

        elif method == 2:
            isInteger = False
            while isInteger == False:
                temp = input('\nNumber of stocks to analyze (2 minimum): ')
                isInteger = Functions.stringIsInt(temp)
                if isInteger == True:
                    if int(temp) >= 2:
                        numberOfStocks = int(temp)
                    else:
                        print('Please type a number greater than or equal to 2')
                        isInteger = False
                else:
                    print('Please type an integer')

            i = 0
            while i < numberOfStocks:
                print('Stock', i + 1, end=' ')
                stockName = str(input('ticker: '))

                if stockName != '' and Functions.hasNumbers(stockName) == False:
                    stockName = stockName.upper()
                    listOfStocks.append(stockName)
                    listOfStocks[i] = Stock()
                    listOfStocks[i].setName(stockName)
                    i += 1
                else:
                    print('Invalid ticker')

        elif method == 3:
            listOfStocks = []
            url = 'https://money.usnews.com/funds/mutual-funds/most-popular'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            print('Sending request to', url)
            f = requests.get(url, headers=headers)
            Functions.fromCache(f)
            raw_html = f.text
            soup = BeautifulSoup(raw_html, 'html.parser')

            file = open('usnews-stocks.txt', 'w')
            r = soup.find_all(
                'span', attrs={'class': 'text-smaller text-muted'})
            for k in r:
                print(k.text.strip(), end=' ')
                listOfStocks.append(k.text.strip())
                file.write(str(k.text.strip()) + '\n')
            file.close()

            for i in range(0, len(listOfStocks), 1):
                stockName = listOfStocks[i].upper()
                listOfStocks[i] = Stock()
                listOfStocks[i].setName(stockName)

            print('\n' + str(len(listOfStocks)) + ' mutual funds total')

        elif method == 4:
            listOfStocks = []
            url = 'https://www.kiplinger.com/tool/investing/T041-S001-top-performing-mutual-funds/index.php'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
            print('Sending request to', url)
            f = requests.get(url, headers=headers)
            Functions.fromCache(f)
            raw_html = f.text
            soup = BeautifulSoup(raw_html, 'html.parser')

            file = open('kiplinger-stocks.txt', 'w')
            r = soup.find_all('a', attrs={'style': 'font-weight:700;'})
            for k in r:
                print(k.text.strip(), end=' ')
                listOfStocks.append(k.text.strip())
                file.write(str(k.text.strip()) + '\n')
            file.close()

            for i in range(0, len(listOfStocks), 1):
                stockName = listOfStocks[i].upper()
                listOfStocks[i] = Stock()
                listOfStocks[i].setName(stockName)

            print('\n' + str(len(listOfStocks)) + ' mutual funds total')

        elif method == 5:
            listOfStocks = []
            url = 'https://www.thestreet.com/topic/21421/top-rated-mutual-funds.html'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
            print('Sending request to', url)
            f = requests.get(url, headers=headers)
            Functions.fromCache(f)
            raw_html = f.text
            soup = BeautifulSoup(raw_html, 'html.parser')

            file = open('thestreet-stocks.txt', 'w')
            r = soup.find_all('a')
            for k in r:
                if len(k.text.strip()) == 5:
                    n = re.findall(r'^/quote/.*\.html', k['href'])
                    if len(n) != 0:
                        print(k.text.strip(), end=' ')
                        listOfStocks.append(k.text.strip())
                        file.write(str(k.text.strip()) + '\n')
            file.close()

            for i in range(0, len(listOfStocks), 1):
                stockName = listOfStocks[i].upper()
                listOfStocks[i] = Stock()
                listOfStocks[i].setName(stockName)

            print('\n' + str(len(listOfStocks)) + ' mutual funds total')

        if len(listOfStocks) < 2:
            print('Please choose another method')
        else:
            found = True

    return listOfStocks


def asyncData(benchmark, listOfStocks):
    # Make list of urls to send requests to
    urlList = []
    # Benchmark
    url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=',
                   benchmark.name, '&outputsize=full&apikey=', apiAV))
    urlList.append(url)

    # Stocks
    for i in range(0, len(listOfStocks), 1):
        # Alpha Vantage
        url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=',
                       listOfStocks[i].name, '&outputsize=full&apikey=', apiAV))
        urlList.append(url)

    # Risk-free rate
    url = ''.join(
        ('https://www.quandl.com/api/v3/datasets/USTREASURY/LONGTERMRATES.json?api_key=', apiQuandl))
    urlList.append(url)

    # Yahoo Finance
    for i in range(0, len(listOfStocks), 1):
        url = ''.join(('https://finance.yahoo.com/quote/',
                       listOfStocks[i].name, '?p=', listOfStocks[i].name))
        urlList.append(url)
    for i in range(0, len(listOfStocks), 1):
        url = ''.join(
            ('https://finance.yahoo.com/lookup?s=', listOfStocks[i].name))
        urlList.append(url)

    # Send async requests
    print('\nSending async requests (Assuming Alpha Vantage is first choice)')
    with PoolExecutor(max_workers=3) as executor:
        for _ in executor.map(sendAsync, urlList):
            pass

    return


def sendAsync(url):
    time.sleep(random.randrange(0, 2))
    print('Sending request to', url)
    requests.get(url)
    return


def timeFrameInit():
    isInteger = False
    while isInteger == False:
        print(
            '\nPlease enter the time frame in months (<60 months recommended):', end='')
        temp = input(' ')
        isInteger = Functions.stringIsInt(temp)
        if isInteger == True:
            if int(temp) > 1:
                months = int(temp)
            else:
                print('Please enter a number greater than 1')
                isInteger = False
        else:
            print('Please type an integer')

    timeFrame = months
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

    if f.status_code != 200:
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
    benchmark.monthlyReturn = Stock.calcMonthlyReturn(benchmark)
    if benchmark.monthlyReturn == 'Not available':
        print('Please use a lower time frame\nEnding program')
        exit()
    benchmark.averageMonthlyReturn = Stock.calcAverageMonthlyReturn(benchmark)
    benchmark.standardDeviation = Stock.calcStandardDeviation(benchmark)

    # Make benchmark data global
    Stock.benchmarkDates = benchmark.dates
    Stock.benchmarkCloseValues = benchmark.closeValues
    Stock.benchmarkAverageMonthlyReturn = benchmark.averageMonthlyReturn
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
        listOfStocks[i].monthlyReturn = Stock.calcMonthlyReturn(
            listOfStocks[i])
        if listOfStocks[i].monthlyReturn == 'Not available':
            print('Removing', listOfStocks[i].name, 'from list of stocks')
            del listOfStocks[i]
            if len(listOfStocks) == 0:
                print('No stocks fit time frame. Ending program')
                exit()
        else:
            listOfStocks[i].averageMonthlyReturn = Stock.calcAverageMonthlyReturn(
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
    if len(listOfStocks) < 2:
        print('Cannot proceed to the next step. Exiting program.')
        exit()


def indicatorInit():
    # Runs correlation or regression study
    indicatorFound = False
    listOfIndicators = ['Expense Ratio',
                        'Market Capitalization', 'Turnover', 'Persistence']
    print('\n', end='')
    print('List of indicators:')
    for i in range(0, len(listOfIndicators), 1):
        print(str(i + 1) + '. ' + listOfIndicators[i])
    while indicatorFound == False:
        indicator = str(input('Choose an indicator from the list: '))

        # indicator = 'expense ratio' # TESTING

        if Functions.stringIsInt(indicator) == True:
            if int(indicator) <= 4 and int(indicator) > 0:
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
            print('Please choose an indicator from the list\n')

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
    listOfReturnStrings = ['Average Monthly Return',
                           'Sharpe Ratio', 'Sortino Ratio', 'Treynor Ratio', 'Alpha']

    plt.title(Stock.indicator + ' and ' + listOfReturnStrings[i])
    if Stock.indicator == 'Expense Ratio' or Stock.indicator == 'Turnover':
        plt.xlabel(Stock.indicator + ' (%)')
    elif Stock.indicator == 'Persistence':
        plt.xlabel(Stock.indicator + ' (Difference in average monthly return)')
    else:
        plt.xlabel(Stock.indicator)

    if i == 0:
        plt.ylabel(listOfReturnStrings[i] + ' (%)')
    else:
        plt.ylabel(listOfReturnStrings[i])

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
    sys.stdout.write(
        '                                                                         \r')
    sys.stdout.flush()
    plt.close()


def persistenceTimeFrame():
    print('\nTime frame you chose was', Stock.timeFrame, 'months')
    persTimeFrameFound = False
    while persTimeFrameFound == False:
        persistenceTimeFrame = str(
            input('Please choose how many months to measure persistence: '))
        if Functions.stringIsInt(persistenceTimeFrame) == True:
            if int(persistenceTimeFrame) > 0 and int(persistenceTimeFrame) < Stock.timeFrame - 1:
                persistenceTimeFrame = int(persistenceTimeFrame)
                persTimeFrameFound = True
            else:
                print('Please choose a number between 0 and',
                      Stock.timeFrame, end='\n')
        else:
            print('Please choose an integer between 0 and',
                  Stock.timeFrame, end='\n')

    return persistenceTimeFrame


def indicatorMain(listOfStocks):
    print('\n' + str(Stock.indicator) + '\n')

    listOfStocksIndicatorValues = []
    for i in range(0, len(listOfStocks), 1):
        print(listOfStocks[i].name)
        if Stock.indicator != 'Persistence':
            listOfStocks[i].indicatorValue = Stock.scrapeYahooFinance(
                listOfStocks[i])
        else:
            listOfStocks[i].indicatorValue = Stock.calcPersistence(
                listOfStocks[i])
        print('')

        if listOfStocks[i].indicatorValue == 'Not available':
            listOfStocks[i].indicatorValue = Stock.indicatorManual(
                listOfStocks[i])

        listOfStocksIndicatorValues.append(listOfStocks[i].indicatorValue)

    listOfReturns = []  # A list that matches the above list with return values [[averageMonthlyReturn1, aAR2, aAR3], [sharpe1, sharpe2, sharpe3], etc.]
    tempListOfReturns = []
    for i in range(0, len(listOfStocks), 1):
        tempListOfReturns.append(listOfStocks[i].averageMonthlyReturn)
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

    listOfReturnStrings = ['Average Monthly Return',
                           'Sharpe Ratio', 'Sortino Ratio', 'Treynor Ratio', 'Alpha']
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
    # Check that all required packages are installed
    packagesInstalled = Functions.checkPackages(
        ['numpy', 'requests', 'bs4', 'requests_cache'])
    if not packagesInstalled:
        exit()
    else:
        print('All required packages are installed')

    # Check python version is above 3.3
    pythonVersionGood = Functions.checkPythonVersion()
    if not pythonVersionGood:
        return

    # Test internet connection

    internetConnection = Functions.isConnected()
    if not internetConnection:
        return
    else:
        Functions.getJoke()

    # Functions.getJoke()

    # Choose benchmark and makes it class Stock
    benchmark = benchmarkInit()
    # Add it to a list to work with other functions
    benchmarkAsList = [benchmark]

    # Asks for stock(s) ticker and makes them class Stock
    listOfStocks = stocksInit()

    # Determine time frame (Years)
    timeFrame = timeFrameInit()
    Stock.timeFrame = timeFrame  # Needs to be a global variable for all stocks

    # Choose indicator
    Stock.indicator = indicatorInit()
    # Choose time frame for initial persistence
    if Stock.indicator == 'Persistence':
        Stock.persTimeFrame = persistenceTimeFrame()

    # Send async request to AV for listOfStocks and benchmark
    asyncData(benchmark, listOfStocks)

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
