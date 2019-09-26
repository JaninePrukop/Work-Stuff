"""
Written by Janine Prukop

This takes a .csv file from a Zoom preview, finds the company websites, and writes a new .csv file with the found
websites and the other information with everything ready to run through the Builder and ordered to match the
template on the google drive.

This program requires CompLinksFromNames.csv, chomedriver.exe, and the input .csv to be in the directory with it.
"""

import csv
from CompLinksFromNames import URLFinder

csvName = input("Name of file to read IDs from: ") + '.csv'
outName = 'Build' + csvName
replace = input('Do you want to replace the existing URLs? (Y/N): ')

comments = []
compIds = []
compName = []
firstName = []
lastName = []
title = []
phone1 = []
phone2 = []
email = []
linkedIn = []
websites = []
industry = []
employeeSize = []
revenue = []
hqAddress = []
hqCity = []
hqState = []
zipCode = []
country = []
personID = []
personCity = []
personState = []
websites = []
ws = -1
pID = -1
jt = -1
pc = -1
ps = -1
cID = -1
cn = -1
hqc = -1
hqs = -1
zc = -1
c = -1
ind = -1
web = -1

header = ['Comments', 'Company', 'Full Name', 'First Name', 'Last Name', 'Title', 'Phone 1', 'Phone 2'
          , 'Email', 'Person City', 'Person State', 'Website', 'Industry', 'Employee Size', 'Revenue', 'LinkedIn URL',
          'HQ Address', 'HQ City', 'HQ State', 'Zip', 'Country']

with open(csvName, encoding='utf-8', errors='ignore') as inFile:
    dialect = csv.excel
    readCSV = csv.reader(inFile, delimiter=',')
    inHeader = next(readCSV)
    for i in range(len(inHeader)):
        print(inHeader[i].lower())
        if inHeader[i] == 'Zoom Individual ID':
            pID = i
        elif inHeader[i] == 'Job title':
            jt = i
        elif inHeader[i] == 'Person City':
            pc = i
        elif inHeader[i] == 'Person State':
            ps = i
        elif inHeader[i] == 'Zoom Company ID':
            cID = i
        elif inHeader[i] == 'Company name':
            cn = i
        elif inHeader[i] == 'Company City':
            hqc = i
        elif inHeader[i] == 'Company State':
            hqs = i
        elif inHeader[i] == 'Company ZIP/Postal code':
            zc = i
        elif inHeader[i] == 'Company Country':
            c = i
        elif inHeader[i] == 'Industry label':
            ind = i
        elif inHeader[i] == 'Website':
            web = i

    for row in readCSV:
        # print(row)
        personID.append(row[pID])
        title.append(row[jt])
        personCity.append(row[pc])
        personState.append(row[ps])
        compIds.append(row[cID])
        compName.append(row[cn])
        hqCity.append(row[hqc])
        hqState.append(row[hqs])
        zipCode.append(row[zc])
        country.append(row[c])
        industry.append(row[ind])
        if web != -1 and (replace == 'n' or replace == 'N'):
            websites.append(row[web])
        else:
            websites.append('')
inFile.close()

urls = URLFinder(compName, websites)

with open(outName, 'a', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    writer.writerows([header])
    for i in range(1, len(personID)):
        output = []
        output.append(personID[i])
        output.append(compName[i])
        output.append('')
        output.append('')
        output.append('')
        output.append(title[i])
        output.append('')
        output.append('')
        output.append('')
        output.append(personCity[i])
        output.append(personState[i])
        output.append(websites[i])
        output.append(industry[i])
        output.append('')
        output.append('')
        output.append('')
        output.append('')
        output.append(hqCity[i])
        output.append(hqState[i])
        output.append(zipCode[i])
        output.append(country[i])
        writer.writerows([output])
out_file.close()

