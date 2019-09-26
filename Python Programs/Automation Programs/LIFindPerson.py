"""
Written by Janine Prukop
Created 5-15-2019
Last Edit: 7-15-2019

This program requires chomedriver.exe and the input .csv to be in the directory with it.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import csv


def linkedIn(names, comp, login, pssword):

    urls = []
    urls.append("URL result")

    driver = webdriver.Chrome()

    StartUrl = 'http://www.linkedin.com/in/mikehazel'
    driver.get(StartUrl)
    time.sleep(2)
    driver.find_element_by_link_text('Sign in').click()

    try:
        emailLogin = driver.find_element_by_id("login-email")
    except:
        emailLogin = driver.find_element_by_id("username")
    emailLogin.send_keys(login)

    time.sleep(2)

    try:
        passLogin = driver.find_element_by_id("login-password")
    except:
        passLogin = driver.find_element_by_id("password")
    passLogin.send_keys(pssword)
    passLogin.send_keys(Keys.RETURN)

    # Check list of companies to get URLs
    for i in tqdm(range(1, len(names))):
        if names[i] == '':
            urls.append('No name provided')
            continue


        driver.get("https://cse.google.com/cse?cx=009462381166450434430:ecyvn9zudgu")
        searchBar = driver.find_element_by_name('search')
        searchInput = comp[i] + ' ' + names[i]
        searchBar.send_keys(searchInput)
        searchBar.send_keys(Keys.RETURN)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all("div", {"class": "gs-bidi-start-align"})
        if len(links) != 0:
            temp = links[1].contents
            result = ''
            for item in temp:
                result += str(item)
            result = result.replace('<b>', '')
            result = result.replace('</b>', '')
            urls.append(result)

        else:
            urls.append('No link found, line 48')

    return urls

if __name__ == '__main__':
    inFile = input("What file are we reading from? ") + '.csv'
    outFile = 'LinkedInPersonFinder_' + inFile
    compLabel = input("What is the header name for the company names? ")
    nameLabel = input("What is the header name for the person's full name? ")
    email = input("What is your LinkedIn login email? ")
    password = input("What is your LinkedIn Password? ")


    with open(inFile, 'r') as in_file:
        companies = ['Company']
        names = ['Full name']
        count = 0
        readCSV = csv.reader(in_file, delimiter=',')
        com = -1
        nm = -1
        # ln = -1
        header = next(readCSV)
        # print(header)
        for i in range(len(header)):
            # print(header[i].lower())
            if header[i].lower() == compLabel.lower():
                com = i
            elif header[i].lower() == nameLabel.lower():
                nm = i

        if nm == -1 or com == -1:
            print("header for " + inFile + "incomplete or in wrong format")
            exit()
        for row in readCSV:
            companies.append(row[com])
            names.append(row[nm])
        print(companies)
        print(names)

        links = linkedIn(names, companies, email, password)

        with open(outFile, 'a', newline='') as out_file:
            writer = csv.writer(out_file)
            for i in range(len(links)):
                writer.writerow([names[i], companies[i], links[i]])
