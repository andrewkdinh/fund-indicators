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
      print("Getting available dates for", self, "...\n")
      # Gets first and last possible dates from each source
      # Also gets all dates from each source

      # IEX
      print("\nDates from IEX...")
      firstLastDatesIEX = Stock.getDatesIEX(self, 'firstLast')
      print("\nFirst and last dates:", firstLastDatesIEX)
      datesIEX = Stock.getDatesIEX(self, 'all')
      #print("All dates (recent first):", datesIEX, "\n")

      # Alpha Vantage
      print("\nDates from Alpha Vantage...")
      firstLastDatesAV = Stock.getDatesAV(self, 'firstLast')
      print("\nFirst and last dates:", firstLastDatesAV)
      datesAV = Stock.getDatesAV(self, 'all')
      #print("All dates (recent first):", datesAV, "\n")

      #
    
   def getDatesIEX(self, which):
      url = ''.join(('https://api.iextrading.com/1.0/stock/', self, '/chart/5y'))
      #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
      print("URL:", url)
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
      else:
#         for i in range(0, len(loaded_json), 1): # If you want to do oldest first
         for i in range(len(loaded_json)-1, 0, -1):
            line = loaded_json[i]
            date = line['date']
            dates.append(date)
      return dates

   def getDatesAV(self, which):
      url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=', self, '&apikey=', apiAV))
      # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=MSFT&apikey=demo
      print("URL:", url)
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
      else:
         dates = listOfDates
      return dates
'''
      # Find finalDate (comes first)
      print("Length:", len(loaded_json))
      lastLine = loaded_json[-1] # Returns last value of the list (Equivalent to len(loaded_json)-1)
      print("lastLine:", lastLine)
      finalDate = lastLine['date']
      print("Final date:", finalDate)
      dates = []
      dates.append((firstDate, finalDate))
'''
'''
  def printDates(self):
    print("Getting data from IEX...")
    url = ''.join(('https://api.iextrading.com/1.0/stock/', self.name, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    print("URL:", url)
    f = requests.get(url)
    #print(f.text)
    json_data = f.text
    loaded_json = json.loads(json_data)

    print("Printing from IEX...")
    for i in range (0,len(loaded_json),1):
      a = loaded_json[i]
      print(a['date'])
'''

def main():
   #if __name__ == '__main__':
        #  install('requests')

   stock = 'spy'
   spy = Stock(stock)
   #print(spy.name)
   Stock.getDates(stock)
   #Stock.printDates(spy)

main()
