from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time
import csv

outputFile = 'All the Hs first pass.csv'
header = ['Company', 'Name', 'Phone Number']
with open(outputFile, 'a') as out:
    writer = csv.writer(out, dialect='excel')
    writer.writerow(header)

startingURL = 'https://connectedinvestors.com/company///G'
driver = webdriver.Chrome()
companies = []
names = []
phoneNums = []
fullInfo = []
compsNeeded = []
numOfPages = 5
count = 0

driver.get(startingURL)

temphtml = driver.page_source
startSoup = BeautifulSoup(temphtml, 'lxml')

listLLC = startSoup.find_all('span')

# print(listLLC)
for i in range(len(listLLC)):
    print('Span #', i, 'contains: ', listLLC[i])
print(len(listLLC))

while count < numOfPages:
    for i in range(36, len(listLLC)):
        print('Company number ', i - 35, 'Page #: ', count + 1)
        companies.append(listLLC[i].text)
        # print(companies[-1])
        try: driver.find_element_by_partial_link_text(companies[-1]).click()
        except: print('oops')
        time.sleep(2)
        temphtml = driver.page_source
        tempSoup = BeautifulSoup(temphtml, 'lxml')
        team = tempSoup.find_all('section', {'class': "sub fade-light clear search"})
        for item in team:
            #print(item)
            # print('first a tag: ', item.a.text)
            person = item.find('h2', {'class': "col-sm-12 discussion-title section-heading"})
            phoneNumber = item.find_all('span', {'class': "clickPhone btn btn-link btn-small"})
            if len(phoneNumber) == 0:
                phoneNumber = ''
            else:
                phoneNumber = str(phoneNumber[0])
                phoneNumber = phoneNumber.replace('<span class="clickPhone btn btn-link btn-small" data-phone="', '')
                phoneNumber = phoneNumber.replace('" title="Show Phone"><i class="fa fa-phone small"></i>', '')
                phoneNumber = phoneNumber.replace('Show phone</span>', '')
                # print(phoneNumber)
            fullInfo.append([companies[-1], person.a.text, phoneNumber])
            with open(outputFile, 'a') as out:
                writer = csv.writer(out, dialect='excel')
                writer.writerow(fullInfo[-1])
        if len(team) == 0:
            compsNeeded.append(companies[-1])
            with open('StillNeededH.csv', 'a') as out:
                writer = csv.writer(out, dialect='excel')
                writer.writerow(compsNeeded[-1])
        driver.get(startingURL)

        # print(fullInfo)
        # print(compsNeeded)
        time.sleep(2)
    driver.find_element_by_class_name('next_page').click()
    count += 1
    startingURL = 'https://connectedinvestors.com/company//' + str(count + 1) + '/H'

# print(companies)

driver.close()
