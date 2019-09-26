"""
Written by Janine Prukop

Required headers (order and capitalization do not matter):
    comments, company, full name, first name, last name, title, phone 1, phone 2, email, person city, person state,
    website, industry, employee size, revenue, linkedin url, hq address, hq city, hq state, zip, country
"""

import csv
import sys
from EmailBouncer import checker
from LIFindPerson import linkedIn
from LIVerifyer import verifier

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
linkedResult = []

emailResults = []

with open(infile, 'r') as in_file:
    count = 0
    readCSV = csv.reader(in_file, delimiter=',')
    em = -1
    nm = -1
    t = -1
    header = next(readCSV)
    emailResults.append('Email result')
    linkedResult.append('LinkedIn verifier')
    # print(header)
    for i in range(len(header)):
        if header[i].lower().strip() == 'comments':
            cm = i
            comments.append(header[i])
        elif header[i].lower().strip() == 'company':
            cp = i
            company.append(header[i])
        elif header[i].lower().strip() == 'full name':
            nm = i
            names.append(header[i])
        elif header[i].lower().strip() == 'first name':
            fn = i
            firstName.append(header[i])
        elif header[i].lower().strip() == 'last name':
            ln = i
            lastName.append(header[i])
        elif header[i].lower().strip() == 'title':
            t = i
            titles.append(header[i])
        elif header[i].lower().strip() == 'phone 1':
            p1 = i
            phone1.append(header[i])
        elif header[i].lower().strip() == 'phone 2':
            p2 = i
            phone2.append(header[i])
        elif header[i].lower().strip() == 'email':
            em = i
            emails.append(header[i])
        elif header[i].lower().strip() == 'person city':
            pc = i
            pCity.append(header[i])
        elif header[i].lower().strip() == 'person state':
            ps = i
            pState.append(header[i])
        elif header[i].lower().strip() == 'website':
            web = i
            website.append(header[i])
        elif header[i].lower().strip() == 'industry':
            ind = i
            industry.append(header[i])
        elif header[i].lower().strip() == 'employee size':
            es = i
            size.append(header[i])
        elif header[i].lower().strip() == 'revenue':
            rev = i
            revenue.append(header[i])
        elif header[i].lower().strip() == 'linkedin url':
            url = i
            liURL.append(header[i])
        elif header[i].lower().strip() == 'hq address':
            hqa = i
            hqAddress.append(header[i])
        elif header[i].lower().strip() == 'hq city':
            hqc = i
            hqCity.append(header[i])
        elif header[i].lower().strip() == 'hq state':
            hqs = i
            hqState.append(header[i])
        elif header[i].lower().strip() == 'zip':
            z = i
            hqZip.append(header[i])
        elif header[i].lower().strip() == 'country':
            c = i
            country.append(header[i])
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
    if names[k] == '':
        continue
    if firstName[k] == '':
        temp = names[k].split()
        # print(temp)
        firstName[k] = temp[0]
        if len(temp) > 1:
            lastName[k] = temp[1]

if runs < 1:
    print("You need to check at least once.")
    sys.exit()
emailResults = checker(emails, runs)

liURL = linkedIn(names, company, linkedLogIn, linkedPass)
# print(liURL)

linkedResult = verifier(names, liURL, company, linkedLogIn, linkedPass)

with open(outfile, 'a', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    for i in range(len(company)):
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
        output.append(linkedResult[i])
        writer.writerows([output])
out_file.close()
