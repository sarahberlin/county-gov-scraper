import requests
import bs4
import csv
from csv import DictWriter
import sys
import urllib, urllib2

root_url = 'http://www.bexar.org'
index_url = root_url + '/152/Elected-Officials'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code


#get non-commissioner sites
govt_urls = []
def get_govt_urls():
    soup = bs4.BeautifulSoup((requests.get(index_url)).text)
    for site in [a.attrs.get('href') for a in soup.select('div.row a[href^=https://]')]:
        govt_urls.append(site)
    for site in [a.attrs.get('href') for a in soup.select('div.row a[href^=http://www]')]:
        if 'constables' not in site and 'jp' not in site and 'pcourt' not in site and site != 'http://www.bexar.org':
            govt_urls.append(site)
    return govt_urls

get_govt_urls()


#scrape non-commisioner officials' sites
def govtdata():
    clerkDict = {}
    DADict = {}
    districtclerkDict = {}
    sheriffDict = {}
    taxDict = {}
    for url in govt_urls:
        soup = bs4.BeautifulSoup((requests.get(url)).text)
        if 'comcourt' not in url:
            if url == 'https://gov.propertyinfo.com/tx-bexar/':
                clerkDict['official.name'] = soup.select('td p')[0].get_text().encode('utf-8').split(',')[1].strip()
                clerkDict['office.name'] = "County Clerk"
                clerkDict['website'] = url
                clerkDict['electoral.district'] = "Bexar County"
                dictList.append(clerkDict)
            elif url == 'http://www.bexar.org/da/index.html':
                DADict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').split(' | ')[0]
                DADict['office.name'] = "Criminal District Attorney"
                DADict['website'] = url
                DADict['electoral.district'] = "Bexar County"
                dictList.append(DADict)
            elif url == 'http://www.bexar.org/DC':
                districtclerkDict['official.name'] = soup.select('strong.Mctext')[0].get_text().encode('utf-8')
                districtclerkDict['office.name'] = "District Clerk"
                districtclerkDict['website'] = url
                districtclerkDict['electoral.district'] = "Bexar County"
                dictList.append(districtclerkDict)
            elif url == 'http://www.bexar.org/sheriff':
                sheriffDict['official.name'] = soup.select('strong')[0].get_text().encode('utf-8').title()
                sheriffDict['office.name'] = "Sheriff"
                sheriffDict['website'] = url
                sheriffDict['electoral.district'] = "Bexar County"
                dictList.append(sheriffDict)
            elif url == 'http://www.bexar.org/tax':
                taxDict['official.name'] = soup.select('p strong')[0].get_text().encode('utf-8').replace(', MPA, PCC', '')
                taxDict['office.name'] = "Tax Assessor-Collector"
                taxDict['website'] = url
                taxDict['electoral.district'] = "Bexar County"
                dictList.append(taxDict)
    return dictList

govtdata()

#get commissioner sites
commissioner_urls = []

def get_councilor_pages():
    page_url = 'http://www.bexar.org/146/Commissioners-Court'
    soup = bs4.BeautifulSoup((requests.get(page_url)).text)
    for page in [a.attrs.get('href') for a in soup.select('li.topMenuItem a[href^]')]:
        if 'Judge' in page or 'commissioner' in page:
            commissioner_urls.append('http://www.bexar.org'+page)
        elif "Precinct" in page:
            commissioner_urls.append('http://www.bexar.org'+page)
    return commissioner_urls

get_councilor_pages()

#get commissioner data
def get_councilor_data():
    for page in commissioner_urls:
        councilor_data = {}
        official_soup = bs4.BeautifulSoup((requests.get(page)).text)
        councilor_data['address']='101 W. Nueva 10th Floor San Antonio, TX 78205-3482'
        councilor_data['phone']='210-335-2626'
        councilor_data['website']= page
        if 'Judge' in page:
            councilor_data['official.name'] = official_soup.select('title')[0].get_text().encode('utf-8').split('Judge')[1].strip().split('|')[0].strip()
            councilor_data['office.name'] = 'County Judge'
            councilor_data['electoral.district'] = 'Bexar County'
            dictList.append(councilor_data)
        else:
            if 'Precinct-3' in page:
                councilor_data['official.name'] = [img.attrs.get('alt') for img in official_soup.select('img[alt]')][4]
            elif 'Precinct-4' in page:
                councilor_data['official.name']= official_soup.select('h3')[2].get_text().encode('utf-8')
            else:
                councilor_data['official.name']= official_soup.select('h2')[0].get_text().encode('utf-8').replace("\xc2\xa0", '').replace('\n', '').replace("\xe2\x80\x9c", "'").replace("\xe2\x80\x9d", "'").replace("Commissioner", "").strip().title()
            councilor_data['office.name'] = 'County Commissioner Precinct '+ page[-1]
            councilor_data['electoral.district'] = 'Bexar County Council District ' + page[-1]
            dictList.append(councilor_data)
    return dictList

get_councilor_data()


for dictionary in dictList:
    dictionary['state'] = 'TX'


fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
bexar_county_board_file = open('bexar_county_board.csv','wb')
csvwriter = csv.DictWriter(bexar_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

bexar_county_board_file.close()
 
with open("bexar_county_board.csv", "r") as bexar_county_board_csv:
     bexar_county_board = bexar_county_board_csv.read()

#print bexar_county_board

