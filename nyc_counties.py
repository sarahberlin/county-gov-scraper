import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2


dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#scrapes page of kings county (brooklyn) DA
def kings_county():
	kings_da_url = 'http://brooklynda.org/brooklyn-da-ken-thompson/'
	if checkURL(kings_da_url) == 404:
		print '404 error. Check the url for {0}'.format(kings_da_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(kings_da_url)).text)
		newDict = {}
		newDict['office.name'] = "Distict Attorney"
		newDict['electoral.district'] = "Brooklyn"
		newDict['official.name']= soup.select('h2')[0].get_text().encode('utf-8').title().replace('Brooklyn Da\n', '')

		newDict['website'] = 'http://brooklynda.org'
		dictList.append(newDict)
	return dictList

kings_county()

#scrapes the page of queens county DA
def queens_county():
	queens_da_url = 'http://www.queensda.org/dabiography.html'
	if checkURL(queens_da_url) == 404:
		print '404 error. Check the url for {0}'.format(queens_da_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(queens_da_url)).text)
		newDict = {}
		newDict['office.name'] = "Distict Attorney"
		newDict['electoral.district'] = "Queens"
		newDict['official.name']= soup.select('td span strong')[0].get_text().encode('utf-8').replace('District Attorney ', '').replace("'s Biography ", "")
		newDict['website'] = 'http://www.queensda.org/index2.html'
		dictList.append(newDict)
	return dictList


queens_county()


#scrapes the page of New York county DA
def ny_county():
	ny_da_url = 'http://manhattanda.org/'
	if checkURL(ny_da_url) == 404:
		print '404 error. Check the url for {0}'.format(ny_da_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(ny_da_url)).text)
		newDict = {}
		newDict['office.name'] = "Distict Attorney"
		newDict['electoral.district'] = "Manhattan"
		newDict['official.name']= soup.select('p.header_block_data')[0].get_text().encode('utf-8').replace('Meet ', '').replace(', Your District Attorney', '').replace('"', '')
		newDict['website'] = ny_da_url
		dictList.append(newDict)
	return dictList

ny_county()


for dictionary in dictList:
    dictionary['state'] = 'NY'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
nyc_counties_file = open('nyc_counties.csv','wb')
csvwriter = csv.DictWriter(nyc_counties_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

nyc_counties_file.close()
 
with open("nyc_counties.csv", "r") as nyc_counties_csv:
     nyc_counties = nyc_counties_csv.read()

#print nyc_counties
