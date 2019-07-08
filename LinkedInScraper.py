"""
Written by Janine Prukop
Created 5-15-2019
Last Edit: 5-21-2019
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
import csv
import time
from selenium.webdriver.common.by import By
from tqdm import tqdm
from random import randint

StartUrl = 'http://www.linkedin.com/in/mikehazel'
inputName = input('File name: ') + '.csv'
outputName = 'output_' + inputName

names = []
firstName = []
lastName = []
title = []
comp = []
urls = []
count = 0
# compPos = int(input("Company column position: "))
firstPos = int(input("First name column position: "))
lastPos = int(input("Last name column position: "))
titlePos = int(input("Title column position: "))
outHeader = "Linked in Links found"

driver = webdriver.Chrome()

with open(inputName) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        names.append(str(row[firstPos]) + ' ' + str(row[lastPos]))
        firstName.append(row[firstPos])
        lastName.append(row[lastPos])
        title.append(row[titlePos])
        # comp.append(row[compPos])
        count += 1
print(count)

# Close the CSV file
csvfile.close()

urls.append("URL result")

driver.get(StartUrl)
time.sleep(5)

driver.find_element_by_partial_link_text('Sign in').click()
time.sleep(2)

emailLogin = driver.find_element_by_id('login-email')
emailLogin.send_keys('JANINE.PRUKOP@Gmail.com')

time.sleep(2)

passLogin = driver.find_element_by_id('login-password')
passLogin.send_keys('J9Fruitcup')
passLogin.send_keys(Keys.RETURN)

time.sleep(5)

head = list()

head.append(firstName[0])
head.append(lastName[0])
# head.append(comp[0])
head.append(title[0])
head.append(urls[0])

with open(outputName, 'a') as out:
    writer = csv.writer(out, lineterminator='\n')
    writer.writerows([head])
out.close()

# Check list of companies to get URLs
for i in tqdm(range(1, len(firstName))):
    driver.get("https://duckduckgo.com/")
    searchBar = driver.find_element_by_id('search_form_input_homepage')
    searchInput = 'site:www.linkedin.com/in/ AND ' + ' AND ' + names[i] + ' AND ' + title[i]
    searchBar.send_keys(searchInput)
    searchBar.send_keys(Keys.RETURN)
    # print("Searching company # " + str(i))
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all("span", {"class": "result__url__full"})
    if len(links) != 0:
        result = str(links[0])
        result = result.replace('<span class="result__url__full">', 'www.linkedin.com')
        result = result.replace('</span>', '')
        # print(result)
        urls.append(result)

    else: urls.append('No link found, line 95')
    # print(urls)

    with open(outputName, 'a') as out:
        writer = csv.writer(out, lineterminator='\n')
        allthings = list()
        errorWrite = ["Can't encode characters", "Can't encode characters", "Can't encode characters", "Can't encode characters"]
        try: allthings.append(firstName[i])
        except UnicodeEncodeError: allthings.append('')
        try: allthings.append(lastName[i])
        except UnicodeEncodeError: allthings.append('')
        # try: allthings.append(comp[i])
        # except UnicodeEncodeError: allthings.append('')
        try: allthings.append(urls[i])
        except UnicodeEncodeError: allthings.append('')
        try: writer.writerow(allthings)
        except UnicodeEncodeError: writer.writerow(errorWrite)
    out.close()
'''
    if i % 4 == 0:
        time.sleep(180)
'''