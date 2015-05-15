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

#scrapes commissioners
def get_councilor_data():
    root_url = 'http://ocgov.com/gov/bos/'
    if checkURL(root_url) == 404:
        print '404 error. Check the url for {0}'.format(root_url)
    else:
        soup = bs4.BeautifulSoup((requests.get(root_url)).text)
        for x in range(0,5):
            newDict = {}
            newDict['phone'] = soup.select('table.table1 tr')[x].get_text().encode('utf-8').split('(')[1].split('0')[0].replace('714', '(714') +'0'
            newDict['official.name'] =soup.select('table.table1 tr')[x].get_text().encode('utf-8').replace('\xc3\xa2\xc2\x80\xc2\x93', '').replace('\xc3\x82\xc2\xa0', '').split(',')[0].replace('Board Chairman', '').replace('Vice Chair', '').strip()
            newDict['office.name'] = "Supervisor " + soup.select('table.table1 tr')[x].get_text().encode('utf-8').replace('\xc3\xa2\xc2\x80\xc2\x93', '').replace('\xc3\x82\xc2\xa0', '').split(',')[2].split('            ')[0].strip()
            newDict['electoral.district'] = "Orange County Council District " + soup.select('table.table1 tr')[x].get_text().encode('utf-8').replace('\xc3\xa2\xc2\x80\xc2\x93', '').replace('\xc3\x82\xc2\xa0', '').split(',')[2].split('            ')[0].strip()[0]
            newDict['website'] = 'http://ocgov.com/gov/bos/' + soup.select('table.table1 tr')[x].get_text().encode('utf-8').replace('\xc3\xa2\xc2\x80\xc2\x93', '').replace('\xc3\x82\xc2\xa0', '').split(',')[2].split('            ')[0].strip()[0]
            newDict['address'] = '333 W. Santa Ana Blvd., 5th Floor' 
            dictList.append(newDict)
    return dictList

get_councilor_data()


#scrapes non-commissioners
def govtdata():
    govsites = ['http://ocgov.com/gov/clerk/', 'http://ocgov.com/gov/assessor/', 'http://ocsd.org/divisions/office_of_the_sheriff', 'http://orangecountyda.org/office/ocda.asp', 'http://ocgov.com/gov/ttc/', 'http://ac.ocgov.com/']
    assessorDict = {}
    DADict = {}
    sheriffDict = {}
    treasurerDict = {}
    clerkDict = {}
    auditorDict = {}
    for url in govsites:
        if checkURL(url) == 404:
            print '404 error. Check the url for {0}'.format(url)
        else:
            soup = bs4.BeautifulSoup((requests.get(url)).text)
            if 'assessor' in url:
                assessorDict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').split('-')[2].strip()
                assessorDict['office.name'] = "Assessor"
                assessorDict['website'] = url
                assessorDict['electoral.district'] = "Orange County"
                dictList.append(assessorDict)
            elif 'orangecountyda' in url:
                DADict['official.name'] = soup.select('h1')[0].get_text().encode('utf-8')
                DADict['office.name'] = 'District Attorney'
                DADict['website'] = "http://orangecountyda.org/"
                DADict['electoral.district'] = "Orange County"
                dictList.append(DADict)
            elif 'ttc' in url:
                treasurerDict['official.name'] = soup.select('h1')[1].get_text().encode('utf-8').split(',')[0]
                treasurerDict['office.name'] = "Treasurer - Tax Collector"
                treasurerDict['website'] = url
                treasurerDict['electoral.district'] = "Orange County"
                dictList.append(treasurerDict)
            elif 'sheriff' in url:
                sheriffDict['official.name'] = soup.select('p strong')[0].get_text().encode('utf-8').split('            ')[1]
                sheriffDict['office.name'] = "Sheriff-Coroner"
                sheriffDict['website'] = 'http://ocsd.org/'
                sheriffDict['electoral.district'] = "Orange County"
                dictList.append(sheriffDict)
            elif 'clerk' in url:
                clerkDict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').split('-')[2].strip()
                clerkDict['office.name'] = "Clerk-Recorder"
                clerkDict['website'] = url
                clerkDict['electoral.district'] = "Orange County"
            elif 'ac.ocgov' in url:
                auditorDict['official.name'] = soup.select('title')[0].get_text().encode('utf-8').split('-')[2].strip()
                auditorDict['office.name'] = "Auditor-Controller"
                auditorDict['website'] = url
                auditorDict['electoral.district'] = "Orange County"
                dictList.append(auditorDict)
    return dictList

govtdata()


#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email', 'facebook', 'twitter']
orange_county_board_file = open('orange_county_board.csv','wb')
csvwriter = csv.DictWriter(orange_county_board_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

orange_county_board_file.close()
 
with open("orange_county_board.csv", "r") as orange_county_board_csv:
     orange_county_board = orange_county_board_csv.read()

#print orange_county_board
