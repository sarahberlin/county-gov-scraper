
import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.clarkcountynv.gov'
index_url = root_url + '/electedofficials/Pages/Default2.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#get page urls of all the councilors
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        return [a.attrs.get('href') for a in soup.select('td p a[href^=/depts/countycom]')]


#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(root_url + page_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url + page_url)
    else:
	    councilor_data = {}
	    soup = bs4.BeautifulSoup((requests.get(root_url + page_url)).text)
	    try:
	    	councilor_data['office.name'] = "County Comissioner "+soup.select('div.CC_Banner_Short_Banner')[0].get_text().encode('utf-8').split(':')[0]
	    	councilor_data['official.name'] = soup.select('div.CC_Banner_Short_Banner')[0].get_text().encode('utf-8').split(':')[1].strip()
	    	councilor_data['electoral.district'] = "Clark County Council " + soup.select('div.CC_Banner_Short_Banner')[0].get_text().encode('utf-8').split(':')[0][-1]
	    	councilor_data['website'] = root_url+page_url
	    	councilor_data['address']= '500 S. Grand Central Parkway Las Vegas, Nevada 89155'
	    	contact_page = (root_url+page_url).replace('/Pages/default.aspx','')+ '/Pages/ContactUs.aspx'
	    	contact_soup = bs4.BeautifulSoup((requests.get(contact_page)).text)
	    	councilor_data['email'] = [a.attrs.get('href') for a in contact_soup.select('div a[href^=mailto:]')][0].replace('mailto:', '')
	    	councilor_data['phone']= contact_soup.select('div.contactDetails')[0].get_text().encode('utf-8').split('Phone:')[1].replace('\r\n\t', '').replace('\t', '')
	    except:
	    	pass
    return councilor_data

#runs scripts together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#gets data from non-commissioner officials
def get_govt_data():
	govt_page = '/ElectedOfficials/Pages/ClarkCountyOfficials.aspx'
	if checkURL(root_url + govt_page) == 404:
		print '404 error. Check the url for {0}'.format(govt_page)
	else:
		soup = bs4.BeautifulSoup((requests.get(root_url + govt_page)).text)
		table = []
		for x in range(2,23):
			table.append(soup.select('tbody td')[x].get_text().encode('utf-8').replace('\xc2\xa0', '').replace('\n', '').strip())
		table_data = []
		for x in range(0,21):
			if x < 3:
				table_data.append(table[x])
			elif 5 < x < 9:
				table_data.append(table[x])
			elif 11 < x < 15:
				table_data.append(table[x])
			elif 17 < x:
				table_data.append(table[x])
		links = [a.attrs.get('href') for a in soup.select('td p a[href]')][:5]
		for x in range(0,10):
			if x == 0:
				newDict ={}
				newDict['office.name']= table_data[x]
				newDict['official.name']= table_data[x+3]
				newDict['website']= 'http://www.clarkcountynv.gov/'+links[x]
				newDict['electoral.district'] = 'Clark County'
				dictList.append(newDict)
			elif x == 1:
				newDict ={}
				newDict['office.name']= table_data[x]
				newDict['official.name']= table_data[x+3]
				newDict['website'] = 'http://www.clarkcountynv.gov/'
				newDict['electoral.district'] = 'Clark County'
				dictList.append(newDict)
			elif x == 2:
				newDict ={}
				newDict['office.name']= table_data[x]
				newDict['official.name']= table_data[x+3]
				newDict['website'] = 'http://www.clarkcountynv.gov/'+links[x-1]
				newDict['electoral.district'] = 'Clark County'
				dictList.append(newDict)
			elif 9> x > 5:
				newDict ={}
				newDict['office.name']= table_data[x]
				newDict['official.name']= table_data[x+3]
				newDict['website']='http://www.clarkcountynv.gov/'+links[x-4]
				newDict['electoral.district'] = 'Clark County'
				dictList.append(newDict)
	return dictList

get_govt_data()



#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
clark_county_board_file = open('clark_county_board.csv','wb')
csvwriter = csv.DictWriter(clark_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

clark_county_board_file.close()
 
with open("clark_county_board.csv", "r") as clark_county_board_csv:
     clark_county_board = clark_county_board_csv.read()

#print clark_county_board
