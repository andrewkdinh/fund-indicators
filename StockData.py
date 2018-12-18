# StockData.py
# Andrew Dinh
# Python 3.6.1
# Description: 
'''
Returns all available dates and prices for each stock requested.
'''

# Alpha Vantage API Key: O42ICUV58EIZZQMU
# Barchart API Key: a17fab99a1c21cd6f847e2f82b592838
# Tiingo API Key: 2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8
# If you're going to take these API keys and abuse it, you should really reconsider your life priorities

apiAV = 'O42ICUV58EIZZQMU'
apiBarchart = 'a17fab99a1c21cd6f847e2f82b592838'
apiTiingo = '2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8' # Limited to 400 requests/day

import requests, json
from datetime import datetime

class Stock:
  def __init__(self, newName = '', newfirstLastDates = [], newAbsFirstLastDates = [], newDates = [], newListIEX = [], newListAV = [], newListTiingo = []):
    self.name = newName                             # Name of stock
    self.firstLastDates = newfirstLastDates         # Dates that at least 2 sources have (or should it be all?) - Maybe let user decide
    self.absFirstLastDates = newAbsFirstLastDates   # Absolute first and last dates from all sources
    self.dates = newDates                           # All available dates
    '''
    Format: 
    # List from each source containing: [firstDate, lastDate, allDates, values, timeFrame]
    # firstDate & lastDate = '2018-12-18' (year-month-date)
    allDates = ['2018-12-17', '2018-12-14'] (year-month-date)
    values (close) = ['164.6307', 164.6307]
    timeFrame = [days, weeks, years]
    '''
    self.listIEX = newListIEX                     # Dates available from IEX
    self.listAV = newListAV                       # Dates available from AV
    self.listTiingo = newListTiingo               # Dates available from Tiingo

  def set(self, newName, newfirstLastDates, newAbsFirstLastDates, newDates, newListIEX, newListAV, newListTiingo):
    self.name = newName                             # Name of stock
    self.firstLastDates = newfirstLastDates         # Dates that at least 2 sources have (or should it be all?) - Maybe let user decide
    self.absFirstLastDates = newAbsFirstLastDates   # Absolute first and last dates from all sources
    self.dates = newDates                           # All available dates

    # List from each source containing: ['firstDate', 'lastDate', allDates, values]
    self.listIEX = newListIEX                     # Dates available from IEX
    self.listAV = newListAV                       # Dates available from AV
    self.listTiingo = newListTiingo               # Dates available from Tiingo

  def setFirstLastDates(newFirstLastDates):
    self.firstLastDates = newFirstLastDates
  def setAbsFirstLastDates(newAbsFirstLastDates):
    self.absFirstLastDates = newAbsFirstLastDates
  def setDates(newDates):
    self.dates = newDates
  def setListIEX(newListIEX):
    self.listIEX = newListIEX
  def setListAV(newListAV):
    self.listAV = newListAV
  def setListTiingo(newListTiingo):
    self.listTiingo = newListTiingo

  def getIEX(self):
    url = ''.join(('https://api.iextrading.com/1.0/stock/', self, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    print("\nSending request to:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    listIEX = []

    print("\nFinding first and last date")
    # Adding (firstDate, lastDate) to listIEX
    # Find firstDate (comes first)
    firstLine = loaded_json[0]
    #print("firstLine:", firstLine)
    firstDate = firstLine['date']
    #print("firstDate:",firstDate)
    # Find lastDate (comes last)
    #print("Length:", len(loaded_json))
    lastLine = loaded_json[-1] # Returns last value of the list (Equivalent to len(loaded_json)-1)
      #print("lastLine:", lastLine)
    lastDate = lastLine['date']
    #print("last date:", lastDate)
    listIEX.append(firstDate)
    listIEX.append(lastDate)
    print(listIEX[0], ',', listIEX[1])

    print("\nFinding all dates given")
    allDates = []
#   for i in range(0, len(loaded_json), 1): # If you want to do oldest first
    for i in range(len(loaded_json)-1, -1, -1):
      line = loaded_json[i]
      date = line['date']
      allDates.append(date)
    listIEX.append(allDates)
    #print(listIEX[1])
    print("Uncomment above line in code to see output")

    print("\nFinding close values for each date")
    values = []
#   for i in range(0, len(loaded_json), 1): # If you want to do oldest first
    for i in range(len(loaded_json)-1, -1, -1):
      line = loaded_json[i]
      value = line['close']
      values.append(value)
    listIEX.append(values)
    #print(listIEX[3])
    print("Uncomment above line in code to see output")

    print("\nFinding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listIEX.append(timeFrame)
    print(listIEX[4])

    return listIEX

  def getAV(self):
    listAV = []
    url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=', self, '&apikey=', apiAV))
    # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=MSFT&apikey=demo
    print("\nSending request to:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    #print(loaded_json['Monthly Time Series'])
    monthlyTimeSeries = loaded_json['Monthly Time Series']
    #print(monthlyTimeSeries)
    listOfDates = list(monthlyTimeSeries)
    #print(listOfDates)

    firstDate = listOfDates[-1]
    lastDate = listOfDates[0]
    #print("firstDate:", firstDate)
    #print("lastDate:", lastDate)
    listAV.append(firstDate)
    listAV.append(lastDate)
    listAV.append(listOfDates)

    print("\nFinding first and last date")
    print(listAV[0], ',', listAV[1])
    print("\nFinding all dates given")
    #print(listAV[2])
    print("Uncomment above line in code to see output")

    print("\nFinding close values for each date")
    values = []
    for i in range(0, len(listOfDates), 1):
      temp = listOfDates[i]
      loaded_json2 = monthlyTimeSeries[temp]
      value = loaded_json2['4. close']
      values.append(value)
    listAV.append(values)
    #print(listOfDates[0])
    #i = listOfDates[0]
    #print(monthlyTimeSeries[i])
    #print(listAV[3])
    print("Uncomment above line in code to see output")

    print("\nFinding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listAV.append(timeFrame)
    print(listAV[4])

    return listAV

  def getTiingo(self):
    '''
    #OR we can use the token directly in the url
    headers = {
       'Content-Type': 'application/json'
       }
    requestResponse = requests.get("https://api.tiingo.com/api/test?token=<TOKEN>",
                                  headers=headers)
    print(requestResponse.json())
    '''
    token = ''.join(('Token ', apiTiingo))
    headers = {
      'Content-Type': 'application/json',
      'Authorization' : token
       }
    url = ''.join(('https://api.tiingo.com/tiingo/daily/', self))
    print("\nSending request to:", url)
    requestResponse = requests.get(url, headers=headers)
    #print(requestResponse.json())
    loaded_json = requestResponse.json()
    #print(loaded_json)
    #print(len(loaded_json))
    '''
    list1 = list(loaded_json)
    for i in range (0, len(list1), 1):
      if list1[i] == 'startDate':
        startNum = i
      elif list1[i] == 'endDate':
        endNum = i
    print(list1[startNum])
    print(list1[endNum])
    '''
    listTiingo = []

    print("\nFinding first and last date")
    firstDate = loaded_json['startDate']
    lastDate = loaded_json['endDate']
    #print(firstDate)
    #print(lastDate)
    listTiingo.append(firstDate)
    listTiingo.append(lastDate)
    print(listTiingo[0], ',', listTiingo[1])

    print("\nFinding all dates given")
    dates = []
    values = [] # Used loop for finding values
    url2 = ''.join((url, '/prices?startDate=', firstDate, '&endDate=', lastDate))
    # https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1
    print("\nSending request to:", url2)
    requestResponse2 = requests.get(url2, headers=headers)
    loaded_json2 = requestResponse2.json()
    #print(loaded_json2)
    #print(len(loaded_json2))
    for i in range(len(loaded_json2)-1, -1, -1):
      line = loaded_json2[i]
      dateWithTime = line['date']
      temp = dateWithTime.split('T00:00:00.000Z')
      date = temp[0]
      dates.append(date)

      value = line['close']
      values.append(value)
    listTiingo.append(dates)
    #print(listTiingo[2])
    print("Uncomment above line in code to see output")

    print("Finding close values for each date")
    # Used loop from finding dates
    listTiingo.append(values)
    #print(listTiingo[3])
    print("Uncomment above line in code to see output")

    print("Finding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listTiingo.append(timeFrame)
    print(listTiingo[4])

    return listTiingo

  def getFirstLastDate(self, listOfFirstLastDates):
    listOfFirstDates = []
    listOfLastDates = []
    #print(len(listOfFirstLastDates))
    for i in range (0, len(listOfFirstLastDates), 1):
      firstLastDates = listOfFirstLastDates[i]
      firstDate = firstLastDates[0]
      lastDate = firstLastDates[1]
      listOfFirstDates.append(firstDate)
      listOfLastDates.append(lastDate)
    #print(listOfFirstDates)
    #print(listOfLastDates)
    for i in range (0, len(listOfFirstDates), 1):
      date = listOfFirstDates[i]
      if i == 0:
        firstDate = date
        yearMonthDate = firstDate.split('-')
        firstYear = yearMonthDate[0]
        firstMonth = yearMonthDate[1]
        firstDay = yearMonthDate[2]
      else:
        yearMonthDate = date.split('-')
        year = yearMonthDate[0]
        month = yearMonthDate[1]
        day = yearMonthDate[2]
        if year < firstYear or (year == firstYear and month < firstMonth) or (year == firstYear and month == firstMonth and day < firstDay):
          firstDate = date
          firstYear = year
          firstMonth = month
          firstDay = day
    #print(firstDate)
    for i in range(0, len(listOfLastDates),1):
      date = listOfLastDates[i]
      if i == 0:
        lastDate = date
        yearMonthDate = lastDate.split('-')
        lastYear = yearMonthDate[0]
        lastMonth = yearMonthDate[1]
        lastDay = yearMonthDate[2]
      else:
        yearMonthDate = date.split('-')
        year = yearMonthDate[0]
        month = yearMonthDate[1]
        day = yearMonthDate[2]
      if year > lastYear or (year == lastYear and month > lastMonth) or (year == lastYear and month == lastMonth and day > lastDay):
        lastDate = date
        lastYear = year
        lastMonth = month
        lastDay = day
    #print(lastDate)
    absFirstLastDates = []
    absFirstLastDates.append(firstDate)
    absFirstLastDates.append(lastDate)
    return absFirstLastDates

  def main(self):
    # Makes list with ['firstDate', 'lastDate', [allDates], values]

    listOfFirstLastDates = []

    # IEX
    print("\nIEX")
    listIEX = Stock.getIEX(self)
    #print(listIEX)
    listOfFirstLastDates.append((listIEX[0], listIEX[1]))

    # Alpha Vantage
    print("\nAlpha Vantage (AV)")
    listAV = Stock.getAV(self)
    #print(listAV)
    listOfFirstLastDates.append((listAV[0], listAV[1]))

    print("\nTiingo") # COMMENTED OUT FOR NOW B/C LIMITED TO 400 REQUESTS/DAY
    #listTiingo = Stock.getTiingo(self)
    #print(listTiingo)
    #listOfFirstLastDates.append((listTiingo[0], listTiingo[1]))

    #print(listOfFirstLastDates)
    absFirstLastDates = Stock.getFirstLastDate(self, listOfFirstLastDates)
    print("\nThe absolute first date was:", absFirstLastDates[0])
    print("The absolute last date was:", absFirstLastDates[1])

    '''
    FIGURE OUT HOW TO MAKE EACH OF THESE LISTS AN ATTRIBUTE OF CLASS STOCK
    self.listIEX = listIEX
    self.listAV = listAV
    self.listTiingo = listTiingo

    self.absFirstLastDates = absFirstLastDates
    '''

def main():
  stock = 'spy'
  spy = Stock(stock)
  Stock.main(stock)
  #Stock.printDates(spy)

if __name__ == "__main__":
  main()
