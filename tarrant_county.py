import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://access.tarrantcounty.com/'
index_url = root_url + '/en/county/supermenu-contents/government/elected-county-officials.html#'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#creates a list of the names and offices for the commissioners and other officials
names_and_offices = []
def get_basic_info():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        for item in soup.find_all('div', {'id':'wpsm-mainNavPane-government-threecollinks_1'})[0].get_text().encode('utf-8').replace('\n\n', '').replace('\xc2\xa0','').split('\n'):
            names_and_offices.append(item)
        for official in names_and_offices:
            if 'Peace' in official:
                names_and_offices.pop(names_and_offices.index(official))
        for official in names_and_offices:
            if official == 'Judges (Courts)':
                names_and_offices.pop(names_and_offices.index(official))
            elif official == 'Elected County names_and_offices':
                names_and_offices.pop(names_and_offices.index(official))
            elif official == 'Constables':
                names_and_offices.pop(names_and_offices.index(official))
    return names_and_offices

get_basic_info()

#creates a list of the urls for each official
urls = []
def get_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        outer_div = soup.find('div', {'id':'wpsm-mainNavPane-government-threecollinks_1'})
        inner_div = outer_div.find_all('div', {'class':'wpsm-mainNavMainPane-Col'})
        for div in inner_div:
            links = div.find_all('a')
            for link in links:
                urls.append(link.attrs.get('href'))
        for url in urls:
            if 'Constable' in url:
                urls.pop(urls.index(url))
            elif 'supermenu-contents/' in url:
                urls.pop(urls.index(url))
            elif 'eCourts' in url:
                urls.pop(urls.index(url))
        for url in urls:
            if 'JusticePeace' in url:
                urls.pop(urls.index(url))
    return urls

get_urls()

#formats everything into dictionaries for each official and then adds them to dictList
def make_dicts():
    for x in range(0,20):
        if x%2 == 0:
            newDict = {}
            newDict['office.name']= names_and_offices[x].replace(' - ', '')
            newDict['official.name'] = names_and_offices[x+1].strip()
            newDict['website'] = root_url + urls[x/2]
            if "Precinct" in newDict['office.name']:
                page_scrape= root_url + urls[x/2]
                if checkURL(page_scrape) == 404:
                    print '404 error. Check the url for {0}'.format(page_scrape)
                else:
                    page_soup = bs4.BeautifulSoup((requests.get(page_scrape)).text)
                    newDict['address'] = '100 E. Weatherford Room 502A Fort Worth, Texas 76196'
                    newDict['phone'] = '817-884-1234'
                    newDict['electoral.district'] = 'Tarrant County Council District '+ names_and_offices[x].replace(' - ', '')[-1]
            else:
                newDict['electoral.district'] = "Tarrant County"
            dictList.append(newDict)
    return dictList

make_dicts()

for dictionary in dictList:
    dictionary['state'] = 'TX'

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
