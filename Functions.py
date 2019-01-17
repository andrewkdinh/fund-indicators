# Python file for general functions
class Functions:
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

def main():
    exit()

if __name__ == "__main__":
  	main()
