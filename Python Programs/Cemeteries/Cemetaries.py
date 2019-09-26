from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

driver = webdriver.Chrome()
cities = []
states = []
populations = []
inFile = input('What file are we reading from? ') + '.csv'
outputName = 'output_' + inFile

with open(inFile) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    innerCity = []
    innerState = []
    for row in readCSV:
        innerCity = row[0]
        innerState = row[1]
        populations = row[2]

        cities.append(innerCity)
        states.append(innerState)

urls = [''] * len(cities)

for j in range(len(cities)):
    driver.get("https://duckduckgo.com/")
    searchBar = driver.find_element_by_id('search_form_input_homepage')
    searchInput = 'City of ' + cities[j] + ', ' + states[j] + ' cemetery'
    searchBar.send_keys(searchInput)
    searchBar.send_keys(Keys.RETURN)
    print("Searching name # : " + str(j + 1))
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all("span", {"class": "result__url__domain"})
    if len(links) != 0:
        # print(links)
        result = str(links[0])
        result = result.replace('<span class="result__url__domain">', '')
        result = result.replace('</span>', '')
        result = result.replace('https://', '')
        result = result.replace('http://', '')
        result = result.strip('/')
        urls[j] = result
    else: urls[j] = "Couldn't find a link"

for i in range(len(cities)):
    row = []
    row.append(cities[i])
    row.append(states[i])
    row.append(populations[i])
    row.append(urls[i])
    with open(outputName, 'a') as out:
        writer = csv.writer(out, lineterminator='\n')
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            writer.writerow([names[i], 'error'])









