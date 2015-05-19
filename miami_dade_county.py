import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://miamidade.gov/wps/portal/Main/government'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#scrapes non-commissioners
def get_govt_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(0,3):
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
    return dictList

get_govt_data()

#scrapes commissioners
def get_councilor_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(0,13):
            newDict = {}
            newDict['official.name'] = soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].replace('Chairman\r\n', '').split('\r\n')[1].replace('\nWebsite |', '').replace('\n Website |', '').replace('\xc3\xa9','e').replace("Vice Chair", "").strip()
            newDict['office.name'] = "County Commissioner " + soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[0].replace('\nWebsite |', '').strip()
            newDict['electoral.district'] = "Miami-Dade County Council " + soup.findAll('div', {'id':'electedCommission'})[0].get_text().encode('utf-8').split('Contact')[x].split('\r\n')[0].replace('\nWebsite |', '').strip()
            newDict['website'] = [a.attrs.get('href') for a in soup.select('div span a[href^=http://www.miamidade.gov/district]')][x]
            newDict['address'] = '111 NW 1st Street, Suite 220 Miami, Florida 33128'
            contact_page = [a.attrs.get('href') for a in soup.select('div span a[href^=http://www.miamidade.gov/district]')][x+14+x]
            if checkURL(contact_page) == 404:
                print '404 error. Check the url for {0}'.format(contact_page)
            else:
                contact_soup = bs4.BeautifulSoup((requests.get(contact_page)).text)
                newDict['phone'] = contact_soup.find_all('div', {'class': 'rightContent'})[0].get_text().encode('utf-8').split("Office")[1].split('Phone')[0].strip()
            try:
                newDict['email'] = [a.attrs.get('href') for a in contact_soup.select(' a[href*@]')][0].replace('mailto:','')
            except:
                pass
            dictList.append(newDict)
    return dictList

get_councilor_data()

for dictionary in dictList:
    dictionary['state'] = 'FL'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
miami_dade_county_board_file = open('miami_dade_county_board.csv','wb')
csvwriter = csv.DictWriter(miami_dade_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

miami_dade_county_board_file.close()
 
with open("miami_dade_county_board.csv", "r") as miami_dade_county_board_csv:
     miami_dade_county_board = miami_dade_county_board_csv.read()

#print miami_dade_county_board
