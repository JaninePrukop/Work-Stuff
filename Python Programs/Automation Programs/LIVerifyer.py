"""
Written By Janine Prukop

Headers required (Order matters):
    URLs, Person's name, Company name

This will take a list of company names and LinkedIn URLs from a .csv file and return an output file that adds the found
urls. It will ask what your LinkedIn Login Info is, and what file to read out.

This program requires chomedriver.exe and the input .csv to be in the directory with it.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import csv
from CompLinksFromNames import URLFinder
# pip install lxml


# Open the CSV file with URLS and read into a list
def verifier(names, urls, comps, login, pssword):
    print('length of names : ', len(names))
    print('length of urls : ', len(urls))
    print('length of comps : ', len(comps))
    for item in comps:
        print(item)

    driver = webdriver.Chrome()
    status = list()
    status.append('Status')
    companies = [['Company1', 'Company2', 'Company3']]
    titles = [['Title1', 'Title2', 'Title3']]
    companyURLS = [['URL1', 'URL2', 'URL3']]
    deBug = [['Debug1', 'Debug2', 'Debug3']]
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

    time.sleep(60)

    providedCompURLS = [''] * len(urls)
    providedCompURLS = URLFinder(comps[0:len(urls)], providedCompURLS)
    print('provided URLS : \n', providedCompURLS)
    print(len(providedCompURLS))

    for i in tqdm(range(1, len(urls))):

        compNames = []
        jobTitles = []
        compDates = []
        innerDebug = []
        try:
            driver.get(urls[i])
        except:
            status.append('ERROR')
            companies.append(['ERROR', 'ERROR', 'ERROR'])
            titles.append(['ERROR', 'ERROR', 'ERROR'])
            deBug.append(['ERROR', 'ERROR', 'ERROR'])
            continue
        time.sleep(20)
        driver.execute_script("window.scrollTo(0, 250);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 540);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 1080);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 16200);")
        time.sleep(20)
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        # try:
        test1 = soup.find_all('div',
                              attrs={'class': 'pv-entity__summary-info pv-entity__summary-info--background-section '
                                              'mb2'})
        print('\n\nThere are ', len(test1), ' items in test1. \n\n')
        test2 = soup.find_all('li', attrs={'class': 'pv-profile-section__card-item-v2 pv-profile-section '
                                                    'pv-position-entity ember-view'})
        print('\n\nThere are ', len(test2), ' items in test2. \n\n')
        test = test1 + test2

        for k in range(len(test)):
            allDates = test[k].find_all('h4')
            print(allDates)
            if allDates != []:
                dates = str(allDates[1])
                if 'Employment Duration' in dates:
                    dates = str(allDates[0])
                dates = dates.replace('<h4 class="pv-entity__date-range t-14 t-black--light t-normal">', '')
                dates = dates.replace('<span class="visually-hidden">Dates Employed</span>', '')
                dates = dates.replace('<span>', '')
                dates = dates.replace('</span>', '')
                dates = dates.replace('</h4>', '')
                dates = dates.strip()
                compDates.append(dates)
            else:
                compDates.append('none')
            # print(compDates)
            try:
                compNames.append(test[k].find('p', attrs={'class': 'pv-entity__secondary-title'}).text)
                innerDebug.append(' ')
                jobTitles.append(test[k].find('h3').text)
            except:
                try:
                    second = test[k].find_all('h3')
                    comp = second[0].text.split('\n')
                    compNames.append(comp[2])
                    title = second[1].text.split('\n')
                    jobTitles.append(title[2])
                except:
                    compNames.append('Line 119')
                    jobTitles.append('Line120')

            compURLS = [''] * len(compNames)
            compURLS = URLFinder(compNames, compURLS)
            if len(compNames) < 3:
                for l in range(3 - len(compNames)):
                    compNames.append('No Company')
            if len(jobTitles) < 3:
                for l in range(3 - len(jobTitles)):
                    jobTitles.append('No Company')
            if len(compURLS) < 3:
                for l in range(3 - len(compURLS)):
                    compURLS.append('No Company')
            if len(innerDebug) < 3:
                for l in range(3 - len(innerDebug)):
                    innerDebug.append('No Company')

            # print(compURLS)
            # print(innerDebug)
            companyURLS.append(compURLS[:3])
            companies.append(compNames[:3])
            titles.append(jobTitles[:3])
            deBug.append(innerDebug[:3])
            content = compNames[0]
            if len(companyURLS) < k:
                companyURLS.append([' ', ' ', ' '])

        # print('Content: \n', content)
        # print('list of companies: \n', companies)
        # print('List of titles: \n', titles)

        for m in range(len(compDates)):
            if 'Present' in compDates[m]:
                if str(providedCompURLS[i]).strip() == str(compURLS[m]):
                    status.append('True')
                    print('Current job matched')
                    print("Provided Comp URL : ", providedCompURLS[i])
                    print("\nFound Comp URL : ", compURLS[m])
                    print('\nCompany employment dates: \n', compDates[m])
                    break
            else:
                if providedCompURLS[i] == compURLS[m]:
                    status.append('False')
                    print('Old job matched')
                    print("Provided Comp URL : ", providedCompURLS[i])
                    print("\nFound Comp URL : ", compURLS[m])
                    print('\nCompany employment dates: \n', compDates[m])
                    break
        if len(status) < i + 1:
            status.append('Get a human')
    return status


if __name__ == '__main__':
    pos = []
    login = input("What's your LinkedIn login?: ")
    pssword = input("What's your LinkedIn password?: ")
    inFile = input("What file are we reading from?: ") + '.csv'
    outFile = 'LIVerified_' + inFile

    with open(inFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        urls = []
        names = []
        comps = []
        for row in readCSV:
            print(row)
            url = row[0]
            name = row[1]
            comp = row[2]

            # If File does not have a linkedIn URL skip it
            # if 'linkedin' not in url.lower():
                # urls.append('no url')
                # continue
            # Read contacts with linkedIn URLs into lists
            # else:
            urls.append(url)
            names.append(name)
            comps.append(comp)
        print(comps)

    status = verifier(names, urls, comps, login, pssword)

    head = list()

    head.append(urls[0])
    head.append(names[0])
    head.append(comps[0])
    head.append('Status')

    with open(outFile, 'a') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerows([head])
        for i in range(1, len(urls)):
            all = list()
            oURL = urls[i]
            oName = names[i]
            oComp = comps[i]
            oStatus = status[i]
            all.append(oURL)
            all.append(oName)
            all.append(oComp)
            all.append(oStatus)
            writer.writerows([all])
