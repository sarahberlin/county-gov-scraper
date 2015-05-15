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
    root_url = 'http://www.browardsoe.org/'
    index_url = root_url +'ElectedOfficials.aspx?s=79'
    if checkURL(index_url) == 404:
        print '404 error. Check the url.'
    else:
        soup = bs4.BeautifulSoup((requests.get(index_url)).text)
        clerkDict = {}
        sheriffDict = {}
        propertyDict = {}
        supervisorDict = {}
        for x in range (0, 180):
            office = soup.select('tr td.ElectedOfficials_Office')[x].get_text().encode('utf-8').replace("*", '')
            official = soup.select('td.ElectedOfficials_ElectedOfficial a')[x].text.encode('utf-8')
            website = [a.attrs.get('href') for a in soup.select('td.ElectedOfficials_ElectedOfficial a[href]')][x]
            if "Clerk of the Circuit Court" in office:
                clerkDict['office.name']= office
                clerkDict['official.name'] = official
                clerkDict['website'] = root_url +website
                clerkDict['electoral.district'] = "Broward County"
                dictList.append(clerkDict)
            elif "Sheriff" in office:
                sheriffDict['office.name']= office
                sheriffDict['official.name'] = official
                sheriffDict['website'] = root_url +website
                sheriffDict['electoral.district'] = "Broward County"
                dictList.append(sheriffDict)
            elif "Property Appraiser" in office:
                propertyDict['office.name']= office
                propertyDict['official.name'] = official
                propertyDict['website'] = root_url +website
                propertyDict['electoral.district'] = "Broward County"
                dictList.append(propertyDict)
            elif "Supervisor of Elections" in office:
                supervisorDict['office.name']= office
                supervisorDict['official.name'] = official
                supervisorDict['website'] = root_url +website
                supervisorDict['electoral.district'] = "Broward County"
                dictList.append(supervisorDict)
    return dictList

get_govt_data()

#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
broward_county_board_file = open('broward_county_board.csv','wb')
csvwriter = csv.DictWriter(broward_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

broward_county_board_file.close()
 
with open("broward_county_board.csv", "r") as broward_county_board_csv:
     broward_county_board = broward_county_board_csv.read()

#print broward_county_board
