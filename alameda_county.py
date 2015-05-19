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

root_url = 'http://www.acgov.org'
index_url = root_url + '/government/elected.htm'


#gets urls for each official
urls = []
def get_urls():
	if checkURL(index_url) == 404:
		print '404 error. Check the url for {0}'.format(index_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(index_url)).text)
		infobar = soup.find_all('div', {'id':'infobar'})[0]
		for url in [a.attrs.get('href') for a in infobar.select('a[href]')][:11]:
			urls.append(url)
		return urls

get_urls()

#scrapes the elected officials page and creates a dictionary for each official
def get_data():
	if checkURL(index_url) == 404:
		print '404 error. Check the url for {0}'.format(index_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(index_url)).text)
		for y in range(0,11):
			govtdata = {}
			if 'Board' in soup.select('ul.bullet li')[y].get_text():
				govtdata['office.name'] = soup.select('ul.bullet li')[y].get_text().encode('utf-8').split(',')[0] + soup.select('ul.bullet li')[y].get_text().encode('utf-8').split(',')[1]
				govtdata['official.name'] = soup.select('ul.bullet li')[y].get_text().encode('utf-8').split(',')[2].replace('\t', '')
				govtdata['electoral.district'] = 'Alameda County Council District ' + soup.select('ul.bullet li')[y].get_text().encode('utf-8')[22]
				govtdata['website'] = root_url + urls[y]
				govtdata['address'] = 'County of Alameda Administration Building 1221 Oak Street, #536, Oakland, CA 94612'
				govtdata['phone'] = '(510) 272-669' + soup.select('ul.bullet li')[y].get_text().encode('utf-8')[22]
				dictList.append(govtdata)
			else:
				govtdata['office.name'] = soup.select('ul.bullet li')[y].get_text().encode('utf-8').split(',')[0]
				govtdata['official.name'] = soup.select('ul.bullet li')[y].get_text().encode('utf-8').split(',')[1]
				govtdata['electoral.district'] = 'Alameda County'
				govtdata['website'] = root_url + urls[y]
				dictList.append(govtdata)
		return dictList

get_data()

for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
alameda_county_supervisors_file = open('alameda_county_supervisors.csv','wb')
csvwriter = csv.DictWriter(alameda_county_supervisors_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

alameda_county_supervisors_file.close()
 
with open("alameda_county_supervisors.csv", "r") as alameda_county_supervisors_csv:
     alameda_county_supervisors = alameda_county_supervisors_csv.read()

#print alameda_county_supervisors











