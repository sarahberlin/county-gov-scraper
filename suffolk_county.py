import requests
import bs4
import csv
from csv import DictWriter
import sys
import urllib, urllib2

root_url = 'http://legis.suffolkcountyny.gov'
index_url = root_url + '/legislators.html'

#creates empty list to store all of the officials' dictionaries
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code


#get page urls of all the councilors
page_urls = []
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
    	soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        for page_url in [a.attrs.get('href') for a in soup.select('table a[href*/do]')]:
        	if 'http' not in page_url:
        		page_urls.append('http://legis.suffolkcountyny.gov' + page_url)
        	else:
        		page_urls.append(page_url)
    return page_urls

get_page_urls()

def make_dicts():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        names = [img.get('alt') for img in soup.findAll('img')][1:-2]
        for x in range(0,18):
            govtdata = {}
            govtdata['official.name']= names[x]
            govtdata['office.name']= "County Legislator District {0}".format(x+1)
            govtdata['electoral.district']= "County Council District {0}".format(x+1)
            govtdata['website']= page_urls [x]
            govtdata['address']=  'William H. Rogers Building, North County Complex Smithtown, NY 11787'
            govtdata['phone']=  '(631) 853-4070'
            govtdata['state'] = 'NY'
            dictList.append(govtdata)
    return dictList

make_dicts()

#get data from non-commissioner sites
def govtdata():
    govsites = ['http://suffolkcountyny.gov/comptroller/Home.aspx', 'http://suffolkcountyny.gov/da/Home.aspx', 'http://suffolkcountyny.gov/sheriff/Home.aspx', 'http://suffolkcountyny.gov/Departments/countyclerk.aspx']
    for url in govsites:
        if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
        else:
            comptrollerDict = {}
            DADict = {}
            sheriffDict = {}
            clerkDict = {}
            soup = bs4.BeautifulSoup((requests.get(url)).text)
            if url == 'http://suffolkcountyny.gov/comptroller/Home.aspx':
                comptrollerDict['official.name'] = [img.attrs.get('alt') for img in soup.select('img[alt]')][1] 
                comptrollerDict['office.name'] = "Comptroller"
                comptrollerDict['website'] = url
                comptrollerDict['electoral.district'] = "Suffolk County"
                comptrollerDict['state'] = "NY"
                dictList.append(comptrollerDict)
            elif url == 'http://suffolkcountyny.gov/da/Home.aspx':
                DADict['official.name'] = soup.select('span.TitleHead')[0].get_text().encode('utf-8').replace('Suffolk County District Attorney ', '')
                DADict['office.name'] = 'District Attorney'
                DADict['website'] = url
                DADict['electoral.district'] = "Suffolk County"
                DADict['state'] = "NY"
                dictList.append(DADict)
            elif url == 'http://suffolkcountyny.gov/sheriff/Home.aspx':
                sheriffDict['official.name'] = [img.attrs.get('alt') for img in soup.select('img[alt]')][1].replace('Pictured is Sheriff ', '')
                sheriffDict['office.name'] = 'Sheriff'
                sheriffDict['website'] = url
                sheriffDict['electoral.district'] = 'Suffolk County'
                sheriffDict['state'] = "NY"
                dictList.append(sheriffDict)
            elif url == 'http://suffolkcountyny.gov/Departments/countyclerk.aspx':
            	clerkDict['official.name'] = soup.select('span.Head')[0].get_text().encode('utf-8').strip()
                clerkDict['office.name'] = 'County Clerk'
                clerkDict['website'] = url
                clerkDict['electoral.district'] = 'Suffolk County'
                clerkDict['state'] = "NY"
                dictList.append(clerkDict)

    return dictList

govtdata()


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
suffolk_county_board_file = open('suffolk_county_board.csv','wb')
csvwriter = csv.DictWriter(suffolk_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

suffolk_county_board_file.close()
 
with open("suffolk_county_board.csv", "r") as suffolk_county_board_csv:
     suffolk_county_board = suffolk_county_board_csv.read()

#print suffolk_county_board











