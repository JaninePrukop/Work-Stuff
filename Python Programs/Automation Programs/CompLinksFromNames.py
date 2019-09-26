"""
Written by Janine Prukop

Header needed (Order matters):
    Company Name, Company URL

This will take a list of company names from a .csv file and return an output file that adds the found urls.
It will ask what what file to read out of and if you want to leave any existing websites.

This program requires chomedriver.exe and the input .csv to be in the directory with it.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
# pip install lxml


def URLFinder(namelist, urls):

    driver = webdriver.Chrome()
    for j in range(len(namelist)):
        driver.get("https://duckduckgo.com/")
        searchBar = driver.find_element_by_id('search_form_input_homepage')
        searchInput = namelist[j]
        try: searchBar.send_keys(searchInput)
        except: searchBar = driver.find_element_by_class_name('js-search-input')
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
    driver.close()
    return urls


if __name__ == '__main__':
    inputName = input('File name: ') + '.csv'
    outputName = 'CompWebsites_' + inputName
    replace = input('Do you want to replace the existing URLs? (Y/N): ')

    names = []
    urlLi = []
    count = 0

    # Open the CSV file with URLS and read into two list
    with open(inputName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            names.append(row[0])
            if replace == 'n' or replace == 'N':
                urlLi.append(row[1])
            else:
                urlLi.append('')
    csvfile.close()

    urls = URLFinder(names, urlLi)

    for i in range(len(names)):
        row = []
        row.append(names[i])
        row.append(urls[i])
        with open(outputName, 'a') as out:
            writer = csv.writer(out, lineterminator='\n')
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                writer.writerow([names[i], 'error'])

