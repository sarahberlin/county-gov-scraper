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

#root and index urls for non-commissioner elected officials
govt_root_url = 'http://www.waynecounty.com'
govt_index_url = govt_root_url + '/elected.htm'

#gets urls for each non-commissioner elected official and adds to list govt_page_urls
govt_page_urls = []
def get_govt_page_urls():
	if checkURL(govt_index_url) == 404:
		print '404 error. Check the url for {0}'.format(govt_index_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(govt_index_url)).text)
		for url in [a.attrs.get('href') for a in soup.select('div.deptText a[href]')]:
			govt_page_urls.append(url.strip())
		govt_page_urls.pop(govt_page_urls.index('/commission/index.htm'))
	return govt_page_urls

#scrapes each url
def get_govt_data(govt_page_url):
	if checkURL(govt_root_url + govt_page_url) == 404:
		print '404 error. Check the url for {0}'.format(govt_root_url + govt_page_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(govt_root_url + govt_page_url)).text)
		councilor_data = {}
		councilor_data['official.name'] = soup.select('div.infoName')[0].get_text().encode('utf-8').replace('\r\n', '').replace('            ', '').replace('\xc2\xa0', '').strip()
		councilor_data['electoral.district'] = 'Wayne County'
		councilor_data['website'] = govt_root_url + govt_page_url
		councilor_data['address'] = ''
		councilor_data['email'] = [a.attrs.get('href') for a in soup.select('div.infoEmail a[href]')][0].replace('mailto:', '').replace('?name=', '')
		councilor_data['phone'] = soup.select('div.infoPhone')[0].get_text().encode('utf-8').strip()
		if 'deeds' in govt_page_url:
			councilor_data['office.name'] = "Register of Deeds"
		else:
			councilor_data['office.name'] = soup.select('div.infoName')[1].get_text().encode('utf-8').replace('Wayne ', '')
	return councilor_data

#runs programs together and adds dictionaries to dictList
get_govt_page_urls()
for govt_page_url in govt_page_urls:
	dictList.append(get_govt_data(govt_page_url))

#root and index urls for commissioners
councilor_root_url = 'http://www.waynecounty.com'
councilor_index_url = councilor_root_url +'/commission/commissioners.htm'

#gets urls for commissioners
def get_councilor_urls():
	if checkURL(councilor_index_url) == 404:
		print '404 error. Check the url for {0}'.format(councilor_index_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(councilor_index_url)).text)
	return [a.attrs.get('href') for a in soup.select('div.deptList a[href^=/commission/district]')]

#scrapes each commissioner's page
def get_councilor_data(councilor_url):     
	if checkURL(councilor_root_url + councilor_url) == 404:
		print '404 error. Check the url for {0}'.format(councilor_root_url + councilor_url)
	else:
		soup = bs4.BeautifulSoup((requests.get(councilor_root_url + councilor_url)).text)
		councilor_data = {}
		councilor_data['official.name'] = soup.select('div.infoName')[0].get_text().encode('utf-8').replace('\r\n', '').replace('            ', '').replace('\xc2\xa0', '').strip()
		councilor_data['electoral.district'] = 'Wayne County Council ' + soup.select('div.infoName')[1].get_text().encode('utf-8').split(' Commissioner')[0]
		councilor_data['office.name'] = "Commissioner "+ soup.select('div.infoName')[1].get_text().encode('utf-8').split(' Commissioner')[0]
		councilor_data['website'] = councilor_root_url + councilor_url
		councilor_data['address'] = '500 Griswold St. 7th Floor, Detroit, MI 48226'
		councilor_data['email'] = [a.attrs.get('href') for a in soup.select('div.infoEmail a[href]')][0].replace('mailto:', '').replace('?name=', '')
		councilor_data['phone'] = soup.select('div.infoPhone')[0].get_text().encode('utf-8').strip()
	return councilor_data

#runs functions together and adds dictionaries to dictList
councilor_urls = get_councilor_urls()
for councilor_url in councilor_urls:
	dictList.append(get_councilor_data(councilor_url))

for dictionary in dictList:
    dictionary['state'] = 'MI'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
wayne_county_board_file = open('wayne_county_board.csv','wb')
csvwriter = csv.DictWriter(wayne_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

wayne_county_board_file.close()
 
with open("wayne_county_board.csv", "r") as wayne_county_board_csv:
     wayne_county_board = wayne_county_board_csv.read()

#print wayne_county_board