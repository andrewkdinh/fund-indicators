# Python file for general functions
def getNearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def stringToDate(date):
    from datetime import datetime

    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
    return(datetime_object)
    '''
    dateSplit = date.split('-')
    year = int(dateSplit[0])
    month = int(dateSplit[1])
    day = int(dateSplit[2])
    datetime_object = datetime.date(year, month, day)
    '''
    return datetime_object

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


def main():
    exit()


if __name__ == "__main__":
    main()
