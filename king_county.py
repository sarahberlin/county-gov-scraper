import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.kingcounty.gov/elected.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code


def get_council_data():
	if checkURL(root_url) == 404:
		print '404 error. Check the url for {0}'.format(root_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(root_url)).text)
		for x in range(0,9):
			newDict = {}
			newDict['official.name'] = soup.select('div.col-xs-6  ul.list-unstyled li a')[x].get_text().encode('utf-8').split(' \xc2\xb7 ')[0]
			newDict['office.name'] = "County Councilmember " + soup.select('span.hidden-xs')[x+1].get_text().encode('utf-8').strip()
			newDict['electoral.district'] = 'King County Council ' + soup.select('span.hidden-xs')[x+1].get_text().encode('utf-8').strip()
			newDict['website'] = 'http://www.kingcounty.gov'+[a.attrs.get('href') for a in soup.select('ul.list-unstyled li a[href^=/council/]')][x]
			newDict['phone'] = '206-477-100' + soup.select('span.hidden-xs')[x+1].get_text().encode('utf-8').strip()[-1]
			newDict['address'] = '516 Third Ave., Rm. 1200 Seattle, WA 98104'
			email_page = 'http://www.kingcounty.gov/council/councilmembers.aspx'
			if checkURL(email_page) == 404:
				print '404 error. Check the url for {0}'.format(email_page)
				dictList.append(newDict)
			else:
				email_soup = bs4.BeautifulSoup((requests.get(email_page)).text)
				newDict['email'] = [a.attrs.get('href') for a in email_soup.select('a[href^=mailto:]')][x].replace('mailto:','')
				dictList.append(newDict)
		newDict = {}
		newDict['official.name'] = soup.select('p a ')[0].get_text().encode('utf-8').replace('King County Executive ', '')
		newDict['office.name'] = soup.select('p a span.hidden-xs')[0].get_text().encode('utf-8')
		newDict['electoral.district'] = "King County"
		newDict['website'] = [a.attrs.get('href') for a in soup.select('p a[href^=/elected/executive]')]

	return dictList

get_council_data()


def get_govt_data():
	if checkURL(root_url) == 404:
		print '404 error. Check the url for {0}'.format(root_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(root_url)).text)
		for x in range(0,4):
			newDict = {}
			newDict['office.name'] = soup.select('div.floating-content-box')[x].get_text().encode('utf-8').split('\n')[1]
			newDict['official.name'] = soup.select('div.floating-content-box')[x].get_text().encode('utf-8').split('\n')[2]
			newDict['electoral.district'] = "King County"
			newDict['website'] = 'http://www.kingcounty.gov' + [a.attrs.get('href') for a in soup.select('div.floating-content-box a[href]')][x*4]
			dictList.append(newDict)
	return dictList

get_govt_data()


for dictionary in dictList:
    dictionary['state'] = 'WA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
king_county_board_file = open('king_county_board.csv','wb')
csvwriter = csv.DictWriter(king_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

king_county_board_file.close()
 
with open("king_county_board.csv", "r") as king_county_board_csv:
     king_county_board = king_county_board_csv.read()

#print king_county_board
