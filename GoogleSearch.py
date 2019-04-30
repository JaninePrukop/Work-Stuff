"""
Written by Janine Prukop
Created 4-24-2019
Last Edit: 4-24-2019
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

inputName = 'TargetAccounts.csv'
outputName = 'Output2_' + inputName
driver = webdriver.Chrome()

names = []
urls = []
count = 0

# Open the CSV file with URLS and read into two list
with open(inputName) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        names.append(row[0])
        urls.append(row[1])
        print(row[0])
        count += 1
print(count)
csvfile.close()


for i in range(count):
    row = []
    if urls[i] != '':
        row.append(names[i])
        row.append(urls[i])
        with open(outputName, 'a') as out:
            writer = csv.writer(out, lineterminator='\n')
            writer.writerow(row)
        out.close()
    else:
        driver.get("https://www.google.com")
        searchBar = driver.find_element_by_css_selector('.gLFyf.gsfi')
        searchInput = names[i]
        searchBar.send_keys(searchInput)
        searchBar.send_keys(Keys.RETURN)
        print("Searching name # : " + str(i))
        time.sleep(5 + randint(0, 15))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('cite')
        if len(links) != 0:
            result = str(links[0])
            result = result.replace('<cite class="iUh30">', '')
            result = result.replace('</cite>', '')
            result = result.replace('https://', '')
            result = result.strip('/')
            urls[i] = result
        else: urls[i] = "Couldn't find a link"

        row.append(names[i])
        row.append(urls[i])
        with open(outputName, 'a') as out:
            writer = csv.writer(out, lineterminator='\n')
            try: writer.writerow(row)
            except UnicodeEncodeError:
                writer.writerow([names[i], 'error'])
        out.close()

