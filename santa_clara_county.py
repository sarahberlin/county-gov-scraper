import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.sccgov.org'
index_url = root_url + '/sites/scc/Pages/Elected-Officials.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code
#titles + names
def get_govt_data():
	if checkURL(index_url) == 404:
		print '404 error. Check the url for {0}'.format(index_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(index_url)).text)
		for x in range(0, len(soup.find_all('a', {'class': 'sccgov_electedofficials_portrait_title'}))):
			newDict = {}
			newDict['office.name'] = soup.find_all('a', {'class': 'sccgov_electedofficials_portrait_title'})[x].get_text().encode('utf-8')
			newDict['official.name'] = soup.find_all('div', {'class': 'sccgov_electedofficials_portrait_footer'})[x].get_text().encode('utf-8')
			newDict['website'] = index_url
			if 'Supervisor' in soup.find_all('a', {'class': 'sccgov_electedofficials_portrait_title'})[x].get_text().encode('utf-8'):
				newDict['office.name'] = "County Supervisor "+ soup.find_all('a', {'class': 'sccgov_electedofficials_portrait_title'})[x].get_text().encode('utf-8').split('Supervisor')[0].strip()
				newDict['address'] ='Tenth Floor - East Wing 70 West Hedding Street San Jose, CA 95110'
				newDict['phone'] ='408-299-5001'
				newDict['electoral.district'] = 'Santa Clara County Council District ' + soup.find_all('a', {'class': 'sccgov_electedofficials_portrait_title'})[x].get_text().encode('utf-8').split('Supervisor')[0].strip()[-1]
				dictList.append(newDict)
			else:
				newDict['electoral.district'] = 'Santa Clara County'
				dictList.append(newDict)
	return dictList

get_govt_data()

for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
santa_clara_county_board_file = open('santa_clara_county_board.csv','wb')
csvwriter = csv.DictWriter(santa_clara_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

santa_clara_county_board_file.close()
 
with open("santa_clara_county_board.csv", "r") as santa_clara_county_board_csv:
     santa_clara_county_board = santa_clara_county_board_csv.read()

#print santa_clara_county_board