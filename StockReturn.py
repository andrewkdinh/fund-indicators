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

    def getFirstLastDates2(self, stock):
        finalDatesAndClose = StockData.returnFinalDatesAndClose(stock)
        finalDatesAndClose2 = StockData.returnFinalDatesAndClose2(stock)
        firstDate = self.firstLastDates[0]
        lastDate = self.firstLastDates[1]
        finalDates = finalDatesAndClose[0]

        firstDateExists = False
        lastDateExists = False
        for i in range(0, len(finalDates), 1):
            if finalDates[i] == str(firstDate):
                firstDateExists = True
            elif finalDates[i] == lastDate:
                lastDateExists = True
                i = len(finalDates)

        if firstDateExists == False:
            print("Could not find first date. Changing first date to closest date")
            tempDate = Functions.stringToDate(firstDate) # Change to datetime
            print('Original first date: ', tempDate)
            #tempDate = datetime.date(2014,1,17)
            newFirstDate = Functions.getNearest(finalDatesAndClose2[0], tempDate)
            print('New first date: ', newFirstDate)
            firstDate = str(newFirstDate)

        if lastDateExists == False:
            print("Could not find final date. Changing final date to closest date")
            tempDate2 = Functions.stringToDate(lastDate) # Change to datetime
            print('Original final date: ', tempDate2)
            #tempDate2 = datetime.date(2014,1,17)
            newLastDate = Functions.getNearest(finalDatesAndClose2[0], tempDate2)
            print('New final date: ', newLastDate)
            lastDate = str(newLastDate)

        firstLastDates = []
        firstLastDates.append(firstDate)
        firstLastDates.append(lastDate)
        return firstLastDates

    def getUnadjustedReturn(self, stock):
        finalDatesAndClose = StockData.returnFinalDatesAndClose(stock)
        finalDatesAndClose2 = StockData.returnFinalDatesAndClose2(stock)
        firstDate = self.firstLastDates[0]
        lastDate = self.firstLastDates[1]
        finalDates = finalDatesAndClose[0]

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

        print('\nMaking sure dates are within list...')
        self.firstLastDates = Return.getFirstLastDates2(self, stock)
        print('New dates: ', self.firstLastDates)

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
