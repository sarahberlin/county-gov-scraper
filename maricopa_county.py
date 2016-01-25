import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2


root_url = 'https://www.maricopa.gov/MenuDetail.aspx?Menu=deptView&a=dept1'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error. STILL NEEDS TO BE INTEGRATED INTO THIS SCRIPT#
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#get urls for supervisors and adds them to a list
supervisor_websites = []
def get_supervisor_websites():
	soup = bs4.BeautifulSoup((requests.get(root_url)).text)
	for site in [a.attrs.get('href') for a in soup.select('table.SectionBody a[href]')]:
		if "/dist" in site:
			supervisor_websites.append('https://www.maricopa.gov' + site)
	return supervisor_websites

get_supervisor_websites()

#scrape each supverisor site to create a dictionary and then add to dictList
def scrape_supervisor_websites():
	for site in supervisor_websites:
		newDict = {}
		soup = bs4.BeautifulSoup((requests.get(site)).text)
		newDict['official.name'] = soup.select('div.welcome')[0].get_text().encode('utf-8').split("Maricopa ")[0]
		newDict['office.name'] = soup.select('div.welcome')[0].get_text().encode('utf-8').split("Maricopa ")[1].replace(',', '')
		newDict['electoral.district'] = "Maricopa County Council District " + soup.select('div.welcome')[0].get_text().encode('utf-8').split("Maricopa")[1].replace(',', '')[-1]
		newDict['address'] = '301 W. Jefferson, 10th Floor Phoenix, Arizona 85003'
		contactpage = site.replace('/default.aspx', '/') + 'contact.aspx'
		contactsoup = bs4.BeautifulSoup((requests.get(contactpage)).text)
		newDict['email'] = [a.attrs.get('href') for a in contactsoup.select('a[href^mailto]')][0].replace('mailto:', '')
		newDict['phone'] = contactsoup.select('div.sixcol')[0].get_text().split('\n')[5].encode('utf-8').strip()
		newDict['website'] = site
		dictList.append(newDict)
	return dictList

scrape_supervisor_websites()

#scrapes homepage to get names and offices for non-supervisor elected officials and then creates dictionary for each official and add to dictList

def scrape_govt_websites():
	govt_names_and_offices = []
	root_url = 'https://www.maricopa.gov/MenuDetail.aspx?Menu=deptView&a=dept1'
	soup = bs4.BeautifulSoup((requests.get(root_url)).text)
	templist = soup.select('table.SectionBody')[1].get_text().encode('utf-8').replace('\nAssessor', 'Assessor').replace('\n\n\n', '').split("\n")
	for official in templist:
	     if "Assessor" in official or "Clerk of the Board" in official or "Clerk of the Court" in official or "County Attorney" in official or "Recorder" in official or "Sheriff" in official or "Treasurer" in official:
	            govt_names_and_offices.append(official)
	for official in govt_names_and_offices:
		newDict = {}
		newDict['office.name'] = official.split(' - ')[0]
		newDict['official.name'] = official.split(' - ')[1]
		newDict['electoral.district'] = "Maricopa County"
		if newDict['office.name'] == 'Assessor':
			newDict['website'] = 'http://mcassessor.maricopa.gov/the-assessor/biography/'
		elif newDict['office.name'] == 'Clerk of the Board':
			newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
		elif newDict['office.name'] == 'Clerk of the Court':
			newDict['website'] = 'http://clerkofcourt.maricopa.gov/clkbio.asp'
		elif newDict['office.name'] == 'County Attorney':
			newDict['website'] = 'http://www.maricopacountyattorney.org/'
		elif newDict['office.name'] == 'Recorder':
			newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
		elif newDict['office.name'] == 'Sheriff':
			newDict['website'] = 'http://www.mcso.org/Default.aspx'
		elif newDict['office.name'] == 'Treasurer':
			newDict['website'] = 'http://recorder.maricopa.gov/'
		dictList.append(newDict)
	return dictList

scrape_govt_websites()

#adds state
for dictionary in dictList:
    dictionary['state'] = 'AZ'

#creates csv
fieldnames = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter']
maricopa_county_supervisors_file = open('maricopa_county_supervisors.csv','wb')
csvwriter = csv.DictWriter(maricopa_county_supervisors_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

maricopa_county_supervisors_file.close()
 
with open("maricopa_county_supervisors.csv", "r") as maricopa_county_supervisors_csv:
     maricopa_county_supervisors = maricopa_county_supervisors_csv.read()

#print maricopa_county_supervisors

