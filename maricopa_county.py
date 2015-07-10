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

#gets names and offices for all officials and adds them to list
names_and_offices = []
def get_name_and_office():
    root_url = 'https://www.maricopa.gov/MenuDetail.aspx?Menu=deptView&a=dept1'
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for official in soup.select('table.SectionBody')[1].get_text().encode('utf-8').replace('\nAssessor', 'Assessor').split('\n\n\n\n\n\n\n'):
            names_and_offices.append(official) 
        names_and_offices.pop(0)
        names_and_offices.pop(1)
    return names_and_offices

get_name_and_office()

          
#gets websites for all officials and adds them to a list
websites = []
def get_websites():
    root_url = 'https://www.maricopa.gov/MenuDetail.aspx?Menu=deptView&a=dept1'
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(10,26):
            websites.append([a.attrs.get('href') for a in soup.select('table.SectionBody a[href]')][x].encode('utf-8'))
        websites.pop(1)
    return websites

 
get_websites()
#formats and adds to dictionaries, scrapes contact pages for supervisors, then adds to dictList
def get_govt_data():
    for x in range (0, 15):
        newDict = {}
        for official in names_and_offices:
            newDict['office.name']= names_and_offices[x].split(' - ')[0]
            newDict['official.name'] = names_and_offices[x].split(' - ')[1].replace('\n\n\n', '')
            newDict['electoral.district'] = 'Maricopa County'
            if "BOS" in names_and_offices[x].split(' - ')[0]:
                    newDict['office.name'] = 'County Supervisor District ' + names_and_offices[x].split(' - ')[0].replace(' BOS', '')[-1]
                    newDict['electoral.district'] = 'Maricopa County Council District '+ names_and_offices[x].split(' - ')[0].replace(' BOS', '')[-1]
                    newDict['website'] = 'https://www.maricopa.gov' + websites[x]
                    newDict['address'] = '301 W. Jefferson, 10th Floor Phoenix, Arizona 85003'
                    contactpage = ('https://www.maricopa.gov' + websites[x]).replace('/default.aspx', '/') + 'contact.aspx'
                    if checkURL(contactpage) == 404:
                        print '404 error. Check the url for {0}'.format(contactpage)
                    else:
                        contactsoup = bs4.BeautifulSoup((requests.get(contactpage)).text)
                        newDict['email'] = [a.attrs.get('href') for a in contactsoup.select('a[href^mailto]')][0].replace('mailto:', '')
                        newDict['phone'] = contactsoup.select('div.sixcol')[0].get_text().split('\n')[5].encode('utf-8').strip()
            else:
                if websites[x] == '/clk_board/default.aspx':
                    newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
                elif websites[x] == '//treasurer.maricopa.gov/Pages/LoadPage?page=Bio':
                    newDict['website'] = 'https://treasurer.maricopa.gov/Pages/LoadPage?page=Bio'
                elif websites[x] == '/clk_board/default.aspx':
                    newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
                elif websites[x] == '/cao/':
                    newDict['website'] = 'https://www.maricopa.gov/cao/'
                elif websites[x] == '/dcm/':
                    newDict['website'] = 'https://www.maricopa.gov/dcm/'
                else:
                    newDict['website'] = websites[x]
        dictList.append(newDict)
    return dictList

get_govt_data()


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

