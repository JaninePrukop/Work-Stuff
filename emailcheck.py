# Author Janine Prukop
# Date last modified 5/23/2019

import csv
from tqdm import tqdm
import validateBundle
import os
import random
import sys
import time

# inFile = input("What file are we reading from? ") + '.csv'
emailHeader = input("Email column header: ")
# firstHeader = input("First name column header: ")
# lastHeader = input("Last name column header: ")
runs = int(input("How many times do you want to check? "))
if runs < 1:
    print("You need to check st least once.")
    sys.exit()
emails = []
finalOutput = []


if __name__ == '__main__':
    directory = os.listdir()
    print(directory)
    for j in range(len(directory)):
        if directory[j].startswith("output"):
            continue
        elif directory[j].endswith('csv'):
            inFile = directory[j]
        else: continue
        outFile = "output8_" + inFile
        with open(inFile, 'r') as in_file:
            count = 0
            readCSV = csv.reader(in_file, delimiter=',')
            em = -1
            # fn = -1
            # ln = -1
            header = next(readCSV)
            header.append('Email result')
            # print(header)
            for i in range(len(header)):
                # print(header[i].lower())
                if header[i].lower() == emailHeader.lower():
                    em = i
                    # print(em)
                # elif header[i].lower() == firstHeader.lower():
                #     fn = i
                    # print(fn)
                # elif header[i].lower() == lastHeader.lower():
                #     ln = i
                    # print(ln)
            if em == -1:
                print("header for " + inFile + "incomplete or in wrong format")
                exit()
            for row in readCSV:
                emails.append(row)
            print(emails)

        index = random.sample(range(len(emails)), len(emails))
        while count < runs:
            result = ['']
            result[0] = ('error, line 52', 'error, line 52')
            newIndex = []
            for i in tqdm(index, desc='Checking Emails'):
                output = emails[i]
                result[0] = ('error, line 51', 'error, line 51')
                # print(row)
                # print(output)
                if len(emails[i]) > 0:
                    # first = row[fn]
                    # last = row[ln]
                    email = emails[i][em]
                    result = list(validateBundle.validate(email))
                    # print(result)
                    if result[0][1] == 'Bad Email':
                        newIndex.append(i)
                    # print(result)
                    else:
                        if count == 0:
                            output.append(result[0][1])
                        else:
                            output.append('Soft Bounce')
                        finalOutput.append(output)
                    time.sleep(.5)
                    # print(output)
                else: break
            index = newIndex
            count += 1
        if len(index) > 0:
            for num in index:
                output = emails[num]
                output.append('Hard Bounce')
                finalOutput.append(output)
    with open(outFile, 'a', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerows([header])
        for line in finalOutput:
            writer.writerows([line])
