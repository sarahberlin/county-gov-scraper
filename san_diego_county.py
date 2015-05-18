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

#scrapes supervisor sites
def get_councilor_data():
    root_url = 'http://www.sandiegocounty.gov/content/sdc/general/bos.html'
    response = requests.get(root_url)
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup(response.text)
        for x in range (5,10):
            newDict = {}
            newDict['electoral.district'] = "San Diego County Council " + soup.select('tbody td')[x].get_text().encode('utf-8').split("\n")[1]
            newDict['office.name'] = "San Diego County Supervisor " + soup.select('tbody td')[x].get_text().encode('utf-8').split("\n")[1]
            newDict['official.name'] = soup.select('tbody td')[x].get_text().encode('utf-8').split("\n")[0]
            newDict['website'] = [a.attrs.get('href') for a in soup.select('tbody td a[href]')][x-5]
            newDict['phone'] = '(619) 531-5430'
            dictList.append(newDict)
    return dictList

get_councilor_data()

#scrapes other officials' sites
def govtdata():
    govsites = ['https://arcc.sdcounty.ca.gov/Pages/default.aspx', 'http://www.sdcda.org/office/meet-da.html', 'http://www.sdsheriff.net/', 'http://www.sdtreastax.com/']
    assessorDict = {}
    DADict = {}
    sheriffDict = {}
    treasurerDict = {}
    for url in govsites:
        if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
        else:
            soup = bs4.BeautifulSoup((requests.get(url)).text)
            if 'arcc' in url:
                assessorDict['official.name'] = soup.find('span', {'id': 'ejdj-title'}).get_text().encode('utf-8')
                assessorDict['office.name'] = "Assessor"
                assessorDict['website'] = url
                assessorDict['electoral.district'] = "San Diego County"
                dictList.append(assessorDict)
            elif 'sdcda' in url:
                DADict['official.name'] = soup.select('h2')[4].get_text().encode('utf-8')
                DADict['office.name'] = 'District Attorney'
                DADict['website'] = "http://www.sdcda.org/"
                DADict['electoral.district'] = "San Diego County"
                dictList.append(DADict)
            elif 'sdtreas' in url:
                treasurerDict['official.name'] = soup.find('div', {'id': 'ttc-footer-address'}).get_text().encode('utf-8').replace("\n\xc2\xa0\n",'').split(" |")[0].title()
                treasurerDict['office.name'] = "Treasurer"
                treasurerDict['website'] = url
                treasurerDict['electoral.district'] = "San Diego County"
                dictList.append(treasurerDict)
            elif 'sheriff' in url:
                sheriffDict['official.name'] = soup.select('h2')[0].get_text().encode('utf-8').replace('A Message From Sheriff ', '')
                sheriffDict['office.name'] = "Sheriff"
                sheriffDict['website'] = url
                sheriffDict['electoral.district'] = "San Diego County"
                dictList.append(sheriffDict)
    return dictList

govtdata()


#creates csv
fieldnames = ['official.name','electoral.district', 'office.name','phone','website']
sandiego_county_board_file = open('sandiego_county_board.csv','wb')
csvwriter = csv.DictWriter(sandiego_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

sandiego_county_board_file.close()
 
with open("sandiego_county_board.csv", "r") as sandiego_county_board_csv:
     sandiego_county_board = sandiego_county_board_csv.read()

#print sandiego_county_board

