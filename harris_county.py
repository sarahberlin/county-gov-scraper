import requests
import bs4
import csv
from csv import DictWriter 


root_url = 'http://www.harriscountytx.gov/electedofficials.aspx'
dictList = []

#get page urls of all the councilors
def get_data():
    response = requests.get(root_url)
    soup = bs4.BeautifulSoup(response.text) 
    for x in range(0, 24):
        if x%2 == 0:
            newDict = {}
            newDict['official.name'] = soup.select('a.content_body')[x+1].get_text()
            if 'http' not in [a.attrs.get('href') for a in soup.select('a.content_body')][x]:
                    newDict['website'] = ('http://www.harriscountytx.gov/'+[a.attrs.get('href') for a in soup.select('a.content_body')][x])
            else:
                    newDict['website'] =  [a.attrs.get('href') for a in soup.select('a.content_body')][x]
            if "Precinct" in soup.select('a.content_body')[x].get_text():
                newDict['office.name'] = "County Commissioner "+ soup.select('a.content_body')[x].get_text()
                newDict['electoral.district'] = "Harris County Council "+  soup.select('a.content_body')[x].get_text()
            else:
                newDict['office.name'] = soup.select('a.content_body')[x].get_text()
                newDict['electoral.district'] = "Harris County" 
            newDict['address'] = '1001 Preston, Houston, Texas 77002'
            newDict['phone'] = '(713) 755-5000'
        dictList.append(newDict)  
        print dictList 

get_data()

temp_List = []
for x in range(0, 24):
    if x %2 == 0:
        temp_List.append(dictList[x])

dictList = temp_List


#creates csv
fieldnames = ['official.name','office.name','electoral.district','website', 'address', 'phone']
harris_county_officials_file = open('harris_county_officials.csv','wb')
csvwriter = csv.DictWriter(harris_county_officials_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in dictList:
    csvwriter.writerow(row)

harris_county_officials_file.close()
 
with open("harris_county_officials.csv", "r") as harris_county_officials_csv:
     harris_county_officials = harris_county_officials_csv.read()

print harris_county_officials

