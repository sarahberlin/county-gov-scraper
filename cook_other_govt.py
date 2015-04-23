import requests
import bs4
import csv
from csv import DictWriter 

dictList= []
def govtdata():
    govsites = ['http://www.cookcountyil.gov/joseph-berrios/', 'http://www.cookcountyclerkofcourt.org/', 'http://www.cookcountyclerk.com/Pages/default.aspx', 'http://www.cookcountysheriff.org/sheriffs_bio/sheriff_bio.html', 'http://www.statesattorney.org/', 'http://www.cookcountytreasurer.com/treasurersbiography.aspx']
    assessorDict = {}
    clerkofCourtDict = {}
    clerkDict = {}
    sheriffDict = {}
    SADict = {}
    treasurerDict = {}
    for url in govsites:
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
    print dictList

govtdata()












officials_root_url = 'http://www.cookcountyil.gov'
response = requests.get(officials_root_url)
soup = bs4.BeautifulSoup(response.text)
newDictList = []

def get_basic_data():
    for x in range(2,12):
        newDict = {}
        newDict['title_name'] = soup.select('li.menu-item-3250')[0].get_text().encode('utf-8').replace("\xe2\x80\x99", "'").split('\n')[x]
        newDict['website'] = [a.attrs.get('href') for a in soup.select('li.menu-item-3250 a[href^=http://www.cookcountyil.gov/]')][x-2]
        newDict['district'] = 'Cook County'
        newDictList.append(newDict)
    print newDictList
 


def get_officials_urls():
    response = requests.get(officials_root_url)
    soup = bs4.BeautifulSoup(response.text) 
    return [a.attrs.get('href') for a in soup.select('li.menu-item-3250 a[href^=http://www.cookcountyil.gov/]')][:10]


def get_official_data(official_page_url):
    official_data = {}
    response = requests.get(official_page_url)
    soup = bs4.BeautifulSoup(response.text)
    try:
        official_data['name'] = soup.select('h1')[0].get_text().encode('utf-8')
        official_data['district'] = "Cook County"
        official_data['office'] = soup.select('h3')[1].get_text().encode('utf-8').replace(":\n", ' ')
        official_data['website'] = official_page_url
        official_data['address'] = soup.select('div p')[0].get_text().encode('utf-8').split("Phone: ")[0].replace('\n', ' ').strip()
        official_data['email'] = ''
        official_data['phone'] = soup.select('div p')[0].get_text().encode('utf-8').split('\n')[2].replace("Phone: ", "")
    except:
        pass
    return official_data

officialsList = []

#run the functions together
officials_page_urls = get_officials_urls()
for official_page_url in officials_page_urls:
    officialsList.append(get_official_data(official_page_url)) 






##############