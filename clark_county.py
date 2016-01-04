#!/usr/bin/python
# -*- coding: latin-1 -*-


import csv
from csv import DictWriter
import urllib, urllib2

from selenium import webdriver
import lxml.html as lh

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#empty list that all the dictionaries will be appended to
dictList = []

#main page url
root_url = 'http://www.clarkcountynv.gov'

################ scraping county commissioners #########
index_url = root_url + '/elected-officials/Pages/Default.aspx'
comm_page_list = []

#get page urls of all the councilors
def get_page_urls():
	if checkURL(index_url) == 404:
		print '404 error. Check the url for {0}'.format(index_url)
	else:
		driver = webdriver.PhantomJS()
		driver.get(index_url)
		content = driver.page_source
		driver.quit()
		doc = lh.fromstring(content)
		for page in doc.xpath('//div/p/a/@href'):
			if len(page) == 31:
				comm_page_list.append(str(page))
		return comm_page_list


def get_councilor_data(page_url):
	if checkURL(root_url + page_url + '/Pages/default.aspx') == 404:
		print '404 error. Check the url for {0}'.format(root_url + page_url + '/Pages/default.aspx')
	else:
		driver = webdriver.PhantomJS()
		driver.get(root_url + page_url + '/Pages/default.aspx')
		content = driver.page_source
		driver.quit()
		doc = lh.fromstring(content)
		for x in doc.xpath('//h2//text()[1]'):
			councilor_data = {}
			district = x.split('-')[0].strip()
			name = x.split('-')[1].strip()
			councilor_data['office.name'] = 'County Commissioner ' + district
			councilor_data['electoral.district'] = 'Clark County Council ' + district
			councilor_data['official.name'] = name
			councilor_data['website'] = root_url+page_url
			councilor_data['address']= '500 S. Grand Central Parkway Las Vegas, Nevada 89155'
			councilor_data['email'] = 'ccdist' + district[-1] + '@ClarkCountyNV.gov'
			councilor_data['phone']= '(702) 455-3500'
			councilor_data['state'] = 'NV'
			return councilor_data


#run the functions together
get_page_urls()
page_urls = comm_page_list
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url))


################ scraping other elected officials #########

other_page_list = []
other_index_url = root_url + '/elected-officials/Pages/ClarkCountyOfficials.aspx'


def get_other_urls():
	if checkURL(other_index_url) == 404:
		print '404 error. Check the url for {0}'.format(other_index_url)
	else:
		driver = webdriver.PhantomJS()
		driver.get(other_index_url)
		content = driver.page_source
		driver.quit()
		doc = lh.fromstring(content)
		for page in doc.xpath('//tr/td/p/span/a/@href'):
			if '/Pages/Default.aspx' not in page:
				other_page_list.append(str(page))
		return other_page_list


def get_other_data(other_page_url):
	if checkURL(root_url + other_page_url) == 404:
		print '404 error. Check the url for {0}'.format(root_url + other_page_url)
	else:
		driver = webdriver.PhantomJS()
		driver.get(root_url + other_page_url)
		content = driver.page_source
		driver.quit()
		doc = lh.fromstring(content)
		if other_page_url == '/elected-officials/Pages/PublicAdministrator.aspx':
			for x in doc.xpath('//span[@class="ms-rteFontSize-3"][1]//text()[1]'):
				councilor_data = {}
				office = x.encode('utf-8').split('  ')[0]
				name = x.encode('utf-8').split('  ')[1]
				councilor_data['office.name'] = office
		elif other_page_url == '/elected-officials/Pages/CountyAssessor.aspx':
			for x in doc.xpath('//span[@class="ms-rteThemeForeColor-5-4 ms-rteFontSize-3"][1]//text()'):
				councilor_data = {}
				office = x.encode('utf-8').split('\xa0 ')[0].replace('\xc2','')
				name = x.encode('utf-8').split('\xa0 ')[1].replace('\xc2\xa0','')
				councilor_data['office.name'] = office
				councilor_data['official.name'] = name
		elif other_page_url == '/elected-officials/Pages/CountyTreasurer.aspx':
			for x in doc.xpath('//span[@class="ms-rteFontSize-3"][1]//text()'):
				councilor_data = {}
				office = x.encode('utf-8').split('\xc2\xa0 ')[0] + ' ' + x.encode('utf-8').split('\xc2\xa0 ')[1]
				name = x.encode('utf-8').split('\xc2\xa0 ')[2].replace('\xc2\xa0','')
				councilor_data['office.name'] = office
				councilor_data['official.name'] = name
		else:
			for x in doc.xpath('//span[@class="ms-rteFontSize-3"][1]//text()'):
				councilor_data = {}
				office = x.encode('utf-8').split('\xc2\xa0 ')[0]
				name = x.encode('utf-8').split('\xc2\xa0 ')[1].replace('\xc2\xa0','') 
				councilor_data['office.name'] = office
		councilor_data['electoral.district'] = 'Clark County'
		councilor_data['official.name'] = name
		councilor_data['website'] = root_url+other_page_url
		councilor_data['state'] = 'NV'
		return councilor_data


#run the functions together
get_other_urls()
other_page_urls = other_page_list
for other_page_url in other_page_urls:
	dictList.append(get_other_data(other_page_url))


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
clark_county_board_file = open('clark_county_board.csv','wb')
csvwriter = csv.DictWriter(clark_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

clark_county_board_file.close()
 
with open("clark_county_board.csv", "r") as clark_county_board_csv:
     clark_county_board = clark_county_board_csv.read()

#print clark_county_board