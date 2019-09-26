from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time
import csv
import re

start = 0
maxNum = 287
outputOne = 'NOEMAILSOutputAttending4-15.csv'
contacts = []
dncList = []
# header = ["Company", "First Name", "Last Name", "Title", '', '', "Phone Number", '', "Email", '', '', '', '', "Website",
#           "Address", "Industry"]
# contacts.append(header)
industry = 'Retailer/Tenant'

'''
with open(outputOne, 'a') as out:
    writer = csv.writer(out, dialect='excel')
    writer.writerow(header)
out.close()
'''

with open('DNC.csv', 'r') as dnc:
    reader = csv.reader(dnc)
    for row in reader:
        dncList.append(row[0])


# Using Chrome to access web
driver = webdriver.Chrome()

# Filters titles in US
driver.get('https://www.icsc.org/search?type=members&event_id=2019RECON&from=2016&sort=sort_by_last_name&perPage=288&\
query=&filter=business_types:Retailer%2FTenant:Food%20services,%20including%20restaurants%20and%20drinking%20establishme\
nts&fi\
lter=business_types:Retailer%2FTenant:Apparel,%20footwear%20and%20accessory%20stores&filter=business_types:Retailer%2FTe\
nant:Other%20categories%20and%20specialty%20stores,%20incl.%20pet%20stores%20and%20florists&filter=business_types:Retail\
er%2FTenant:Food%20and%20beverage%20stores,%20not%20including%20restaurants&filter=business_types:Retailer%2FTenant:Auto\
motive,%20including%20dealers,%20auto%20repair%20and%20gasoline%20stations&filter=business_types:Retailer%2FTenant:Drugs\
tores%20and%20cosmetics&filter=business_types:Retailer%2FTenant:General%20merchandise%20and%20department%20stores&filter\
=business_types:Retailer%2FTenant:Furniture%20and%20home%20furnishing%20stores&filter=business_types:Retailer%2FTenant:S\
porting%20goods,%20books,%20hobbies%20and%20music%20stores&filter=business_types:Retailer%2FTenant:Educational,%20health\
%20care%20and%20daycare%20services')


email = 'jschneuker@seguintexas.gov'
psswrd = 'EDCaccess1'

user = driver.find_element_by_name('_username')
sitePsswrd = driver.find_element_by_name('_password')

user.send_keys(email)
driver.implicitly_wait(1)
sitePsswrd.send_keys(psswrd)
sitePsswrd.send_keys(Keys.RETURN)

time.sleep(10)

counterEmail = 0
counterTotal = 0


html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

people = soup.find_all(href=re.compile('member/profile'))
print(int(len(people))/2)
'''
for person in people:
    print(person)
'''
for j in range(start, int(len(people)/2)):
    person = people[j]
    personal_contact = []
    broken = str(person).split()
    for i in range(len(broken)):
        broken[i] = broken[i].strip('-').strip('!').strip('<')
    fullname = broken[10]+' '+broken[11]

    try: driver.find_element_by_partial_link_text(fullname).click()
    except WebDriverException:
        print("can't click")
        continue
    time.sleep(7)
    temphtml = driver.page_source
    nameSoup = BeautifulSoup(temphtml, 'html.parser')

    comp = nameSoup.find_all('p', {'class': 'display6 accent p-0 m-0'})
    if len(comp) != 0:
        personal_contact.append(comp[0].text)
        if comp[0] in dncList:
            print('skipping')
            continue
    else:
        personal_contact.append('')

    personal_contact.append(broken[10])
    personal_contact.append(broken[11])

    title = nameSoup.find_all('p', {'class': 'display6 secondary p-0 m-0'})
    if len(title) != 0:
        personal_contact.append(title[0].text)
    else: personal_contact.append('')

    personal_contact.append('')
    personal_contact.append('')

    num = nameSoup.find_all(href=re.compile('tel:'))
    if len(num) != 0:
        personal_contact.append(num[0].text.strip('\n'))
    else:
        personal_contact.append('')

    personal_contact.append('')
    '''
    try:
        driver.find_element_by_partial_link_text('display email').click()
        time.sleep(20)
        temphtml = driver.page_source
        emailSoup = BeautifulSoup(temphtml, 'lxml')
        email = emailSoup.find_all(href=re.compile('.*@.*'))
        # print(email)
        if len(email) != 0:
            broken = str(email[0]).split()
            # print(broken)
            broke = broken[7].split('>')
            emailSplit = broke[1].split('<')
            personal_contact.append(emailSplit[0])
        counterEmail += 1
        print('Number of contacts with emails : ' + str(counterEmail))

    except NoSuchElementException:
        personal_contact.append('')
    '''
    personal_contact.append('')

    personal_contact.append('')
    personal_contact.append('')
    personal_contact.append('')
    personal_contact.append('')

    temphtml = driver.page_source
    newSoup = BeautifulSoup(temphtml, 'lxml')

    web = newSoup.find_all(href=re.compile('http://'))
    if len(web) != 0:
        personal_contact.append(web[0].text)
    else:
        personal_contact.append('')

    address = newSoup.find_all('span', {'class': 'secondary'})
    splitAddress = str(address[1]).split('<br/>')
    unsplitAddress = ''
    for i in range(len(splitAddress)):
        unsplitAddress = unsplitAddress + splitAddress[i]
    splitAddress = unsplitAddress.split('\t')
    if len(splitAddress) >= 40 :
        wholeAddress = splitAddress[10] + splitAddress[20] + splitAddress[40]
        splitAddress = wholeAddress.split('\n')
        unsplitAddress = ''
        for i in range(len(splitAddress)):
            unsplitAddress = unsplitAddress + splitAddress[i]
        personal_contact.append(unsplitAddress.strip('</span>'))
    else: personal_contact.append('Not Available')

    personal_contact.append(industry)

    with open(outputOne, 'a') as out:
        writer = csv.writer(out, dialect='excel')
        writer.writerow(personal_contact)
    out.close()

    contacts.append(personal_contact)
    counterTotal += 1
    print('Total number of contacts : ' + str(counterTotal))
    driver.back()
    time.sleep(5)
    #if counterEmail == maxNum:
    #    break


print(contacts)
with open('OutputAttending0.csv', 'w') as out:
    writer = csv.writer(out, dialect='excel')
    writer.writerows(contacts)
out.close()
