import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://access.tarrantcounty.com/'
index_url = root_url + '/en/county/supermenu-contents/government/elected-county-officials.html#'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error. NEED TO INTEGRATE THROUGHOUT####
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code


#creates list of the three tables that contain county elected officials
soup = bs4.BeautifulSoup((requests.get(index_url)).text)
ALLtables = soup.select('tbody')
officials_to_scrape = [ALLtables[0],ALLtables[1], ALLtables[4], ALLtables[5],ALLtables[6]]

#loops through list, creates dictionaries for each official, adds them to dictList
def table_scrape():
	for table in officials_to_scrape:
		for row in table:
			tds = row('td')
			newDict = {}
			try:
				newDict['official.name'] = tds[0].get_text().encode('utf-8').replace('\n', '')
				newDict['office.name'] = tds[2].get_text().encode('utf-8').replace('\n', '')
				newDict['electoral.district'] = "Tarrant County"
				newDict['phone'] = tds[3].get_text().encode('utf-8')
				newDict['website'] = index_url
				newDict['state'] = 'TX'
				dictList.append(newDict)
			except:
				pass
	return dictList

table_scrape()

#adds additional detail to commissioners
def add_fields():
	for dictionary in dictList:
		if "Commissioner PCT" in dictionary['office.name']:
			dictionary['office.name'] = "Tarrant County "+dictionary['office.name'].replace('PCT', "Precinct")
			dictionary['electoral.district'] = "Tarrant County Council District " + dictionary['office.name'][-1]
			dictionary['address'] = '100 E. Weatherford, Fort Worth, Texas 76196'
			dictionary['website'] = 'http://access.tarrantcounty.com/en/commissioners-court.html'
		elif dictionary['office.name'] == "County Judge":
			dictionary['address'] = '100 E. Weatherford, Fort Worth, Texas 76196'
			dictionary['website'] = 'http://access.tarrantcounty.com/en/commissioners-court.html'
			#print dictionary

add_fields()

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
tarrant_county_board_file = open('tarrant_county_board.csv','wb')
csvwriter = csv.DictWriter(tarrant_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

tarrant_county_board_file.close()
 
with open("tarrant_county_board.csv", "r") as tarrant_county_board_csv:
     tarrant_county_board = tarrant_county_board_csv.read()

#print tarrant_county_board

