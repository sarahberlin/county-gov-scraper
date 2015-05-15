import requests
import bs4
import csv
from csv import DictWriter
import urllib, urllib2

root_url = 'http://www.countyofriverside.us/AbouttheCounty/SupervisorsandElectedOfficials.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#scrapes all government officials
def get_govt_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        info = soup.find_all('div', {'id':'dnn_ctr574_ContentPane'})[0].get_text().encode('utf-8').split('\n')[6:11] + soup.find_all('div', {'id':'dnn_ctr574_ContentPane'})[0].get_text().encode('utf-8').split('\n')[12:17]
        for x in range (0,10):
            newDict = {}
            if x == 8:
                newDict['official.name']= 'Stanley Sniff'
                newDict['office.name']= info[x]
            else:
                newDict['office.name']= info[x].split(' - ')[0]
                newDict['official.name']= info[x].split(' - ')[1]
            if "District" in newDict['office.name'] and "Attorney" not in newDict['office.name']:
                newDict['office.name'] = "Supervisor "+ newDict['office.name'] 
                bossite= [a.attrs.get('href') for a in soup.select('a[href^=http://www.countyofriverside.us/AbouttheCounty/BoardofSupervisors]')][0]
                bossoup= bs4.BeautifulSoup((requests.get(bossite)).text)
                newDict['website'] = [a.attrs.get('href') for a in bossoup.select('a[href^=http://www.rivco]')][x].encode('utf-8')
                newDict['email'] = [a.attrs.get('href') for a in bossoup.select('a[href^=mailto]')][x].encode('utf-8').replace('mailto:', '')
                newDict['address'] = '4080 Lemon Street - 5th Floor Riverside, California 92501'
                newDict['phone'] = '(951) 955-10{0}0'.format(info[x].split(' - ')[0][-1])
                newDict['electoral.district'] = "Riverside County Council " +info[x].split(' - ')[0]
            elif "Assessor" in newDict['office.name']:
                newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^http://www.asrc]')][0]
                newDict['electoral.district']= 'Riverside County'
            elif 'Auditor' in newDict['office.name']:   
                newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^http://www.aud]')][0]
                newDict['electoral.district']= 'Riverside County'
            elif 'District' in newDict['office.name']:   
                newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^http://www.rivcoda]')][0]
                newDict['electoral.district']= 'Riverside County'
            elif 'Sheriff' in newDict['office.name']:   
                newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^http://www.riversidesheriff]')][0]
                newDict['electoral.district']= 'Riverside County'
            elif 'Treasurer' in newDict['office.name']:   
                newDict['website'] = [a.attrs.get('href') for a in soup.select('a[href^http://www.countytreasurer]')][0]
                newDict['electoral.district']= 'Riverside County'
            dictList.append(newDict)
    return dictList

get_govt_data()


#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
riverside_county_board_file = open('riverside_county_board.csv','wb')
csvwriter = csv.DictWriter(riverside_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

riverside_county_board_file.close()
 
with open("riverside_county_board.csv", "r") as riverside_county_board_csv:
     riverside_county_board = riverside_county_board_csv.read()

#print riverside_county_board
