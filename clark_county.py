
import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

masterList = []

root_url = 'http://www.clarkcountynv.gov'
index_url = root_url + '/electedofficials/Pages/Default2.aspx'

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
    masterList.append(get_councilor_data(page_url)) 


#checks for error in pulls down table of elected officials
clark_officials = 'http://www.clarkcountynv.gov/ElectedOfficials/Pages/ClarkCountyOfficials.aspx'
def get_table():
	if checkURL(clark_officials) == 404:
		print '404 error. Check the url for {0}'.format(clark_officials)
	else:
		req = urllib2.Request(clark_officials)
		page = urllib2.urlopen(req)
		soup = bs4.BeautifulSoup(page)
		table = soup.find("table", { "style" : "height:329px;width:653px;background-color:#c6d9f0" })
		return table

#scrapes table of elected officials, adding each dictionary, some of which do not have data, to templist. note: cells refers to the columns, their indices are 0, 1, 2
tempList = []
def scrape_officials_table():
	if checkURL(clark_officials) == 404:
		print '404 error. Check the url for {0}'.format(clark_officials)
	else:
		for i,row in enumerate(get_table().findAll("tr")):
			cells = row.findAll("td")
			if len(cells) > 2:
				class System():
					def __init__(self):
						self.tempList = []
				columnlist = []
				column1 = cells[0]
				column2 = cells[1]
				column3 = cells[2]
				columnlist.extend([column1, column2, column3])
				for column in columnlist:
					for p in column:
						try:
							pdict = {}
							pdict['text'] = p.get_text().encode('utf-8').replace('\xa0', ' ').replace('\xc2', '').strip()
							pdict['link'] = [a.attrs.get('href') for a in column.select('p a[href]')]
							if len(pdict['text']) > 0 or len(pdict['link']) > 0:
								tempList.append(pdict)
						except:
							pass
		return tempList

scrape_officials_table()

#loops through the dictionaries in templist and reformats data before appending to masterList
def make_officials_dicts():
	if checkURL(clark_officials) == 404:
		print '404 error. Check the url for {0}'.format(clark_officials)
	else:
		for x in range(0,9):
			if 9 > x > 5 or x < 3:
				officialDict = {}
				officialDict['office.name'] = tempList[x]['text']
				officialDict['official.name'] = tempList[x+3]['text']
				officialDict['website'] = root_url + str(tempList[x+3]['link']).replace('[', '').replace(']','').replace("'", "")
				officialDict['electoral.district'] = "Clark County"
				masterList.append(officialDict)
		return masterList

make_officials_dicts()


for dictionary in masterList:
    dictionary['state'] = 'NV'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
clark_county_board_file = open('clark_county_board.csv','wb')
csvwriter = csv.DictWriter(clark_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in masterList:
    csvwriter.writerow(row)

clark_county_board_file.close()
 
with open("clark_county_board.csv", "r") as clark_county_board_csv:
     clark_county_board = clark_county_board_csv.read()

#print clark_county_board

