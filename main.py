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

# Alpha Vantage API Key: O42ICUV58EIZZQMU
# Barchart API Key: a17fab99a1c21cd6f847e2f82b592838
# Tiingo API Key: 2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8
# If you're going to take these API keys and abuse it, you should really reconsider your life priorities

import requests, json

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

class Stock:
  def __init__(self, newStock = ''):
    self.name = newStock

  def getDates(self): # returns beginning and end dates available
    print("Getting dates from sources...")
    # Gets first and last possible dates from each source
    # IEX
    print("Getting dates from IEX")
    datesIEX = Stock.getDatesIEX(self)
    print(datesIEX)
  '''
    print("Getting dates from Alpha Vantage")
    datesAV = Stock.getDatesAV(self)
    print(datesAV)
  '''
    
  def getDatesIEX(self):
    dates = []
    url = ''.join(('https://api.iextrading.com/1.0/stock/', self, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    print("URL:", url)
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    # Find firstDate (comes first)
    firstLine = loaded_json[0]
    print("firstLine:", firstLine)
    firstDate = firstLine['date']
    print("firstDate:",firstDate)
    # Find finalDate (comes last)
    print("Length:", len(loaded_json))
    lastLine = loaded_json[-1] # Returns last value of the list (Equivalent to len(loaded_json)-1)
    print("lastLine:", lastLine)
    finalDate = lastLine['date']
    print("Final date:", finalDate)
    dates = []
    dates.append((firstDate, finalDate))
    return dates

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
  #  install('oauth2client')

  stock = 'spy'
  spy = Stock(stock)
  #print(spy.name)
  Stock.getDates(stock)
  #Stock.printDates(spy)

main()
