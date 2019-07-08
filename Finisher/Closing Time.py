"""
Written by Janine Prukop
Created 6-27-2019
Last Edit: 7-2-2019
"""

import csv
import sys
from emailcheck import checker
from scraper import linkedIn

infile = input('What file are we reading from? ') + '.csv'
outfile = 'Finished_' + infile

comments = []
company = []
names = []
firstName = []
lastName = []
titles = []
phone1 = []
phone2 = []
emails = []
pCity = []
pState = []
website = []
industry = []
size = []
revenue = []
liURL = []
hqAddress = []
hqCity = []
hqState = []
hqZip = []
country = []

emailResults = []

with open(infile, 'r') as in_file:
    count = 0
    readCSV = csv.reader(in_file, delimiter=',')
    em = -1
    nm = -1
    t = -1
    header = next(readCSV)
    header.append('Email result')
    # print(header)
    for i in range(len(header)):
        if header[i].lower() == 'comments':
            cm = i
        elif header[i].lower() == 'company':
            cp = i
        elif header[i].lower() == 'full name':
            nm = i
        elif header[i].lower() == 'first name':
            fn = i
        elif header[i].lower() == 'last name':
            ln = i
        elif header[i].lower() == 'title':
            t = i
        elif header[i].lower() == 'phone 1':
            p1 = i
        elif header[i].lower() == 'phone 2':
            p2 = i
        elif header[i].lower() == 'email':
            em = i
        elif header[i].lower() == 'person city':
            pc = i
        elif header[i].lower() == 'person state':
            ps = i
        elif header[i].lower() == 'website':
            web = i
        elif header[i].lower() == 'industry':
            ind = i
        elif header[i].lower() == 'employee size':
            es = i
        elif header[i].lower() == 'revenue':
            rev = i
        elif header[i].lower() == 'linkedin url':
            url = i
        elif header[i].lower() == 'hq address':
            hqa = i
        elif header[i].lower() == 'hq city':
            hqc = i
        elif header[i].lower() == 'hq state':
            hqs = i
        elif header[i].lower() == 'zip':
            z = i
        elif header[i].lower() == 'country':
            c = i
    if (cm == -1 | cp == -1 | nm == -1 | fn == -1 | ln == -1 | t == -1 | p1 == -1 | p2 == -1 | em == -1 | pc == -1 |
    ps == -1 | web == -1 | ind == -1 | es == -1 | rev == -1 | url == -1 | hqa == -1 | hqc == -1 | hqs == -1 |
    z == -1 | c == -1):
        print("header for " + infile + "incomplete or in wrong format")
        exit()
    for row in readCSV:
        comments.append(row[cm])
        company.append(row[cp])
        names.append(row[nm])
        firstName.append(row[fn])
        lastName.append(row[ln])
        titles.append(row[t])
        phone1.append(row[p1])
        phone2.append(row[p2])
        emails.append(row[em])
        pCity.append(row[pc])
        pState.append(row[ps])
        website.append(row[web])
        industry.append(row[ind])
        size.append(row[es])
        revenue.append(row[rev])
        liURL.append(row[url])
        hqAddress.append(row[hqa])
        hqCity.append(row[hqc])
        hqState.append(row[hqs])
        hqZip.append(row[z])
        country.append(row[c])


linkedLogIn = input('What is your LinkedIn email?: ')
linkedPass = input('What is your LinkedIn password?: ')
runs = int(input("How many times do you want to check the emails? "))

for k in range(1, len(names)):
    if names[i] == '':
        continue
    if firstName[i] == '':
        temp = names[i].split()
        # print(temp)
        firstName[i] = temp[0]
        lastName[i] = temp[1]

if runs < 1:
    print("You need to check at least once.")
    sys.exit()
emailResults = checker(emails, runs)

liURL = linkedIn(names, titles, linkedLogIn, linkedPass)
# print(liURL)


with open(outfile, 'a', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    writer.writerows([header])
    for i in range(1, len(company)):
        output = []
        output.append(comments[i])
        output.append(company[i])
        output.append(names[i])
        output.append(firstName[i])
        output.append(lastName[i])
        output.append(titles[i])
        output.append(phone1[i])
        output.append(phone2[i])
        output.append(emails[i])
        output.append(pCity[i])
        output.append(pState[i])
        output.append(website[i])
        output.append(industry[i])
        output.append(size[i])
        output.append(revenue[i])
        output.append(liURL[i])
        output.append(hqAddress[i])
        output.append(hqCity[i])
        output.append(hqState[i])
        output.append(hqZip[i])
        output.append(country[i])
        output.append(emailResults[i])
        writer.writerows([output])
out_file.close()
