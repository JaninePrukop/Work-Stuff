"""
Written by Janine Prukop

This program requires chromedriver.exe, and the input .csv to be in the directory with it.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
from bs4 import BeautifulSoup
# pip install lxml

startURL = 'https://login.zoominfo.com/#/'
username = input('Zoom username: ')
password = input('Zoom password: ')
csvName = input("Name of file to read IDs from: ") + '.csv'
personURL = 'https://go.zoominfo.com/#/apps/search/person/results?personProfileId='
# start = int(input("What row are you starting on? "))

ids = []
names = []

with open(csvName) as inFile:
    readCSV = csv.reader(inFile, delimiter=',')
    com = -1
    nm = -1
    header = next(readCSV)

    for i in range(len(header)):
        if header[i].lower() == 'comments':
            com = i
        elif header[i].lower() == 'full name':
            nm = i

    for row in readCSV:
        personId = row[com]
        ids.append(personId)
        names.append(row[nm])

inFile.close()

driver = webdriver.Chrome()
driver.get(startURL)
time.sleep(4)
user = driver.find_element_by_id('username')
passwd = driver.find_element_by_id('password_required')
user.send_keys(username)
time.sleep(1)
passwd.send_keys(password)
passwd.send_keys(Keys.RETURN)

auth = input('Auth Code (input DONE if input to the browser): ')

if auth.lower() != 'done':
    passcode = driver.find_element_by_id('pinValue')
    passcode.send_keys(auth)

time.sleep(5)

# print(names)
# print(len(names))
if len(names) > 0:
    for i in range(0, len(names)):
        if names[i] == '':
            start = i
            break
else:
    start = 1
print(start)

count = 0
for i in range(start, len(ids)):
    targetURL = personURL + ids[i]
    count += 1
    print(targetURL)
    print('You are on view # ', count)
    driver.get(targetURL)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    bar = soup.find_all('div', {'class': ['filters-content']})
    while len(bar) != 0:
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        bar = soup.find_all('div', {'class': ['filters-content']})