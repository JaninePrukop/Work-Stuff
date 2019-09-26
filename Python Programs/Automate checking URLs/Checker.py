import csv
from selenium import webdriver


inputName = input('File name: ') + '.csv'

urlList = []
resultsList = []
count = 0

with open(inputName) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        urlList.append(row[0])
        count += 1
print(count)

print(urlList)

driver = webdriver.Chrome()
for i in range(1, len(urlList)):
    target = 'https://' + urlList[i]
    driver.get(target)
    input('Are you done?')
