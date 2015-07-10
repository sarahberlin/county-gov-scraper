import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.broward.org'
index_url = root_url + '/Commission/Pages/default.aspx'

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
        print '404 error. Check the url.'
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        return [a.attrs.get('href') for a in soup.select('a[href^=/Commission/District]')][:9]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(index_url) == 404:
        print '404 error. Check the url.'
    else:
        councilor_data = {}
        soup = bs4.BeautifulSoup((requests.get(root_url + page_url)).text)
        try:
            councilor_data['office.name'] = 'County Commissioner ' + soup.select('a.breadcrumbCurrent')[0].get_text().encode('utf-8').split(' - ')[0]
            councilor_data['official.name'] = soup.select('a.breadcrumbCurrent')[0].get_text().encode('utf-8').split(' - ')[1]
            councilor_data['electoral.district'] = "Broward County Council " + soup.select('a.breadcrumbCurrent')[0].get_text().encode('utf-8').split(' - ')[0]
            councilor_data['website'] = root_url+page_url
            councilor_data['address']= '115 S. Andrews Ave., Room 409, Fort Lauderdale, FL 33301-1872'
            councilor_data['phone']= '954-357-7000'
            contact_page = (root_url + page_url).replace('/Pages/Default.aspx', '/Pages/ContactUs.aspx').replace('/Pages/default.aspx', '/Pages/ContactUs.aspx')
            contact_soup = bs4.BeautifulSoup((requests.get(contact_page)).text)
            councilor_data['email'] = [a.attrs.get('href') for a in contact_soup.select('p a[href^=mailto]')][0].replace('mailto:', '')
        except:
            pass
    return councilor_data

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url)) 

#scrapes sites for sheriff,property appraiser, clerk of courts, supervisor of elections

def get_govt_data():
    sites = ['http://www.browardsoe.org/Portals/Broward/Documents/OfficeHolders/electedofficial.aspx_id_332.html', 'http://www.browardsoe.org/Portals/Broward/Documents/OfficeHolders/electedofficial.aspx_id_333.html', 'http://www.browardsoe.org/Portals/Broward/Documents/OfficeHolders/electedofficial.aspx_id_334.html', 'http://www.browardsoe.org/Portals/Broward/Documents/OfficeHolders/electedofficial.aspx_id_320.html']
    for site in sites:
        if checkURL(site) == 404:
            print '404 error. Check the url for {0}'.format(site)
        else:
            soup = bs4.BeautifulSoup((requests.get(site)).text)
            newDict = {}
            newDict['office.name'] = soup.select('h1')[0].get_text().encode('utf-8').replace('\n','')
            newDict['official.name'] = soup.find_all('span', {'id':'lblName'})[0].get_text().encode('utf-8')
            newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href]')][1]
            newDict['address'] = soup.find_all('span', {'id':'lblLocation1Address'})[0].get_text().encode('utf-8').replace('Room', ' Room').replace('Fort', " Fort").strip()
            newDict['phone'] = soup.find_all('span', {'id':'lblOffice1Phone'})[0].get_text().encode('utf-8')
            newDict['electoral.district'] = "Broward County"
            dictList.append(newDict)
    return dictList

get_govt_data()

for dictionary in dictList:
    dictionary['state'] = 'FL'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
broward_county_board_file = open('broward_county_board.csv','wb')
csvwriter = csv.DictWriter(broward_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

broward_county_board_file.close()
 
with open("broward_county_board.csv", "r") as broward_county_board_csv:
     broward_county_board = broward_county_board_csv.read()

#print broward_county_board
