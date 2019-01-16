# ExpenseRatio.py
# Andrew Dinh
# Python 3.6.7
# Description:
'''
Calculates return for each stock from the lists from ExpenseRatio.py
listOfReturn = [Unadjsted Return, Sharpe Ratio, Sortino Ratio, Treynor Ratio, Jensen's Alpha]
'''

from StockData import StockData
import datetime
from Functions import Functions

class Return:
    def __init__(self, newListOfReturn = [], newTimeFrame = [], newBeta = 0, newStandardDeviation = 0, newNegativeStandardDeviation = 0, newMarketReturn = 0, newSize = 0, newSizeOfNeg = 0, newFirstLastDates = [], newAllLists = [], newAbsFirstLastDates = ''):
        self.listOfReturn = newListOfReturn
        self.timeFrame = newTimeFrame # [year, months (30 days)]
        self.beta = newBeta
        self.standardDeviation = newStandardDeviation
        self.negativeStandardDeviation = newNegativeStandardDeviation
        self.marketReturn = newMarketReturn
        self.size = newSize
        self.sizeOfNeg = newSizeOfNeg
        self.firstLastDates = newFirstLastDates

    def getFirstLastDates(self, stock):
        firstLastDates = []
        timeFrame = self.timeFrame
        firstDate = datetime.datetime.now() - datetime.timedelta(days=timeFrame[0]*365)
        firstDate = firstDate - datetime.timedelta(days=timeFrame[1]*30)
        firstDate = ''.join((str(firstDate.year),'-', str(firstDate.month), '-', str(firstDate.day)))

        lastDate = StockData.returnAbsFirstLastDates(stock)[1]
        #print(lastDate)
        firstLastDates.append(firstDate)
        firstLastDates.append(lastDate)
        return firstLastDates

    def getUnadjustedReturn(self, stock):
        finalDatesAndClose = StockData.returnFinalDatesAndClose(stock)
        finalDatesAndClose2 = StockData.returnFinalDatesAndClose2(stock)
        firstDate = self.firstLastDates[0]
        lastDate = self.firstLastDates[1]
        finalDates = finalDatesAndClose[0]
        finalClose = finalDatesAndClose[1]

        firstClose = 0
        for i in range(0, len(finalDates), 1):
            if finalDates[i] == firstDate:
                firstClose = finalClose[i]
            elif finalDates[i] == lastDate:
                lastClose = finalClose[i]
                i = len(finalDates)

        if firstClose == 0:
            print("Could not find first date. Changing first date to closest date")
            temp = Functions.stringToDate(firstDate) # Change to datetime
            print('Original first date: ', temp)
            newFirstDate = Functions.getNearest(finalDatesAndClose2[0], temp)
            print('New first date: ', newFirstDate)

            for i in range(0, len(finalDates), 1):
                if finalDates[i] == str(newFirstDate):
                    firstClose = finalClose[i]

        print(firstClose)
        print(lastClose)

#    def getBeta(self, timeFrame):

#    def getStandardDeviation(self, timeFrame):

    def main(self, stock):
        # Find date to start from and last date
        self.timeFrame = []
        print("\nPlease enter a time frame in years: ", end='')
        #timeFrameYear = int(input())
        timeFrameYear = 5
        self.timeFrame.append(timeFrameYear)
        print("Please enter a time frame in months (30 days): ", end='')
        #timeFrameMonth = int(input())
        timeFrameMonth = 0
        print('')
        self.timeFrame.append(timeFrameMonth)
        #print(self.timeFrame)
        self.firstLastDates = Return.getFirstLastDates(self, stock)
        print('Dates: ', self.firstLastDates)

        print('\nGetting unadjusted return')
        Return.getUnadjustedReturn(self, stock)

def main():
    stockName = 'spy'
    stock1 = StockData(stockName)
    print("Finding available dates and close values for", stock1.name)
    StockData.main(stock1)

    stock1Return = Return()
    Return.main(stock1Return, stock1)

if __name__ == "__main__":
  	main()
