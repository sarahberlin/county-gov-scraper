import brewery
from brewery import ds
import sys
import csv
from csv import DictWriter
from csv import DictReader
import os
import datetime

#establishes today's date, which will be included in the file name
today = datetime.date.today()

path = '/Users/sarahberlin/Dropbox/GovProj Scraping/County_scripts'
os.listdir(path)

#run all of the python files in this directory so that the csv's are up to date
for py_file in os.listdir(path):
    if ".py" in py_file and 'merged' not in py_file:
        os.system("python {0}".format(py_file))
        print py_file #prints name of file after it's been run, which keeps track of where the script is

#get names of csv files so they can be merged
csv_files = []
for csv_file in os.listdir(path):
    if ".csv" in csv_file and 'merged' not in csv_file:
        csv_files.append(csv_file)

sources = []

for csv_file in csv_files:
    newDict = {}
    newDict['file'] = csv_file
    newDict['fieldnames'] = ['state','electoral.district','office.name','official.name', 'address','phone','website', 'email', 'facebook', 'twitter',]
    sources.append(newDict)


# creates list of all fields and adds filename to store information
#all_fields = brewery.FieldList(["file"])
all_fields = []
#all_fields.append('file')
for source in sources:
    for field in source["fieldnames"]:
        if field not in all_fields:
            all_fields.append(field)


#gets each row in each csv file and puts it in a list
all_rows = []
for source in sources:
    for row in csv.DictReader(open(source['file'], 'rb')):
        all_rows.append(row)

#for row in all_rows:
#    for source in sources:
#        row['file'] = source['file']

#tries to write each of those rows to the new csv and then close the csv
fieldnames = all_fields
county_merged_file = open('county_merged_file-{0}.csv'.format(today),'wb')
csvwriter = csv.DictWriter(county_merged_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in all_rows:
    csvwriter.writerow(row)

county_merged_file.close()


with open('county_merged_file-{0}.csv'.format(today), "r") as merged_file_csv:
     county_merged_file = merged_file_csv.read()

#print county_merged_file
print "Scraping complete"



#these are all of the counties that should be in the merged file. this list will be used to check future iterations of the file against

master_counties = ['Bexar', 'Broward', 'Clark', 'Cook', 'Dallas', 'Harris', 'King', 'Los Angeles', 'Maricopa', 'Miami-Dade', 'Orange', 'Riverside', 'San Bernardino', 'San Diego', 'Santa Clara', 'Tarrant', 'Queens', 'Brooklyn', 'Wayne', 'Manhattan', 'Alameda', 'Suffolk']


#these are all of the counties in the current version of the file
counties_in_file= []
for row in csv.DictReader(open('county_merged_file-{0}.csv'.format(today), 'r')):
    if row['electoral.district'].split(' County')[0] not in counties_in_file:
        counties_in_file.append(row['electoral.district'].split(' County')[0])

#print counties_in_file

#check current file against master file
count = 0
#displays message if we are missing a county
for county in master_counties:
    if county not in counties_in_file:
        print "We are missing " + county + " County"
    else:
        count += 1
#displays message if we have all the counties
if count == len(master_counties):
    print "All the counties that should be in the file are in the file"





