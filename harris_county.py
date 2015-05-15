import requests
import bs4
import csv
from csv import DictWriter 
import urllib, urllib2

root_url = 'http://www.harriscountytx.gov/electedofficials.aspx'

#master list of all the dictionaries containing officials' info
dictList = []

#checks that a given url works and doesn't return a 404 error
def checkURL(x):
    try:
        code = urllib2.urlopen(x).code
    except:
        code = 404
    return code

#get page urls of all the commissioners and other officials
def get_data():
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        response = requests.get(root_url)
        soup = bs4.BeautifulSoup(response.text) 
        for x in range(0, 24):
            if x%2 == 0:
                newDict = {}
                newDict['official.name'] = soup.select('a.content_body')[x+1].get_text().encode('utf-8')
                newDict['address'] = '1001 Preston, Houston, Texas 77002'
                newDict['phone'] = '(713) 755-5000'
                if 'http' not in [a.attrs.get('href') for a in soup.select('a.content_body')][x]:
                        newDict['website'] = ('http://www.harriscountytx.gov/'+[a.attrs.get('href') for a in soup.select('a.content_body')][x])
                else:
                        newDict['website'] =  [a.attrs.get('href') for a in soup.select('a.content_body')][x]
                if "Precinct" in soup.select('a.content_body')[x].get_text():
                    newDict['office.name'] = "County Commissioner "+ soup.select('a.content_body')[x].get_text().encode('utf-8')
                    newDict['electoral.district'] = "Harris County Council "+  soup.select('a.content_body')[x].get_text().encode('utf-8')
                    dictList.append(newDict)
                else:
                    newDict['office.name'] = soup.select('a.content_body')[x].get_text().encode('utf-8')
                    newDict['electoral.district'] = "Harris County".encode('utf-8')
                    dictList.append(newDict)
    return dictList 

get_data()


#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
harris_county_officials_file = open('harris_county_officials.csv','wb')
csvwriter = csv.DictWriter(harris_county_officials_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

harris_county_officials_file.close()
 
with open("harris_county_officials.csv", "r") as harris_county_officials_csv:
     harris_county_officials = harris_county_officials_csv.read()

#print harris_county_officials

