import requests
import bs4
import csv
from csv import DictWriter

root_url = 'https://www.maricopa.gov/MenuDetail.aspx?Menu=deptView&a=dept1'
response = requests.get(root_url)
soup = bs4.BeautifulSoup(response.text)    


info = soup.select('table.SectionBody')[1].get_text().encode('utf-8').replace('\nAssessor', 'Assessor').split('\n\n\n\n\n\n\n')

info.pop(0)
info.pop(1)

links = []
for x in range(8,25):
    links.append([a.attrs.get('href') for a in soup.select('table.SectionBody a[href]')][x].encode('utf-8'))

links.pop(1)


dictList = []

def get_govt_data():
    for x in range (0, 15):
        newDict = {}
        for item in info:
            newDict['office.name']= info[x].split(' - ')[0]
            newDict['official.name'] = info[x].split(' - ')[1].replace('\n\n\n', '')
            newDict['electoral.district'] = 'Maricopa County'
            if "BOS" in info[x].split(' - ')[0]:
                    newDict['office.name'] = 'County Supervisor District ' + info[x].split(' - ')[0].replace(' BOS', '')[-1]
                    newDict['electoral.district'] = 'Maricopa County Council District '+ info[x].split(' - ')[0].replace(' BOS', '')[-1]
                    newDict['website'] = 'https://www.maricopa.gov' + links[x]
                    newDict['address'] = '301 W. Jefferson, 10th Floor Phoenix, Arizona 85003'
                    contactpage = ('https://www.maricopa.gov' + links[x]).replace('/default.aspx', '') + '/contact.aspx'
                    contactsoup = bs4.BeautifulSoup((requests.get(contactpage)).text)
                    newDict['email'] = [a.attrs.get('href') for a in contactsoup.select('a[href^mailto]')][0].replace('mailto:', '')
                    newDict['phone'] = contactsoup.select('div.sixcol')[0].get_text().split('\n')[5].encode('utf-8').strip()
            else:
                if links[x] == '/clk_board/default.aspx':
                    newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
                elif links[x] == '//treasurer.maricopa.gov/Pages/LoadPage?page=Bio':
                    newDict['website'] = 'https://treasurer.maricopa.gov/Pages/LoadPage?page=Bio'
                elif links[x] == '/clk_board/default.aspx':
                    newDict['website'] = 'https://www.maricopa.gov/clk_board/default.aspx'
                elif links[x] == '/cao/':
                    newDict['website'] = 'https://www.maricopa.gov/cao/'
                elif links[x] == '/dcm/':
                    newDict['website'] = 'https://www.maricopa.gov/dcm/'
                else:
                    newDict['website'] = links[x]
        dictList.append(newDict)
    print dictList

get_govt_data()

#creates csv
fieldnames = ['official.name', 'office.name','electoral.district','address','phone','website', 'email']
maricopa_county_supervisors_file = open('maricopa_county_supervisors.csv','wb')
csvwriter = csv.DictWriter(maricopa_county_supervisors_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

maricopa_county_supervisors_file.close()
 
with open("maricopa_county_supervisors.csv", "r") as maricopa_county_supervisors_csv:
     maricopa_county_supervisors = maricopa_county_supervisors_csv.read()

print maricopa_county_supervisors

