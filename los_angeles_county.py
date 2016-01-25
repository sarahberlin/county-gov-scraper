import requests
import bs4
import csv
from csv import DictWriter
import sys
import urllib, urllib2

root_url = 'https://www.lacounty.gov/government'
index_url = root_url + '/supervisors'

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
def get_page_urls():
    if checkURL(index_url) == 404:
        print '404 error. Check the url for {0}'.format(index_url)
    else:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text)
        return [a.attrs.get('href') for a in soup.select('div.secondlevel-right div.slr-item a[href^=https://www.lacounty.gov/government/supervisors/]')]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(page_url) == 404:
        print '404 error. Check the url for {0}'.format(page_url)
    else:
        councilor_data = {}
        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text)
        try:
            councilor_data['official.name'] = soup.select('title')[0].get_text().encode('utf-8').split(' - ')[0]
            councilor_data['electoral.district'] = "Los Angeles County Council District " + soup.select('h1 span')[0].get_text().encode('utf-8')[0]
            councilor_data['office.name'] = "County Supervisor District " + soup.select('h1 span')[0].get_text().encode('utf-8')[0]
            councilor_data['phone'] = soup.find('span', {'class': 'icon'}).get_text().encode('utf-8')
            councilor_data['website'] =  [a.attrs.get('href') for a in soup.select('div.supervisor-info-col a[href]')][1].encode('utf-8')
            councilor_data['email'] = [a.attrs.get('href') for a in soup.select('div.supervisor-info-col a[href]')][2].encode('utf-8').replace('mailto:','')
            councilor_data['facebook'] = [a.attrs.get('href') for a in soup.select('div.supervisor-info-col a[href]')][3].encode('utf-8')
            councilor_data['twitter'] = [a.attrs.get('href') for a in soup.select('div.supervisor-info-col a[href]')][4].encode('utf-8')
            councilor_data['address'] = '500 W. Temple St. Room 358, Los Angeles 90012'
        except:
            pass
        return councilor_data


#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url))

#get data drom non-commissioner sites

def assessor_scrape():
    url = 'http://assessor.lacounty.gov/'
    if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
    else:
        soup = bs4.BeautifulSoup((requests.get(url)).text)
        assessorDict = {}
        assessorDict['official.name'] = soup.find('div', {'class': 'ms-layer  msp-cn-8-5'}).get_text().encode('utf-8').replace('\n', '')
        assessorDict['office.name'] = "Assessor"
        assessorDict['website'] = url
        assessorDict['electoral.district'] = "Los Angeles County"
        dictList.append(assessorDict)
    return dictList

def sheriff_scrape():
    url = 'http://sheriff.lacounty.gov/wps/portal/lasd'
    if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
    else:
        soup = bs4.BeautifulSoup((requests.get(url)).text)
        sheriffDict = {}
        sheriffDict['official.name'] = soup.find_all('td', {'colspan': 2})[1].get_text().encode('utf-8')
        sheriffDict['office.name'] = 'Sheriff'
        sheriffDict['website'] = url
        sheriffDict['electoral.district'] = 'Los Angeles County'
        dictList.append(sheriffDict)
    return dictList

def da_scrape():
    url = 'http://da.lacounty.gov/'
    if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
    else:
        soup = bs4.BeautifulSoup((requests.get(url)).text)
        DADict = {}
        DADict['official.name'] = soup.find('span', {'class':'big_blue_header'}).get_text().encode('utf-8')
        DADict['office.name'] = 'District Attorney'
        DADict['website'] = url
        DADict['electoral.district'] = "Los Angeles County"
        dictList.append(DADict)
    return dictList

#assessor_scrape()
#sheriff_scrape()
#da_scrape()

for dictionary in dictList:
    dictionary['state'] = 'CA'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
la_county_supervisors_file = open('la_county_supervisors.csv','wb')
csvwriter = csv.DictWriter(la_county_supervisors_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

la_county_supervisors_file.close()
 
with open("la_county_supervisors.csv", "r") as la_county_supervisors_csv:
     la_county_supervisors = la_county_supervisors_csv.read()

#print la_county_supervisors

