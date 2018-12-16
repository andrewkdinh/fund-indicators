# main.py
# Andrew Dinh
# Python 3.6.1
# Description: Get, parse, and interpret JSON files from IEX
import urllib, requests, json

class iex:

  def __init__(self, newStock = 'spy')
  self.iex

  def printDates(self)
    print("Getting data from IEX...")
    url = ''.join(('https://api.iextrading.com/1.0/stock/', stock, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    print("URL:", url)
    f = requests.get(url)
    #print(f.text)
    json_data = f.text
    loaded_json = json.loads(json_data)
    #print(json_data)
    #print(loaded_json)
    #print(loaded_json[0])

    print("Printing dates given from IEX...")
    for i in range (0,len(loaded_json),1):
      a = loaded_json[i]
      print(a['date'])

def main():
  stock = 'spy'
  IEX(stock)

main()