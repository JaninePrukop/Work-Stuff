"""
Written by Janine Prukop
Created 4-10-2019
Last Edit: 4-15-2019
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
outputName = 'MarketingOutputStarting4-22Afternoon.csv'

driver = webdriver.Chrome()

urls = []
comp = []
comp2 = []
urls2 = []
debug = []
count = 0

# Open the CSV file with URLS and read into two list
with open('theRestofthe4000v2.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        urls.append(row[0])
        comp.append(row[1])
        count += 1
print(count)

# Close the CSV file
csvfile.close()

comp2.append("Company result from URL search")
urls2.append("URL result from Company search")
debug.append("Full name pre-split to debug")

driver.get(StartUrl)
time.sleep(4)

driver.find_element_by_partial_link_text('Sign in').click()

emailLogin = driver.find_element_by_class_name('login-email')
emailLogin.send_keys('EXAMPLE@Gmail.com')

time.sleep(2)

passLogin = driver.find_element_by_xpath('//*[@id="login-password"]')
passLogin.send_keys('EXAMPLE')
passLogin.send_keys(Keys.RETURN)

time.sleep(5)

head = list()

head.append(urls[0])
head.append(comp2[0])
head.append(urls2[0])
head.append(comp[0])
head.append(debug[0])

with open(outputName, 'a') as out:
    writer = csv.writer(out, lineterminator='\n')
    writer.writerows([head])
out.close()

# Check list of companies to get URLs
for i in range(len(comp)-1):
    driver.get("https://www.google.com")
    searchBar = driver.find_element_by_css_selector('.gLFyf.gsfi')
    searchInput = 'site:www.linkedin.com/company/ AND ' + comp[i+1]
    searchBar.send_keys(searchInput)
    searchBar.send_keys(Keys.RETURN)
    print("Searching company # " + str(i))
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('cite')
    if len(links) != 0:
        result = str(links[0])
        result = result.replace('<cite class="iUh30">', "")
        result = result.replace('</cite>', "")
        print(result)
        try:
            driver.get(result + '/about/')
            time.sleep(5)
            tempHtml = driver.page_source
            tempsoup = BeautifulSoup(tempHtml, 'lxml')
            templinks = tempsoup.find_all('span', {"class": "link-without-visited-state"})
            # for item in templinks: print(item)
            if len(templinks) > 0:
                cleaned = str(templinks[0]).replace('<span class="link-without-visited-state" dir="ltr">', "")
                cleaned = cleaned.replace('</span>', '')
                cleaned = cleaned.replace('://', '')
                urls2.append(cleaned)
            else: urls2.append('No link found in loop, line 104')
        except WebDriverException: urls2.append('Cannot get to LinkedIn from here Line 105')
        time.sleep(5)

    else: urls2.append('No link found, line 108')
    print(urls2)

    # Check list of URLs to get companies
    driver.get("https://www.google.com")
    searchBar = driver.find_element_by_css_selector('.gLFyf.gsfi')
    searchInput = 'site:www.linkedin.com/company/ AND ' + urls[i + 1]
    searchBar.send_keys(searchInput)
    searchBar.send_keys(Keys.RETURN)
    print("Searching html # : " + str(i))
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('cite')
    if len(links) != 0:
        result = str(links[0])
        result = result.replace('<cite class="iUh30">', '')
        result = result.replace('</cite>', '')
        print(result)
        try:
            driver.get(result + '/about/')
            time.sleep(5)
            tempHtml = driver.page_source
            tempsoup = BeautifulSoup(tempHtml, 'lxml')
            tempnames = tempsoup.find_all('h1', class_="org-top-card-summary__title")
            if len(tempnames) != 0:
                debug.append(tempnames[0])
                splitresult = str(tempnames[0]).split('"')
                cleanresult = splitresult[-1].replace("</span>\n</h1>", "")
                cleanresult = cleanresult.strip(">")
                comp2.append(cleanresult)

            else:
                comp2.append('No name found, line 145')
                debug.append('No name found, line 146')
        except WebDriverException:
            comp2.append('Cannot get to LinkedIn from here Line 141')
            debug.append("Couldn't get to linkedin")

    else:
        comp2.append('No name found, line 143')
        debug.append("No link found")
    print(comp2)
    time.sleep(30 + randint(0, 15))

    with open(outputName, 'a') as out:
        writer = csv.writer(out, lineterminator='\n')
        allthings = list()
        errorWrite = ["Can't encode characters", "Can't encode characters", "Can't encode characters", "Can't encode \
                                                                                                       characters"]
        try: allthings.append(urls[i+1])
        except UnicodeEncodeError: allthings.append('')
        try: allthings.append(comp2[i+1])
        except UnicodeEncodeError: allthings.append('')
        try: allthings.append(urls2[i+1])
        except UnicodeEncodeError: allthings.append('')
        try: allthings.append(comp[i+1])
        except UnicodeEncodeError: allthings.append('')
        try: allthings.append(debug[i+1])
        except UnicodeEncodeError: allthings.append('')
        try: writer.writerow(allthings)
        except UnicodeEncodeError: writer.writerow(errorWrite)
    out.close()

    if i % 4 == 0:
        time.sleep(180)
