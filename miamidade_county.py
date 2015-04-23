import requests
import bs4
import csv
from csv import DictWriter

dictList = []

## noncommissioners
def get_govt_data():
    for x in range(0,3):
        root_url = 'http://miamidade.gov/wps/portal/Main/government'
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        newDict = {}
        newDict['official.name'] = soup.findAll('div', {'id':'electedNonCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[1].replace('\nWebsite |', '').strip()
        newDict['office.name'] = soup.findAll('div', {'id':'electedNonCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[0].replace('\nWebsite |', '').strip().replace('Office of the ', '')
        newDict['electoral.district'] = 'Miami-Dade County'
        if newDict['office.name'] == "Mayor":
            newDict['website'] = 'http://www.miamidade.gov/mayor/'
        elif newDict['office.name'] == "Clerk, Circuit and County Courts":
            newDict['website'] = 'http://www.miami-dadeclerk.com/'
        elif newDict['office.name'] == "Property Appraiser": 
            newDict['website'] = 'http://www.miamidade.gov/pa/'
        dictList.append(newDict)
    print dictList

get_govt_data()

## commissioners
def get_councilor_data():
    root_url = 'http://miamidade.gov/wps/portal/Main/government'
    soup = bs4.BeautifulSoup((requests.get(root_url)).text)
    for x in range(0,13):
        newDict = {}
        newDict['official.name'] = soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].replace('Chairman\r\n', '').split('\r\n')[1].replace('\nWebsite |', '').replace('\n Website |', '').replace('\xc3\xa9','e').replace("Vice Chair", "").strip()
        newDict['office.name'] = "County Commissioner " + soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[0].replace('\nWebsite |', '').strip()
        newDict['electoral.district'] = "County Council " + soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[0].replace('\nWebsite |', '').strip()
        newDict['website'] = [a.attrs.get('href') for a in soup.select('div span a[href^=http://www.miamidade.gov/district]')][x]
        newDict['address'] = '111 NW 1st Street, Suite 220 Miami, Florida 33128'
        contact_page = [a.attrs.get('href') for a in soup.select('div span a[href^=http://www.miamidade.gov/district]')][x+14+x]
        contact_soup = bs4.BeautifulSoup((requests.get(contact_page)).text)
        newDict['phone'] = contact_soup.find_all('div', {'class': 'rightContent'})[0].get_text().encode('utf-8').split("Office")[1].split('Phone')[0].strip()
        try:
            newDict['email'] = [a.attrs.get('href') for a in contact_soup.select(' a[href*@]')][0].replace('mailto:','')
        except:
            pass
        dictList.append(newDict)
    print dictList

get_councilor_data()



#creates csv
fieldnames = ['official.name','electoral.district', 'office.name','phone','website', 'address', 'email']
miami_county_board_file = open('miami_county_board.csv','wb')
csvwriter = csv.DictWriter(miami_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

miami_county_board_file.close()
 
with open("miami_county_board.csv", "r") as miami_county_board_csv:
     miami_county_board = miami_county_board_csv.read()

print miami_county_board
