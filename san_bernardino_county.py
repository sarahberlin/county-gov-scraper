import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#scrapes pages of commissioners
def get_council_data():
    root_url = 'http://www.sbcounty.gov/Main/bos.asp'
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(0,5):
            newDict = {}
            newDict['official.name'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').replace('                                                ', '').replace('Vice Chair', '').replace('Chair', '').replace('\r\n\n\r\n', '\r\n').split('\r\n')[0].replace('\n', '')
            newDict['office.name'] = "County Supervisor District " + soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').replace('                                                ', '').replace('Vice Chair', '').replace('Chair', '').replace('\r\n\n\r\n', '\r\n').split('\r\n')[1].replace('\n', '').replace('First', '1').replace('Second', '2').replace('Third', '3').replace('Fourth','4').replace('Fifth', '5')[0]
            newDict['electoral.district'] = 'San Bernardino County Council District ' + soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').replace('                                                ', '').replace('Vice Chair', '').replace('Chair', '').replace('\r\n\n\r\n', '\r\n').split('\r\n')[1].replace('\n', '').replace('First', '1').replace('Second', '2').replace('Third', '3').replace('Fourth','4').replace('Fifth', '5')[0]
            newDict['phone'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x+5].get_text().encode('utf-8').split('\r\n')[0]
            newDict['website'] = [a.attrs.get('href') for a in soup.select('span.boldtype a[href]')][x]
            newDict['address'] = '385 N. Arrowhead Avenue San Bernardino, CA 92415'
            dictList.append(newDict)
    return dictList

get_council_data()

#scrapes pages of other officials
def get_govt_data():
    root_url = 'http://www.sbcounty.gov/Main/electedofficials.asp'
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(5,10):
            newDict = {}
            newDict['official.name'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').split('\r\n')[0].replace('\n', '')
            newDict['electoral.district'] = 'San Bernardino County'
            if len(soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').split('\r\n')) == 3:
                newDict['office.name'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').split('\r\n')[1].replace('\n', '').replace('Recorder', 'Recorder/') + soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').split('\r\n')[2].replace('\n', '').replace('Recorder', 'Recorder/')
            else:
                newDict['office.name'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x].get_text().encode('utf-8').replace('                                                    ', '').split('\r\n')[1].replace('\n', '')
            newDict['phone'] = soup.find_all('td', {'style':'padding:10px;text-align:left;vertical-align:top;'})[x+5].get_text().encode('utf-8').split('\n')[0].replace('\xc2\xa0','')
            newDict['website'] = [a.attrs.get('href') for a in soup.select('span.boldtype a[href]')][x-5]
            dictList.append(newDict)
    return dictList

get_govt_data()

for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
san_bernardino_county_board_file = open('san_bernardino_county_board.csv','wb')
csvwriter = csv.DictWriter(san_bernardino_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

san_bernardino_county_board_file.close()
 
with open("san_bernardino_county_board.csv", "r") as san_bernardino_county_board_csv:
     san_bernardino_county_board = san_bernardino_county_board_csv.read()

#print san_bernardino_county_board
