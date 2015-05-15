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
		newDict['official.name']= soup.select('h1')[0].get_text().encode('utf-8').replace('Brooklyn DA ', '')
		newDict['website'] = 'http://brooklynda.org'
		dictList.append(newDict)
	return dictList

kings_county()

#scrapes the page of queens county DA
def queens_countu():
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


queens_countu()


#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
kings_and_queens_county_board_file = open('kings_and_queens_county_board.csv','wb')
csvwriter = csv.DictWriter(kings_and_queens_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

kings_and_queens_county_board_file.close()
 
with open("kings_and_queens_county_board.csv", "r") as kings_and_queens_county_board_csv:
     kings_and_queens_county_board = kings_and_queens_county_board_csv.read()

#print kings_and_queens_county_board
