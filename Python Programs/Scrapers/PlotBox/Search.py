from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

driver = webdriver.Chrome()
cities = []
states = []
populations = []
urls = []
cemetaries = []
inFile = input('What file are we reading from? ') + '.csv'
outputName = 'cemetaries_' + inFile
header = ['City', 'State', 'Population', 'City URL', 'Cemetery URL']
with open(outputName, 'a') as out:
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(header)

with open(inFile) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    innerCity = []
    innerState = []
    for row in readCSV:
        innerCity = row[0]
        innerState = row[1]
        innerPopulation = row[2]
        innerUrl = row[3]
        cities.append(innerCity)
        states.append(innerState)
        populations.append(innerPopulation)
        urls.append(innerUrl)

print(cities)
print(states)
print(populations)


cemetaries = [''] * len(cities)

for j in range(1, len(cities)):
    driver.get("https://duckduckgo.com/")
    searchBar = driver.find_element_by_id('search_form_input_homepage')
    searchInput = 'Cemetery cite:' + urls[j]
    searchBar.send_keys(searchInput)
    searchBar.send_keys(Keys.RETURN)
    print("Searching name # : " + str(j))
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all("span", {"class": "result__url__domain"})
    print(links)
    if len(links) > 0:
        i = 0
        while i < len(links):
            if 'findagrave' in str(links[i]):
                i += 1
                continue
            elif 'wiki' in str(links[i]):
                i += 1
                continue
            elif 'zillow' in str(links[i]):
                i += 1
                continue
            else: newi = i + 100
            result = str(links[i])
            result = result.replace('<span class="result__url__domain">', '')
            result = result.replace('</span>', '')
            result = result.replace('https://', '')
            result = result.replace('http://', '')
            result = result.strip('/')
            cemetaries[j] = result
            print(result)
            print(cemetaries[j])
            i += newi

    else:
        cemetaries[j] = "Can't find link"

    row = []
    row.append(cities[j])
    row.append(states[j])
    row.append(populations[j])
    row.append(urls[j])
    row.append(cemetaries[j])
    with open(outputName, 'a') as out:
        writer = csv.writer(out, lineterminator='\n')
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            writer.writerow(['error', 'error', 'error', 'error'])







