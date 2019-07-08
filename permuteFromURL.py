# Written by Janine Prukop
# Date last modified 5/22/2019

import csv
from tqdm import tqdm
import validateBundle
import time

startTime = time.perf_counter()

inFile = input('What file do you want to read from? ') + '.csv'
outFile = 'output_' + inFile
firstName = input('First name header: ')
lastName = input('Last name header: ')
domain = input('Domain header: ')

if __name__ == '__main__':

    with open(inFile, 'r') as in_file:
        readCSV = csv.reader(in_file, delimiter=',')
        em = -1
        fn = -1
        ln = -1
        header = next(readCSV)
        header.append('Final email')
        header.append('Email result')
        # print(header)
        for i in range(len(header)):
            if header[i].lower() == domain.lower():
                em = i
                # print(em)
            elif header[i].lower() == firstName.lower():
                fn = i
                # print(fn)
            elif header[i].lower() == lastName.lower():
                ln = i
                # print(ln)
        if em == -1:
            print("Could not find header with ", domain)
            exit()
        elif fn == -1:
            print("Could not find header with ", firstName)
            exit()
        elif ln == -1:
            print("Could not find header with ", lastName)
            exit()

        with open(outFile, 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerows([header])
            for row in tqdm(readCSV, desc='Checking Emails'):
                output = row
                # print(row)
                # print(output)
                if len(row) > 0:
                    result = list(validateBundle.permute(row[fn], row[ln], row[em]))
                    # print(result)
                    output.append(result[0])
                    output.append(result[1])
                    # print(output)
                    writer.writerows([output])
                else: break
        out_file.close()
    in_file.close()

endTime = time.perf_counter()
totalTime = endTime - startTime
# timeSecs = totalTime/1000000000
print("Time executed = ", totalTime, ' seconds')