import requests
import bs4
import csv
from csv import DictWriter 
import urllib, urllib2

root_url = 'http://www.cookcountyil.gov/board-of-commissioners/'

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
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        response = requests.get(root_url)
        soup = bs4.BeautifulSoup(response.text)    
        return [a.attrs.get('href') for a in soup.select('li.menu-item-3249 a[href^=http://www.cookcountyil.gov/]')][:17]

#get data from each individual councilor's page
def get_councilor_data(page_url):
    if checkURL(page_url) == 404:
        print '404 error. Check the url for {0}'.format(page_url)
        return
    else:
        councilor_data = {}
        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text)
        try:
            councilor_data['official.name'] = soup.select('h1')[0].get_text().encode('utf-8').split(' (')[0].replace('\xe2\x80\x9c', '"').replace('\xe2\x80\x9d', '"')
            councilor_data['electoral.district'] = "Cook County Council " + soup.select('h1')[0].get_text().encode('utf-8').split(' (')[1].replace(')', ' District')
            councilor_data['office.name'] = "County Commissioner " +soup.select('h1')[0].get_text().encode('utf-8').split(' (')[1].replace(')', ' District')
            councilor_data['website'] = page_url
            councilor_data['address'] = '118 N. Clark Street, Room 567 Chicago, IL 60602'
            if "@" in soup.find_all('p')[2].get_text().encode('utf-8').split(":")[2].replace('\xc2\xa0','').replace('\nWebsite', ''):
                councilor_data['email'] = soup.find_all('p')[2].get_text().encode('utf-8').split(":")[2].replace('\xc2\xa0','').replace('\nWebsite', '').strip()
            else:
                councilor_data['email'] = ""
            councilor_data['phone'] = soup.select('div p')[0].get_text().encode('utf-8').split("\n")[2].replace("Phone: ","").replace('Phone:\xc2\xa0','')
        except:
            pass
    return councilor_data

#run the functions together
page_urls = get_page_urls()
for page_url in page_urls:
    dictList.append(get_councilor_data(page_url))

#scrape other officials' sites
def govtdata():
    govsites = ['http://www.cookcountyil.gov/joseph-berrios/', 'http://www.cookcountyclerkofcourt.org/', 'http://www.cookcountyclerk.com/Pages/default.aspx', 'http://www.cookcountysheriff.org/sheriffs_bio/sheriff_bio.html', 'http://www.statesattorney.org/', 'http://www.cookcountytreasurer.com/treasurersbiography.aspx']
    assessorDict = {}
    clerkofCourtDict = {}
    clerkDict = {}
    sheriffDict = {}
    SADict = {}
    treasurerDict = {}
    for url in govsites:
        if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
        else:
            soup = bs4.BeautifulSoup((requests.get(url)).text)
            if url == 'http://www.cookcountyil.gov/joseph-berrios/':
                assessorDict['official.name'] = soup.select('h1')[0].get_text().encode('utf-8')
                assessorDict['office.name'] = "Assessor"
                assessorDict['website'] = url
                assessorDict['electoral.district'] = "Cook County"
                dictList.append(assessorDict)
            elif url == 'http://www.statesattorney.org/':
                SADict['official.name'] = soup.findAll('div', {'id':'after_header'})[0].get_text().encode('utf-8').replace('\xc2\xa0 ', '').replace('Home Search', '').split(',')[0].strip()
                SADict['office.name'] = "State's Attorney"
                SADict['website'] = url
                SADict['electoral.district'] = "Cook County"
                dictList.append(SADict)
            elif url == 'http://www.cookcountyclerkofcourt.org/':
                clerkofCourtDict['official.name'] = soup.findAll('div', {'align':'center'})[3].get_text().encode('utf-8').replace("Message From ", "")
                clerkofCourtDict['office.name'] = "Clerk of Court"
                clerkofCourtDict['website'] = url
                clerkofCourtDict['electoral.district'] = "Cook County"
                dictList.append(clerkofCourtDict)
            elif url == 'http://www.cookcountyclerk.com/Pages/default.aspx':
                clerkDict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').replace("Cook County Clerk's Office | ", "").replace("\r\n", "").replace("\t\t", "")
                clerkDict['office.name'] = "County Clerk"
                clerkDict['website'] = url
                clerkDict['electoral.district'] = "Cook County"
                dictList.append(clerkDict)
            elif url == 'http://www.cookcountytreasurer.com/treasurersbiography.aspx':
                treasurerDict['official.name'] = soup.findAll('div', {'class':'pagetitle'})[0].get_text().encode('utf-8').replace("\r\n", "").split(",")[0].strip()
                treasurerDict['office.name'] = "Treasurer"
                treasurerDict['website'] = "http://www.cookcountytreasurer.com/"
                treasurerDict['electoral.district'] = "Cook County"
                dictList.append(treasurerDict)
            elif url == 'http://www.cookcountysheriff.org/sheriffs_bio/sheriff_bio.html':
                sheriffDict['official.name'] = soup.select('h1')[0].get_text().encode('utf-8').replace("Sheriff ", "")
                sheriffDict['office.name'] = "Sheriff"
                sheriffDict['website'] = "http://www.cookcountysheriff.org"
                sheriffDict['electoral.district'] = "Cook County"
                dictList.append(sheriffDict)
    return dictList

govtdata()

for dictionary in dictList:
    dictionary['state'] = 'IL'


#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
cook_county_board_file = open('cook_county_board.csv','wb')
csvwriter = csv.DictWriter(cook_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

cook_county_board_file.close()
 
with open("cook_county_board.csv", "r") as cook_county_board_csv:
     cook_county_board = cook_county_board_csv.read()

#print cook_county_board

