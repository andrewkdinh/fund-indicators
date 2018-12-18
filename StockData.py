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
'''
def install(package):
  if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
'''
class Stock:
  def __init__(self, newStock = '', newfirstLastDates = [], newDates = []):
    self.name = newStock
    self.firstLastDates = newfirstLastDates
    self.dates = newDates

  def getDates(self): # returns beginning and end dates available
    print("Getting available dates for", self, "...")
    # Gets first and last possible dates from each source
    # Also gets all dates from each source
    
    # IEX
    print("\nDates from IEX...")
    firstLastDatesIEX = Stock.getDatesIEX(self, 'firstLast')
    print("First and last dates:", firstLastDatesIEX)
    print("Adding dates available to datesIEX")
    datesIEX = Stock.getDatesIEX(self, 'all')
    #print("All dates (recent first):", datesIEX, "\n") # Uncomment line to view output

    # Alpha Vantage
    print("\nDates from Alpha Vantage...")
    firstLastDatesAV = Stock.getDatesAV(self, 'firstLast')
    print("First and last dates:", firstLastDatesAV)
    print("Adding dates available to datesAV")
    datesAV = Stock.getDatesAV(self, 'all')
    #print("All dates (recent first):", datesAV, "\n") # Uncomment line to view output
    
    # Tiingo
    print("\nDates from Tiingo...")
    firstLastDatesTiingo = Stock.getDatesTiingo(self, 'firstLast')
    print("First and last dates:", firstLastDatesTiingo)
    print("Adding dates available to datesTiingo")
    datesTiingo = Stock.getDatesTiingo(self, 'all')
    #print("All dates (recent first):", datesTiingo, "\n") # Uncomment line to view output

  def getDatesIEX(self, which):
    url = ''.join(('https://api.iextrading.com/1.0/stock/', self, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    #print("URL:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    dates = []
    if which == 'firstLast':
      # Find firstDate (comes first)
      firstLine = loaded_json[0]
      #print("firstLine:", firstLine)
      firstDate = firstLine['date']
      #print("firstDate:",firstDate)
      # Find finalDate (comes last)
      #print("Length:", len(loaded_json))
      lastLine = loaded_json[-1] # Returns last value of the list (Equivalent to len(loaded_json)-1)
      #print("lastLine:", lastLine)
      finalDate = lastLine['date']
      #print("Final date:", finalDate)
      dates.append((firstDate, finalDate))
    elif which == 'all':
#       for i in range(0, len(loaded_json), 1): # If you want to do oldest first
        for i in range(len(loaded_json)-1, 0, -1):
          line = loaded_json[i]
          date = line['date']
          dates.append(date)
    return dates

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
    finalDate = loaded_json['endDate']
    #print(firstDate)
    #print(finalDate)
    dates = []
    if which == 'firstLast':
      #print("URL:", url)
      dates.append((firstDate, finalDate))
    elif which == 'all':
      url2 = ''.join((url, '/prices?startDate=', firstDate, '&endDate=', finalDate))
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

def main():
  #if __name__ == '__main__':
        #  install('requests')

  stock = 'spy'
  spy = Stock(stock)
  #print(spy.name)
  Stock.getDates(stock)
  #Stock.printDates(spy)

main()
