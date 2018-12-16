# main.py
# Andrew Dinh
# Python 3.6.1
# Description: Get, parse, and interpret JSON files from IEX
import urllib.request
import re
import os

url = urllib.request.urlopen("https://api.iextrading.com/1.0/stock/aapl/chart")
print("url =", url)
html = url.read() # this is not a string, must convert it for findall()
# print("-----------------------------------------------")
# print("the html =", html)

if not os.path.exists(temporary):
    os.makedirs(temporary)

myFile = open('temporary/data.txt','r')
listOfLines = myFile.readlines()
print("fileAsList:\n",listOfLines)


'''
url = urllib.request.urlopen("http://www.gavilan.edu/staff/dir.php")
print("url =", url)
html = url.read() # this is not a string, must convert it for findall()
# print("-----------------------------------------------")
# print("the html =", html)

myFile = open('dataFile.txt','w')
myFile.write(str(html))
myFile.close()

myFile = open('dataFile.txt','r')
listOfLines = myFile.readlines() # returns a list of lines,USE for search()
#print("fileAsList:\n",listOfLines)
listOfEmails = re.findall(r'\w+@gavilan.edu', str(html))
# print(listOfEmails)
myFile.close()

myFile = open('dataFile.txt','r')
listOfLines = myFile.readlines()
for line in listOfLines:
  match = re.search('stoykov',str(line))
  if match:
    print(line)
myFile.close()
'''