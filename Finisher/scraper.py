"""
Written by Janine Prukop
Created 5-15-2019
Last Edit: 6-27-2019
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm


def linkedIn(names, title, login, psswrd):
    StartUrl = 'http://www.linkedin.com/in/mikehazel'

    urls = []
    urls.append("URL result")

    driver = webdriver.Chrome()

    driver.get(StartUrl)
    time.sleep(5)

    driver.find_element_by_partial_link_text('Sign in').click()
    time.sleep(2)

    emailLogin = driver.find_element_by_id('login-email')
    emailLogin.send_keys(login)

    time.sleep(2)

    passLogin = driver.find_element_by_id('login-password')
    passLogin.send_keys(psswrd)
    passLogin.send_keys(Keys.RETURN)

    time.sleep(5)

    # Check list of companies to get URLs
    for i in tqdm(range(1, len(names))):
        if names[i] == '':
            urls.append('No name provided')
            continue
        driver.get("https://duckduckgo.com/")
        searchBar = driver.find_element_by_id('search_form_input_homepage')
        searchInput = 'site:www.linkedin.com/in/ AND ' + names[i] + ' AND ' + title[i]
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

        else:
            urls.append('No link found, line 95')
        # print(urls)

    return urls

