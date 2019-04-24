'''
Copyright (C) 2019 Andrew Dinh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Python file for general functions

import sys
sys.path.insert(0, './modules')


def getNearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def stringToDate(date):
    from datetime import datetime

    # datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
    return(datetime_object)


def removeExtraDatesAndCloseValues(list1, list2):
    # Returns the two lists but with the extra dates and corresponding close values removed
    # list = [[dates], [close values]]

    newList1 = [[], []]
    newList2 = [[], []]

    for i in range(0, len(list1[0]), 1):
        for j in range(0, len(list2[0]), 1):
            if list1[0][i] == list2[0][j]:
                newList1[0].append(list1[0][i])
                newList2[0].append(list1[0][i])
                newList1[1].append(list1[1][i])
                newList2[1].append(list2[1][j])
                break

    returnList = []
    returnList.append(newList1)
    returnList.append(newList2)
    return returnList


def stringIsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def strintIsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def fromCache(r):
    import requests_cache
    from termcolor import colored, cprint
    if r.from_cache is True:
        cprint('(Response taken from cache)', 'white', attrs=['dark'])
    return


def getJoke():
    import requests
    from termcolor import colored, cprint
    import requests_cache
    from halo import Halo
    import sys
    with requests_cache.disabled():
        '''
        f = requests.get('https://official-joke-api.appspot.com/jokes/random').json()
        print('')
        print(f['setup'])
        print(f['punchline'], end='\n\n')
        '''
        headers = {'Accept': 'application/json',
                   'User-Agent': 'fund-indicators (https://github.com/andrewkdinh/fund-indicators)'}
        url = 'https://icanhazdadjoke.com'

        cprint('GET:' + url, 'white', attrs=['dark'])
        with Halo(spinner='dots'):
            f = requests.get(url,
                             headers=headers).json()
        print('')
        print(colored(f['joke'], 'green'))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def checkPackage(package):
    import importlib.util
    import sys
    spec = importlib.util.find_spec(package)
    if spec is None:
        return False
    else:
        return True


def checkPackages(listOfPackages):
    import importlib.util
    import sys

    packagesInstalled = True
    packages = listOfPackages
    for i in range(0, len(packages), 1):
        package_name = packages[i]
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(package_name, "is not installed\nPlease enter 'pip install -r requirements.txt' to install all required packages")
            packagesInstalled = False
    return packagesInstalled


def checkPythonVersion():
    import platform
    # print('Checking Python version')
    i = platform.python_version()
    r = i.split('.')
    k = float(''.join((r[0], '.', r[1])))
    if k < 3.3:
        print('Your Python version is', i,
              '\nIt needs to be greater than version 3.3')
        return False
    else:
        print('Your Python version of', i, 'is good')
        return True


def isConnected():
    import socket  # To check internet connection
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(('1.1.1.1', 53))
        print('Internet connection is good')
        return True
    except OSError:
        # pass
        print("No internet connection!")
    return False


def fileExists(file):
    import os.path
    return os.path.exists(file)


def listIndexExists(i):
    try:
        i
        return True
    except IndexError:
        return False


def removeOutliers(i):
    import statistics
    m = statistics.median(i)
    firstQ = []
    thirdQ = []
    for x in i:
        if x < m:
            firstQ.append(x)
        elif x > m:
            thirdQ.append(x)
    firstQm = statistics.median(firstQ)
    thirdQm = statistics.median(thirdQ)
    iqr = (thirdQm - firstQm) * 1.5

    goodList = []
    badList = []
    for x in i:
        if x < (thirdQm + iqr) and x > (firstQm - iqr):
            goodList.append(x)
        else:
            # In case I want to know. If not, then I just make it equal to returnlist[0]
            badList.append(x)
    returnList = [goodList, badList, firstQm, m, thirdQm, iqr]
    return returnList


def validateJson(text):
    import json
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def keyInDict(dict, key):
    if key in dict:
        return True
    else:
        return False


def getWeather():
    import requests
    from termcolor import colored, cprint
    import requests_cache
    from halo import Halo
    import sys
    sys.path.insert(0, './modules')
    with requests_cache.disabled():
        url = 'https://wttr.in?format=3'

        cprint('GET:' + url, 'white', attrs=['dark'])
        with Halo(spinner='dots'):
            f = requests.get(url)
        print('')
        print(colored('Current weather in ' + f.text, 'green'), end='')


def detectDisplay():
    import os
    try:
        t = os.environ["DISPLAY"]
    except KeyError:
        return False
    if t == ':0.0':
        return True
    else:
        return False


def trueOrFalse():
    found = False
    print('[1] Yes\n[2] No')
    while found is False:
        answer = str(input('Answer: '))
        if stringIsInt(answer) is True:
            temp = int(answer)
            if temp == 1:
                return True
            elif temp == 2:
                return False
            else:
                print('Please choose either 1 or 2')
                pass
        elif answer.lower() == 'yes':
            return True
        elif answer.lower() == 'no':
            return False
        else:
            print('Please choose a number or type an answer')


def main():
    exit()


if __name__ == "__main__":
    main()
