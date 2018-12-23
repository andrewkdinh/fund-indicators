# https://support.google.com/docs/answer/3093281?hl=en
# Historical data cannot be downloaded or accessed via the Sheets API or Apps Script.  If you attempt to do so, you will see a #N/A error in place of the values in the corresponding cells of your spreadsheet.

import gspread, time, webbrowser, msvcrt
from oauth2client.service_account import ServiceAccountCredentials

def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    gc = gspread.authorize(credentials)
    '''
    # Just by ID:
    #sheet = gc.open_by_key('1YS8qBQCXKNfSgQgXeUdSGOd6lM2wm-inV0_1YE36vQM')
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1YS8qBQCXKNfSgQgXeUdSGOd6lM2wm-inV0_1YE36vQM')
    worksheet = sheet.get_worksheet(0)
    worksheet.update_acell('B1', 'bingo!')
    #worksheet.update_cell(1, 2, 'Bingo!')
    val = worksheet.acell('B1').value
    #val = worksheet.cell(1, 2).value
    print(val)
    '''
    url = 'https://docs.google.com/spreadsheets/d/1YS8qBQCXKNfSgQgXeUdSGOd6lM2wm-inV0_1YE36vQM'
    surl = 'https://www.andrewkdinh.com/u/listGoogle'
    print("Opening", url)
    #webbrowser.open(surl)
    sheet = gc.open_by_url(url)
    worksheet = sheet.get_worksheet(0)
    print('Writing Google Finance function to A1')
    worksheet.update_cell(1, 1, '=GOOGLEFINANCE("GOOG", "price", DATE(2014,1,1), DATE(2014,12,31), "DAILY")')
    print('\nOpening link to the Google Sheet. Please download the file as comma-separated values (.csv) and move it to the directory of this Python file', 
        '\nFile > Download as > Comma-separated values(.csv,currentsheet)')
    print("If the link did not open, please go to", surl)
    print("Press any key to continue")
    #time.sleep(45)
    '''
    for i in range(60, 0, -1):
        print(i, end='\r')
        time.sleep(1)
    '''
    waiting = True
    while waiting == True:
        if msvcrt.kbhit():
            waiting = False
            
    print("e")

    #val = worksheet.acell('A1').value
    #print(val)

if __name__ == '__main__':
    main()