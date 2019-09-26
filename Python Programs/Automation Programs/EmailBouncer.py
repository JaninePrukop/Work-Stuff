"""
Author Janine Prukop
Date last modified 7/2/2019

This program checks the emails, for a designated number of times, and returns if the email was good, if it hard bounced,
soft bounced, or timed out.

This program requires the input .csv to be in the directory with it.
"""


from tqdm import tqdm
import validateBundle
import random
import time
import csv
# pip install py3dns


def checker(emails, runs):
    results = list(str(' ') * len(emails))
    # print(len(emails))
    index = random.sample(range(len(emails)), len(emails))
    count = 0
    while count < runs:
        print(count)
        result = ['']
        result[0] = ('error, line 52', 'error, line 52')
        newIndex = []
        for i in tqdm(index, desc='Checking Emails'):
            output = []
            output.append(emails[i])
            result[0] = ('error, line 51', 'error, line 51')
            if len(emails[i]) > 0:
                email = emails[i]
                result = list(validateBundle.validate(email))
                if result[0][1] == 'Bad Email':
                    newIndex.append(i)
                else:
                    if count == 0:
                        results[i] = result[0][1]
                    else:
                        results[i] = 'Soft Bounce'
                time.sleep(.5)
            else:
                results[i] = 'No email provided'
        index = newIndex
        count += 1
    if len(index) > 0:
        for num in index:
            output[0] = emails[num]
            results[num] = 'Hard Bounce'
    return results


if __name__ == '__main__':
    inFile = input("What file are we reading from? ") + ".csv"
    outFile = "BounceCheck_" + inFile
    emailHeader = input("What header does the email column have? ")
    num = int(input("How many times do you want to check the emails? "))
    with open(inFile, 'r') as in_file:
        emails = ['Email']
        count = 0
        readCSV = csv.reader(in_file, delimiter=',')
        em = -1
        # fn = -1
        # ln = -1
        header = next(readCSV)
        # print(header)
        for i in range(len(header)):
            # print(header[i].lower())
            if header[i].lower() == emailHeader.lower():
                em = i

        if em == -1:
            print("header for " + inFile + "incomplete or in wrong format")
            exit()
        for row in readCSV:
            emails.append(row[em])
        print(emails)

    results = checker(emails, num)

    with open(outFile, 'a', newline='') as out_file:
        writer = csv.writer(out_file)
        for i in range(len(emails)):
            writer.writerow([emails[i], results[i]])
