# main.py
# Andrew Dinh
# Python 3.6.1
# Description: Get, parse, and interpret JSON files from IEX
import urllib.request
import re
#import os, errno
import json

file_path = "tmp/data.txt"
# directory = os.path.dirname(file_path)

url = urllib.request.urlopen("https://api.iextrading.com/1.0/stock/aapl/chart")
#print("url =", url)
html = url.read() # this is not a string, must convert it for findall()
# print("the html =", html)

myFile = open('data.json','r')
data = myFile.read()

json_string = json.dumps(data)
print("json string:", data)

'''
myFile =open(file_path,'w')
myFile.write(str(html))
myFile.close()


# Create tmp folder
try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

myFile = open(file_path,'r')
listOfLines = myFile.read().split('}')
#print("fileAsList:\n",listOfLines)

print(listOfLines[0],"\n")
print(listOfLines[1])
'''
'''
for j in range(0,len(listOfLines),1):
  aLine = listOfLines[j]
  #print(aLine)
  lineData = aLine.split()
  #print(lineData)
'''

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
