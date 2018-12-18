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
apiTiingo = '2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8'

import requests, json

class Stock:
  def __init__(self, newName = '', newfirstLastDates = [], newAbsFirstLastDates = [], newDates = [], newListIEX = [], newListAV = [], newListTiingo = []):
    self.name = newName                             # Name of stock
    self.firstLastDates = newfirstLastDates         # Dates that at least 2 sources have (or should it be all?) - Maybe let user decide
    self.absFirstLastDates = newAbsFirstLastDates   # Absolute first and last dates from all sources
    self.dates = newDates                           # All available dates

    # List from each source containing: ['firstDate', 'lastDate', allDates, values]
    self.listIEX = newListIEX                     # Dates available from IEX
    self.listAV = newListAV                       # Dates available from AV
    self.listTiingo = newListTiingo               # Dates available from Tiingo

  def main(self):
    # Makes list with [firstDate, lastDate, allDates, values]

    # IEX
    print("\nIEX")
    listIEX = Stock.getIEX(self)

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
    #print("URL:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    listIEX = []

    # Adding (firstDate, lastDate) to list
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

    allDates = []
#   for i in range(0, len(loaded_json), 1): # If you want to do oldest first
    for i in range(len(loaded_json)-1, 0, -1):
      line = loaded_json[i]
      date = line['date']
      allDates.append(date)
    listIEX.append(allDates)
    #print(listIEX)
    return listIEX

  def getDatesAV(self, which):
    url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=', self, '&apikey=', apiAV))
    # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=MSFT&apikey=demo
    #print("URL:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    #print(loaded_json['Monthly Time Series'])
    monthlyTimeSeries = loaded_json['Monthly Time Series']
    #print(monthlyTimeSeries)
    #print(len(monthlyTimeSeries))
    #length = len(monthlyTimeSeries)
    #print(monthlyTimeSeries['2018-12-17'])
    #print(type(monthlyTimeSeries))
    listOfDates = list(monthlyTimeSeries)
    #print(listOfDates)
    dates = []
    if which == 'firstLast':
       firstDate = listOfDates[-1]
       lastDate = listOfDates[0]
       #print("firstDate:", firstDate)
       #print("lastDate:", lastDate)
       dates.append((firstDate, lastDate))
    elif which == 'all':
      dates = listOfDates
    return dates

  def getDatesTiingo(self, which):
    '''
    headers = {
       'Content-Type': 'application/json',
       'Authorization' : 'Token <TOKEN>'
       }
    requestResponse = requests.get("https://api.tiingo.com/api/test/",
                                  headers=headers)
    print(requestResponse.json())

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
    firstDate = loaded_json['startDate']
    lastDate = loaded_json['endDate']
    #print(firstDate)
    #print(lastDate)
    dates = []
    if which == 'firstLast':
      #print("URL:", url)
      dates.append((firstDate, lastDate))
    elif which == 'all':
      url2 = ''.join((url, '/prices?startDate=', firstDate, '&endDate=', lastDate))
      # https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1
      #print("Second URL:", url2)
      requestResponse2 = requests.get(url2, headers=headers)
      loaded_json2 = requestResponse2.json()
      #print(loaded_json2)
      #print(len(loaded_json2))
      '''
      print(loaded_json2[0])
      temp = loaded_json2[0]
      temp2 = temp['date']
      temp3 = temp2.split('T00:00:00.000Z')
      print(temp2)
      print(temp3)
      print(temp3[0])
      print(temp3[1])
      '''
      for i in range(len(loaded_json2)-1, 0, -1):
        line = loaded_json2[i]
        dateWithTime = line['date']
        temp = dateWithTime.split('T00:00:00.000Z')
        date = temp[0]
        dates.append(date)
    return dates

  def getFirstLastDate(self, listOfFirstLastDates):
    listOfFirstDates = []
    listOfLastDates = []
    #print(len(listOfFirstLastDates))
    for i in range (0, len(listOfFirstLastDates), 1):
      temp = listOfFirstLastDates[i]
      datesTemp = temp[0]
      #print(datesTemp)
      firstDate = datesTemp[0]
      #print(firstDate)
      lastDate = datesTemp[1]
      #print(lastDate)
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
    firstLastDates = []
    firstLastDates.append((firstDate, lastDate))
    return firstLastDates

def main():
  stock = 'spy'
  spy = Stock(stock)

  Stock.set('spy', 2,2,2,2,2,2,2)

  Stock.main(stock)
  #Stock.printDates(spy)

if __name__ == "__main__":
  main()
