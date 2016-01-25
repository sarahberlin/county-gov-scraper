import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.dallascounty.org'
index_url = '/government.php'


#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#empty list for non-commissioner sites
govt_sites = []

#gets sites for non-commissioners from county gov homepage and adds them to govt_sites list
def get_govt_sites():
    if checkURL(root_url+index_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url+index_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url+index_url)).text)
        for site in [a.attrs.get('href') for a in soup.select('div.text a[href]')]:
            if 'constable' not in site and 'jpcourt' not in site and 'probate' not in site and 'civil_district' not in site and 'criminal_district' not in site and 'county_criminal' not in site and 'family_district' not in site and 'juvenile' not in site and '/county_court_at_law' not in site and 'volunteer' not in site and 'wiki' not in site and 'whois' not in site:
                govt_sites.append(site)
    return govt_sites

get_govt_sites()


#get data from non-commissioners
def govtdata():
    cjudgeDict = {}
    clerkDict = {}
    DADict = {}
    districtclerkDict = {}
    sheriffDict = {}
    taxDict = {}
    treasurerDict = {}
    for site in govt_sites:
        if site == 'department/da/da_index.php':
            if checkURL(root_url+'/'+site) == 404:
                print '404 error. Check the url for {0}'.format(root_url+'/'+site)
            else:
                soup = bs4.BeautifulSoup((requests.get((root_url + '/' + site).replace('/da_index.php', '/meettheda.php'))).text)
                DADict['official.name'] = soup.select('p.subhead')[0].get_text().encode('utf-8')
                DADict['office.name'] = "District Attorney"
                DADict['website'] = root_url + '/' + site
                DADict['electoral.district'] = "Dallas County"
                dictList.append(DADict)
        else:
            if checkURL(root_url+site) == 404:
                print '404 error. Check the url for {0}'.format(root_url+site)
            else:
                soup = bs4.BeautifulSoup((requests.get(root_url+site)).text)
                if site == '/department/comcrt/cjenkins.php':
                    cjudgeDict['official.name'] = soup.select('p.subhead')[0].get_text().encode('utf-8').replace(', Dallas County Judge', '')
                    cjudgeDict['office.name'] = "County Judge"
                    cjudgeDict['website'] = root_url + site
                    cjudgeDict['electoral.district'] = "Dallas County"
                    dictList.append(cjudgeDict)
                elif site == '/department/countyclerk/countyclerk.php':
                    clerkDict['official.name'] = soup.select('p.subhead')[2].get_text().encode('utf-8')
                    clerkDict['office.name'] = "County Clerk"
                    clerkDict['website'] = root_url + site
                    clerkDict['electoral.district'] = "Dallas County"
                    dictList.append(clerkDict)
                elif site == '/department/districtclerk/districtclerk_index.html':
                    districtclerkDict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').replace('Dallas County District Clerk ', '')
                    districtclerkDict['office.name'] = "District Clerk"
                    districtclerkDict['website'] = root_url + site
                    districtclerkDict['electoral.district'] = "Dallas County"
                    dictList.append(districtclerkDict)
                elif site == '/department/sheriff/sheriff_intro.php':
                    soup = bs4.BeautifulSoup((requests.get((root_url+site).replace('/sheriff_intro.php',''))).text)
                    sheriffDict['official.name'] = soup.select('p.subhead')[0].get_text().encode('utf-8').replace('Sheriff ', '')
                    sheriffDict['office.name'] = "Sheriff"
                    sheriffDict['website'] = root_url + site
                    sheriffDict['electoral.district'] = "Dallas County"
                    dictList.append(sheriffDict)
                elif site == '/department/tax/taxoffice_home.html':
                    taxDict['official.name'] = soup.select('span.bold')[0].get_text().encode('utf-8').replace(', CTA','')
                    taxDict['office.name'] = "Tax Assessor-Collector"
                    taxDict['website'] = root_url + site
                    taxDict['electoral.district'] = "Dallas County"
                    dictList.append(taxDict)
                elif site == '/department/treasurer/treasurer_index.php':
                    treasurerDict['official.name']= soup.select('p strong a')[0].get_text().encode('utf-8')
                    treasurerDict['office.name']= "Treasurer"
                    treasurerDict['website']= root_url + site
                    treasurerDict['electoral.district']= "Dallas County"
                    dictList.append(treasurerDict)
    return dictList

govtdata()

#scrape county commissioner's sites
def get_councilor_data():
    councilors_url = 'http://www.dallascounty.org/department/comcrt/whois.php'
    if checkURL(councilors_url) == 404:
        print '404 error. Check the url for {0}'.format(councilors_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(councilors_url)).text)
        councilor_sites = [a.attrs.get('href') for a in soup.select('table.alternate_rows a[href]')][2:]
        for site in councilor_sites:
            if checkURL(('http://www.dallascounty.org/department/comcrt/' + site).replace('/department/comcrt//department/comcrt/','/department/comcrt/')) == 404:
                print '404 error. Check the url for {0}'.format(('http://www.dallascounty.org/department/comcrt/' + site).replace('/department/comcrt//department/comcrt/','/department/comcrt/'))
            else:
                councilor_soup = bs4.BeautifulSoup((requests.get(('http://www.dallascounty.org/department/comcrt/' + site).replace('/department/comcrt//department/comcrt/','/department/comcrt/'))).text)
                newDict = {}
                newDict['website'] = ('http://www.dallascounty.org/department/comcrt/' + site).replace('/department/comcrt//department/comcrt/','/department/comcrt/')
                newDict['address']=  '411 Elm St., 2nd Floor Dallas, Texas 75202'
                if 'daniel' in site or 'district4' in site:
                    newDict['official.name'] = councilor_soup.select('td li a')[1].get_text().encode('utf-8').title()
                    newDict['office.name']="County Commissioner "+councilor_soup.select('td li a')[2].get_text().encode('utf-8').title().replace(' Map', '')
                    newDict['electoral.district']= "Dallas County Council " + councilor_soup.select('td li a')[2].get_text().encode('utf-8').title().replace(' Map', '')
                    newDict['phone']='214-653-7361'
                elif 'district2' in site:
                    newDict['official.name'] = councilor_soup.find_all('div', {'id': 'masthead'})[0].get_text().encode('utf-8').replace('Commissioner ', '').split('\r\n')[0]
                    newDict['office.name']= "County Commissioner "+councilor_soup.find_all('div', {'id': 'masthead'})[0].get_text().encode('utf-8').replace('Commissioner ', '').split('\r\n')[1]
                    newDict['electoral.district']= "Dallas County Council "+councilor_soup.find_all('div', {'id': 'masthead'})[0].get_text().encode('utf-8').replace('Commissioner ', '').split('\r\n')[1]
                elif 'district3' in site:
                    newDict['official.name'] =councilor_soup.find_all('span', {'id': 'pagetitle'})[0].get_text().encode('utf-8').split('\xe2\x80\x93')[0].replace('Commissioner', '').strip()
                    newDict['office.name']="County Commissioner "+councilor_soup.find_all('span', {'id': 'pagetitle'})[0].get_text().encode('utf-8').split('\xe2\x80\x93')[1].strip()
                    newDict['electoral.district']= "Dallas County Council "+councilor_soup.find_all('span', {'id': 'pagetitle'})[0].get_text().encode('utf-8').split('\xe2\x80\x93')[1].strip()
                dictList.append(newDict)
    return dictList


get_councilor_data()


for dictionary in dictList:
    dictionary['state'] = 'TX'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
dallas_county_board_file = open('dallas_county_board.csv','wb')
csvwriter = csv.DictWriter(dallas_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

dallas_county_board_file.close()
 
with open("dallas_county_board.csv", "r") as dallas_county_board_csv:
     dallas_county_board = dallas_county_board_csv.read()

#print dallas_county_board
