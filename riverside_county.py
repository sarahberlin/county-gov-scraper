import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.countyofriverside.us/AbouttheCounty/SupervisorsandElectedOfficials.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error.
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#checks for error in root_url and formats table into BOS for supervisors and other_officials for non-supervisors


if checkURL(root_url) == 404:
    print '404 error. Check the url for {0}'.format(root_url)
else:
    soup = bs4.BeautifulSoup((requests.get(root_url)).text)
    info = soup.find_all('div', {'id':'dnn_ctr574_ContentPane'})[0]
    sections = info.find_all('p')
    BOS = sections[1]
    other_officials = sections[2]

#scrapes pages of county supervisors
def get_supervisors_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        for a in BOS.select('a'):
            newDict = {}
            newDict['official.name'] = a.get_text().encode('utf-8').split(' - ')[1]
            newDict['office.name']= "Supervisor " + a.get_text().encode('utf-8').split(' - ')[0]
            newDict['electoral.district'] = "Riverside County Council " + a.get_text().encode('utf-8').split(' - ')[0][-1]
            newDict['address'] = '4080 Lemon Street, 5th Floor Riverside, California 92501'
            newDict['website'] = [a.attrs.get('href')][0]
            newDict['phone'] = '(951) 955-10{0}0'.format(a.get_text().encode('utf-8').split(' - ')[0][-1])
            newDict['email'] = 'district{0}@rcbos.org'.format(a.get_text().encode('utf-8').split(' - ')[0][-1])
            dictList.append(newDict)
    return dictList

get_supervisors_data()

#scrapes pages of other elected officials
def get_govt_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        for a in other_officials.select('a'):
            try:
                newDict = {}
                newDict['official.name'] = a.get_text().encode('utf-8').split(' - ')[1]
                newDict['office.name']= a.get_text().encode('utf-8').split(' - ')[0]
                newDict['website'] = [a.attrs.get('href')][0]
                newDict['electoral.district'] = 'Riverside County'
                dictList.append(newDict)
            except:
                pass
    return dictList

get_govt_data()

for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
riverside_county_board_file = open('riverside_county_board.csv','wb')
csvwriter = csv.DictWriter(riverside_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

riverside_county_board_file.close()
 
with open("riverside_county_board.csv", "r") as riverside_county_board_csv:
     riverside_county_board = riverside_county_board_csv.read()

#print riverside_county_board
